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

class SnakeError(Exception):
    def __init__(self,info):
        Exception.__init__(self,"Error : %s\n" % info)

# App Screen Error {
class SKAppScreenError(SnakeError):
    def __init__(self,info):
        SnakeError.__init__(self,info)

# } Snake Error {
class SKSnakeError(SnakeError):
    def __init__(self,info): SnakeError.__init(self,info)

class SKSnakeWrongDirection(SKSnakeError):
    def __init__(self):
        SKSnakeError.__init__("Wrong Direction!The direction parament must be DIR_RG,DIR_LF,DIR_UP or DIR_DW")
# } Setting Error {
class SKSettingError(SnakeError):
    def __init__(self,info):
        SnakeError.__init__(self,info)

class SettingFileNotFound(SKSettingError):
    def __init__(self,path):
        SKSettingError.__init__(self,"Setting file: %s not found!" % path)

class LoadSettingFail(SKSettingError):
    def __init__(self,info):
        SKSettingError.__init__(self,"Load settings fail: %s" % info)

class WrongSetting(SKSettingError):
    def __init__(self,attr):
        SKSettingError.__init__(self,"Wrong setting name : %s" % attr)

# }
