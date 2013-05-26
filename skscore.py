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
import os
MAX_SCORE_CNT = 5

class SKScore:
    def __init__(self):
        score_file = skenv.INST_DIR + "/score.dat"
        self.score_list = []

        if os.path.isfile(score_file):
            for line in open(score_file):
                score = line.rstrip()
                self.update_rec(int(score))

    def update_rec(self,score):
        self.score_list.append(score)
        self.score_list.sort(reverse = True)
        if len(self.score_list) > MAX_SCORE_CNT:
            self.score_list = self.score_list[:-1]

    def __iter__(self): return iter(self.score_list)

    def __del__(self):
        import skenv
        fp = open(skenv.INST_DIR + "/score.dat","w")
        for rec in self.score_list:
            fp.write("%d\n" % rec)
        fp.close()

if __name__ == "__main__":
    sc = SKScore()
    for it in sc:
        print it
