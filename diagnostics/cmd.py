#
# cmd.py
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPLv2
#
# run a command
#

import os
import subprocess
import shlex


def run_cmd(cmd):
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    return stdout, stderr


def run_root_cmd(cmd, passwd='kano'):
    with open(os.devnull, 'w') as null_f:
        proc = subprocess.Popen(
            ['sudo', '-S', '-k'] + shlex.split(cmd),
            stdin=subprocess.PIPE,
            stdout=null_f,
            stderr=null_f
        )
        proc.communicate('{}\n'.format(passwd))
