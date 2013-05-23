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

version = "0.1"
INST_DIR = "/home/rapid/Desktop/repository/snake"

SettingTree = {
    "settings" : {
        "app" : {
            "size" : ("height","width"),
        },
        "game" : {
            "level" : {
                "lv1" : ("interval","add_length"),
                "lv2" : ("interval","add_length"),
                "lv3" : ("interval","add_length"),
                "lv4" : ("interval","add_length"),
                "lv5" : ("interval","add_length"),
                "lv6" : ("interval","add_length"),
                "lv7" : ("interval","add_length"),
                "lv8" : ("interval","add_length"),
                "lv9" : ("interval","add_length"),
            },
        },
    }
}
