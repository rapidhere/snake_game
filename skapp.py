#!/usr/bin/python

# Copyright (C) 2013 rapidhere
#
# Author:     rapidhere <rapidhere@gmail.com>
# Maintainer: rapidhere <rapidhere@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import skgame
import skerr
import sksetting
import skenv

import os
import fcntl
import time
import sys
import random
import curses

class AppScreen:
    def __init__(self,min_height,min_width):
        scr = curses.initscr()
        scr_size = scr.getmaxyx()
        if scr_size[0] < min_height or scr_size[1] < min_width:
            raise skerr.SKAppScreenTooSmall()
        self.stdscr = curses.newwin(min_height,min_width,0,0)
        self.menuscr = self.stdscr.subwin(min_height - 2,min_width - 2,1,1)

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)

        if not curses.has_colors():
            raise skerr.SKAppScreenError("No color support!")
        curses.start_color()
        COLOR_CNF = (
            ("COLOR_GAME_INFO"  ,curses.COLOR_BLUE  ,curses.COLOR_WHITE),
            ("COLOR_GAME_SNAKE" ,curses.COLOR_WHITE ,curses.COLOR_BLACK),
            ("COLOR_GAME_SCORE" ,curses.COLOR_RED   ,curses.COLOR_WHITE),
        )
        for cnf in COLOR_CNF:
            idx = COLOR_CNF.index(cnf) + 1
            setattr(self,cnf[0],idx)
            curses.init_pair(idx,cnf[1],cnf[2])

    def main_menu(self,menu_list,cutoffs,cur_level):
        self.stdscr.clear()
        self.stdscr.box()
        self.stdscr.refresh()

        size = self.menuscr.getmaxyx()

        cur_idx = 0

        title = "Eating Snake - Main Menu"
        self.stdscr.addstr(0,(size[1] + 2 - len(title)) / 2,title,curses.A_BOLD)

        level_buf = "Current Level : %s" % cur_level
        self.menuscr.addstr(size[0] - 1,size[1] - len(level_buf) - 2,level_buf)
        self.menuscr.addstr(size[0] - 2,1,"version %s" % skenv.version)
        self.menuscr.addstr(size[0] - 1,1,"rapidhere@gmail.com")
        self.menuscr.refresh()

        while True:
            self._show_menu(menu_list,cutoffs,cur_idx,(size[1] - len(title)) / 2)
            ch = self.getch()
            if ch < 256 and ch > 0 and chr(ch).upper() in cutoffs:
                cur_idx = cutoffs.index(chr(ch).upper())
            elif ch == curses.KEY_ENTER or ch == 10:
                return cur_idx
            elif ch == curses.KEY_UP:
                cur_idx = max(0,cur_idx - 1)
            elif ch == curses.KEY_DOWN:
                cur_idx = min(len(menu_list) - 1,cur_idx + 1)
            else:
                pass # ignored

    def _show_menu(self,menu_list,cutoffs,curidx,start_x):
        size = self.menuscr.getmaxyx()
        start_y = (size[0] - len(menu_list)) / 2
        self.menuscr.addstr(start_y - 2,start_x,"Options:")
        for i in range(0,len(menu_list)):
            y =  start_y + i
            buf = "[%s] %s" % (cutoffs[i],menu_list[i])
            x = start_x
            if i == curidx:
                self.menuscr.addstr(y,x,buf,curses.A_STANDOUT)
            else:
                self.menuscr.addstr(y,x,buf)
        self.stdscr.touchwin()
        self.stdscr.refresh()

    def choose_level(self,max_lv):
        curses.echo()
        curses.nocbreak()

        tip = "Please enter a level(1~%d):" % max_lv
        width = len(tip) + 5
        try:
            size = self.menuscr.getmaxyx()
            chwin = curses.newwin(3,width,(size[0] - 3) / 2,(size[1] - width) / 2)
            chwin.box(ord('|'),ord('-'))
            chwin.addstr(1,1,tip)
            chwin.refresh()
            try:
                return int(chwin.getstr())
            except ValueError:
                return 1
        finally:
            del chwin
            curses.noecho()
            curses.cbreak()

    def getch(self):
        return self.stdscr.getch()

    def __del__(self):
        import curses
        curses.endwin()

class SKApp:
    def __init__(self):
        random.seed(time.time())
        self.setting = sksetting.SKSetting()
        self.screen = AppScreen(
            int(self.setting.app.size.height),
            int(self.setting.app.size.width),
        )

    def get_input(self):
        return self.screen.getch()

    def run(self):
        MenuItems = (
            "New Game",
            "Load Game",
            "Choose Level",
            "High Scores",
            "Help",
            "Quit"
        )
        Cuttoffs = ("N","L","C","H","E","Q")
        level = 1
        while True:
            idx = self.screen.main_menu(MenuItems,Cuttoffs,"lv%d" % level)

            if idx == 0:
                self.run_game(level)
            elif idx == 1:
                pass
            elif idx == 2:
                maxlv = len(self.setting.game.level)
                level = self.screen.choose_level(maxlv)
                if level < 1: level = 1
                if level > maxlv: level = maxlv
            elif idx == 3:
                pass
            elif idx == 4:
                pass
            elif idx == 5:
                break

    def run_game(self,levelno):
        flag = fcntl.fcntl(0,fcntl.F_GETFL)
        fcntl.fcntl(0,fcntl.F_SETFL,os.O_NONBLOCK)
        try:
            lv = "lv%d" % levelno
            lv = getattr(self.setting.game.level,lv)
            game = skgame.SKGame(self.screen,self.get_input,float(lv.interval),int(lv.add_length))
            game.run()
        finally:
            fcntl.fcntl(0,fcntl.F_SETFL,flag)

if __name__ == "__main__":
    app = SKApp()
    app.run()
