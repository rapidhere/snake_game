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

all: skcurses.so

CC = gcc

skcurses.so : skcurses.o skcurses_wrap.o
	$(CC) $^ -o $@ -lpython2.7 -lcurses -fpic -shared
skcurses.o : skcurses.c skcurses.h
	$(CC) skcurses.c -c -o $@
skcurses_wrap.o : skcurses_wrap.c
	$(CC) $^ -c -o $@ -I/usr/include/python2.7

clean:
	rm -rf *.o *.pyc
