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

import sksnake

import os
import fcntl
import time
import sys
import random
import curses

class SKGameScreen:
    def __init__(self,appscr,snake_ch = 'o'):
        self.scr = appscr.stdscr
        self.scr.clear()

        size = self.scr.getmaxyx()
        self.workwin = self.scr.subwin(size[0] - 1,size[1],1,0)
        self.workwin.box(curses.ACS_VLINE,curses.ACS_HLINE)

        self.last_info_len = 0

        self.COL_SNAKE = curses.color_pair(appscr.COLOR_GAME_SNAKE)
        self.COL_INFO = curses.color_pair(appscr.COLOR_GAME_INFO)
        self.COL_SCORE = curses.color_pair(appscr.COLOR_GAME_SCORE)

        self.snake_ch = snake_ch

    def get_size(self):
        size = self.workwin.getmaxyx()
        return size[0] - 2,size[1] - 2

    def write_info(self,string):
        self.scr.addstr(0,20," " * self.last_info_len)
        self.scr.addstr(0,20,string,self.COL_INFO)
        self.last_info_len = len(string)

    def write_score(self,score):
        self.scr.addstr(0,3,"Score : %s" % score,self.COL_SCORE)

    def draw_point(self,y,x):
        self.workwin.addstr(y + 1,x + 1,self.snake_ch,self.COL_SNAKE)

    def erase_point(self,y,x):
        self.workwin.addstr(y + 1,x + 1," ")

    def refresh(self):
        self.scr.touchwin()
        self.scr.move(0,0)
        self.scr.refresh()

class SKGame:
    def __init__(self,appscr,input_handler,interval = 0.08,add_length = 5):
        self.screen = SKGameScreen(appscr)

        head_pos = self.screen.get_size()
        self.snake = sksnake.Snake((head_pos[1] / 2,head_pos[0] / 2))

        self.interval = interval
        self.add_length = add_length
        self.input_handler = input_handler

    def _rand_food(self):
        _ran_list = []
        winsz = self.screen.get_size()
        for i in range(0,winsz[1]):
            for j in range(0,winsz[0]):
                _ran_list.append((i,j))

        for spos in self.snake.get_body():
            _ran_list.remove(spos)

        return random.choice(_ran_list)

    def run(self):
        win_size = self.screen.get_size()
        food = self._rand_food()

        while True:
            self.screen.write_score(self.snake.get_length())

            ch = self.input_handler()
            if ch != -1:
                if ch < 256:
                    ch = chr(ch)
                if ch == 'w' or ch == 'W' or ch == curses.KEY_UP:
                    self.snake.set_dir(sksnake.DIR_UP)
                elif ch == 'a' or ch == 'A' or ch == curses.KEY_LEFT:
                    self.snake.set_dir(sksnake.DIR_LF)
                elif ch == 's' or ch == 'S' or ch == curses.KEY_DOWN:
                    self.snake.set_dir(sksnake.DIR_DW)
                elif ch == 'd' or ch == 'D' or ch == curses.KEY_RIGHT:
                    self.snake.set_dir(sksnake.DIR_RG)
                elif ch == 'q' or ch == 'Q':
                    break

            last = self.snake.move()
            self.screen.erase_point(last[1],last[0])
            for pnt in self.snake.get_body():
                self.screen.draw_point(pnt[1],pnt[0])

            if self.snake.eat(food,self.add_length):
                self.screen.erase_point(food[1],food[0])
                food = self._rand_food()
            self.screen.draw_point(food[1],food[0])
            self.snake.digest()

            if self.snake.is_out_of_bounary(win_size[1],win_size[0]) or\
                self.snake.is_cut_self():
                self.screen.write_info("You Failed!")
                self.screen.refresh()
                time.sleep(2)
                break

            self.screen.refresh()
            time.sleep(self.interval)

        return self.snake.get_length()
