#
# output.py
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPLv2
#
# Functions to output to the console
#


import sys


class Colours:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(msg, colour=Colours.BLUE, newline=True, only_file=False):
    if not only_file:
        sys.stdout.write("{}{}{}".format(colour, msg, Colours.ENDC))

        if newline:
            sys.stdout.write("\n")

        sys.stdout.flush()
