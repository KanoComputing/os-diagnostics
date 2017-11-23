#
# audio.py
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPLv2
#
# Audio diagnostics functions
#

import subprocess

from diagnostics.cmd import run_cmd

from diagnostics.output import log, Colours

NAME = 'Audio'


def run_speaker_test(where):
    log('Testing Speaker: {}'.format(where))
    cmd = "speaker-test -r 48000 -f 600 -t sine -s 1"
    run_cmd(cmd)
    x = raw_input("What did you hear? ")
    log(x, only_file=True)


def get_audio_routing():
    cmd = "amixer -c 0 cget name='PCM Playback Route'"
    stdout, stderr = run_cmd(cmd)
    try:
        lines = stdout.split('\n')
        val = lines[2].split('=')[1]
        log("audio route: " + val)
        route = val
    except:
        log("failed to parse audio route")
        route = None

    stdout, stderr = run_cmd('vcgencmd get_config  hdmi_ignore_edid_audio')
    log(stdout)

    stdout, stderr = run_cmd('vcgencmd get_config  hdmi_drive')
    log(stdout)

    return route


def set_audio_routing(where):
    cmd = "amixer -c 0 cset name='PCM Playback Route' {}".format(where)
    stdout, stderr = run_cmd(cmd)


def run():
    '''
    Main test entry point
    '''

    saved_route = get_audio_routing()

    run_speaker_test("current")

    set_audio_routing(1)

    run_speaker_test("Speaker")

    set_audio_routing(2)

    run_speaker_test("TV")

    set_audio_routing(saved_route)
