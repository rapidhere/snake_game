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

DIR_RG = (1,0)
DIR_LF = (-1,0)
DIR_UP = (0,-1)
DIR_DW = (0,1)

class Snake:
    def __init__(self,head_pos):
        self.body = [head_pos,(head_pos[0] + 1,head_pos[1]),(head_pos[0] + 2,head_pos[1])]
        self.dir = DIR_LF

        self.eat_rest = 0

    def get_length(self):
        return len(self.body)

    def get_body(self):
        return self.body

    def set_dir(self,direction):
        if ((direction == DIR_RG and self.dir == DIR_LF) or
            (direction == DIR_LF and self.dir == DIR_RG) or
            (direction == DIR_UP and self.dir == DIR_DW) or
            (direction == DIR_DW and self.dir == DIR_UP)):
            return
        self.dir = direction

    def get_dir(self): return self.dir

    def move(self):
        head = self.body[0]
        last = self.body[-1]
        self.body = self.body[:-1]
        self.body = [(head[0] + self.dir[0],head[1] + self.dir[1])] + self.body
        return last

    def is_out_of_bounary(self,width,height):
        head = self.body[0]
        return (head[0] < 0) or (head[1] < 0) or (head[0] >= width) or (head[1] >= height)

    def is_cut_self(self):
        return self.body[0] in self.body[1:]

    def eat(self,food_pos):
        head = self.body[0]
        flag = False
        if head == food_pos:
            flag = True
            self.eat_rest += 5

        if self.eat_rest:
            tail = self.body[-1]
            stail = self.body[-2]
            last_dir = (tail[0] - stail[0],tail[1] - stail[1])
            self.body.append((tail[0] + last_dir[0],tail[1] + last_dir[1]))
            self.eat_rest -= 1

        return flag

if __name__ == "__main__":
    sk = Snake((10,10))
    sk.set_dir(DIR_RG)
