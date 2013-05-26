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

import skapp

from optparse import OptionParser
import sys
parser = OptionParser(
    usage = "%prog [options]",
    description = """A simple snake game.Suggest that resize your terminal window at a property size befor playing!""",
    epilog = "rapidhere@gmail.com",
    version = "0.1"
)

parser.add_option(
    "","--key-help",
    action = "store_true",default = False,
    help = "show game keys"
)

opts,args = parser.parse_args()
parser.destroy()

if opts.key_help:
    print "'w' or 'W' or UP-Arrow   up"
    print "'a' or 'A' or LF-Arrow   left"
    print "'s' or 'S' or DW-Arrow   down"
    print "'d' or 'D' or RG-Arrpw   right"
    print "'q' or 'Q'    quit"
    sys.exit(0)
else:
    app = skapp.SKApp()
    app.run()
