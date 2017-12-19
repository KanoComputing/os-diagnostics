#
# wifi.py
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPLv2
#
# WiFi diagnostics functions
#


import os
import subprocess

from diagnostics.output import log, Colours
from diagnostics.cmd import run_cmd, run_root_cmd


NAME = 'Reset Parental Password'

PARENTAL_LOCK_FILE = '/etc/kano-parental-lock'


class ParentalSetting(object):
    DISABLED = 0
    ENABLED = 1


def get_parental_setting():
    return ParentalSetting.ENABLED \
        if os.path.isfile(PARENTAL_LOCK_FILE) \
        else ParentalSetting.DISABLED


def reset_parental_setting(new_password):
    from kano_settings.system.advanced import encrypt_password

    run_root_cmd('chmod 666 {}'.format(PARENTAL_LOCK_FILE))

    with open(PARENTAL_LOCK_FILE, 'w') as parental_f:
        parental_f.write(encrypt_password(new_password))

    run_root_cmd('chmod 400 {}'.format(PARENTAL_LOCK_FILE))


def run():
    '''
    Main test entry point
    '''

    if get_parental_setting() == ParentalSetting.DISABLED:
        log('Parental setting already disabled. Use the settings app to enable')
        return

    log('Reset parental password')
    passwd = raw_input('Enter new password: ')

    log(
        '\nChanging password to: "{}", do you wish to proceed?'.format(passwd),
        colour=Colours.YELLOW
    )
    confirm = raw_input('Type "yes" to continue, "no" to cancel: ')

    if confirm.lower() not in ['y', 'yes']:
        log(
            '\nDidn\'t receive confirmation. Aborting',
            colour=Colours.RED
        )
        return


    reset_parental_setting(passwd)
    log('\nPassword changed to: {}'.format(passwd), colour=Colours.GREEN)
