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

import skcurses
import skerr

class ScreenMan:
    def __init__(self):
        try:
            skcurses.skcur_init()
        except RuntimeError,r:
            raise skerr.ScreenManError(str(r))
        self._inited = True

    def __del__(self):
        if hasattr(self,"_inited") and self._inited:
            skcurses.skcur_end()

    def get_size(self):
        try:
            return (skcurses.skcur_get_scr_height(),
                skcurses.skcur_get_scr_width()
            )
        except RuntimeError,r:
            raise skerr.ScreenManError(str(r))

    def refresh(self):
        try:
            skcurses.skcur_refresh()
        except RuntimeError,r:
            raise skerr.ScreenManError(str(r))

    def write_info(self,info):
        try:
            skcurses.skcur_write_info(info)
        except RuntimeError,r:
            raise skerr.ScreenManError(str(r))

    def write_score(self,score):
        try:
            skcurses.skcur_write_score(score)
        except RuntimeError,r:
            raise skerr.ScreenManError(str(r))

    def draw_point(self,y,x,color = skcurses.SKCUR_COLOR_WHITE):
        try:
            skcurses.skcur_draw_point(y,x,color)
        except RuntimeError,r:
            raise skerr.ScreenManError(str(r))

    def erase_point(self,y,x):
        try:
            skcurses.skcur_erase_point(y,x)
        except RuntimeError,r:
            raise skerr.ScreenManError(str(r))

    def getch(self):
        try:
            return skcurses.skcur_getch()
        except RuntimeError,r:
            raise skerr.ScreenManError(str(r))

if __name__ == "__main__":
    import time
    sm = ScreenMan()
    sm.write_score(100)
    sm.refresh()
    while True:
        inp = sm.getch()
        print inp
        sm.refresh()
