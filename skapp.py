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

import skcur
import sksnake

import os
import fcntl
import time
import sys
import random

class SKApp:
    def __init__(self):
        random.seed(time.time())
        self.screen = skcur.ScreenMan()

        head_pos = self.screen.get_size()
        self.snake = sksnake.Snake((head_pos[1] / 2,head_pos[0] / 2))

        self.pipefd_pair = os.pipe()
        fcntl.fcntl(self.pipefd_pair[0],fcntl.F_SETFL,os.O_NONBLOCK)

        self.chpid = os.fork()
        self.duration = 0.08
        if self.chpid == 0: # Child Process
            self._handle_keyboard()
            sys.exit(0)

    def _handle_keyboard(self):
        while True:
            inp = self.screen.getch()
            os.write(self.pipefd_pair[1],str(inp) + " ")

    def get_input(self):
        try:
            buf = os.read(self.pipefd_pair[0],1024).rstrip()
            return int(buf.split(" ")[0])
        except OSError:
            return -1

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
        self.screen.write_info("Hello")
        win_size = self.screen.get_size()
        food = self._rand_food()

        while True:
            self.screen.write_score(self.snake.get_length())

            ch = self.get_input()
            if ch != -1:
                ch = chr(ch)
            if ch == 'w' or ch == 'W':
                self.snake.set_dir(sksnake.DIR_UP)
            elif ch == 'a' or ch == 'A':
                self.snake.set_dir(sksnake.DIR_LF)
            elif ch == 's'or ch == 'S':
                self.snake.set_dir(sksnake.DIR_DW)
            elif ch == 'd' or ch == 'D':
                self.snake.set_dir(sksnake.DIR_RG)
            elif ch == 'q' or ch == 'Q':
                break

            last = self.snake.move()
            self.screen.erase_point(last[1],last[0])
            for pnt in self.snake.get_body():
                self.screen.draw_point(pnt[1],pnt[0])

            if self.snake.eat(food):
                self.screen.erase_point(food[1],food[0])
                food = self._rand_food()
            self.screen.draw_point(food[1],food[0])

            if self.snake.is_out_of_bounary(win_size[1],win_size[0]) or\
                self.snake.is_cut_self():
                self.screen.write_info("You Failed!")
                self.screen.refresh()
                time.sleep(2)
                break

            self.screen.refresh()
            time.sleep(self.duration)

    def __del__(self):
        if self.chpid:
            os.kill(self.chpid,15)
            os.wait()

if __name__ == "__main__":
    app = SKApp()
    app.run()
