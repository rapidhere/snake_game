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
import skenv
import skerr

import os
import xml.etree.ElementTree as ElementTree

class SKSetting:
    class SettingContainer:
        def __init__(self,dict_list):
            self.dict_list = dict_list
        def __iter__(self):
            return iter(self.dict_list)
        def __len__(self):
            return len(self.dict_list)
        def __getattr__(self,attr):
            if attr in self.dict_list and hasattr(self,attr):
                return self.attr
            else:
                raise skerr.WrongSetting(attr)

    def __init__(self):
        setting_file = skenv.INST_DIR + "/snake_setting.xml"

        if not os.path.isfile(setting_file):
            raise skerr.SettingFileNotFound(setting_file)
        try:
            root = ElementTree.parse(setting_file).getroot()
            self.build_settings(self,root,skenv.SettingTree["settings"])
        except skerr.LoadSettingFail:
            raise

    def build_settings(self,father,ele,set_tree):
        chlist = ele.getchildren()
        cur = None
        if not chlist:
            attrs = ele.attrib
            if sorted(attrs.keys()) != sorted(set_tree):
                raise skerr.WrongSettingSyntax()
            cur = SKSetting.SettingContainer(attrs.keys())
            for key in attrs:
                setattr(cur,key,attrs[key])
        else:
            taglist = [x.tag for x in chlist]
            if sorted(taglist) != sorted(set_tree.keys()):
                raise skerr.WrongSettingSyntax()
            cur = SKSetting.SettingContainer(taglist)
            for ch in chlist:
                self.build_settings(cur,ch,set_tree[ch.tag])
        setattr(father,ele.tag,cur)

    def __getattr__(self,attr):
        return getattr(self.settings,attr)


if __name__ == "__main__":
    st = SKSetting()
    print len(st.game.level)
