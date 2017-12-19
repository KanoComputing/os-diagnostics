#
# menu.py
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPLv2
#
# Basic menu for the selecting the diagnostics to do
#


import os
import sys

from diagnostics.output import log, Colours

import diagnostics.wifi as wifi
import diagnostics.audio as audio
import diagnostics.parental as parental

TESTS = [
    wifi,
    audio,
    parental
]

def show_main_menu():
    os.system('clear')
    log('============================')
    log('* Kano OS Diagnostics tool *')
    log('============================\n')

    for idx, test in enumerate(TESTS, start=1):
        log('[{}]: '.format(idx), newline=False)
        log(test.NAME, colour=Colours.BLUE)

    option = raw_input('\nSelect an option: ')
    print '\n'

    try:
        choice_idx = int(option) - 1
        TESTS[choice_idx].run()
    except Exception:
        print 'Select a number 1 - {}'.format(len(TESTS))

    raw_input('\nPress ENTER to continue')
