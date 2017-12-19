#
# wifi.py
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPLv2
#
# WiFi diagnostics functions
#


import os
import re
import subprocess

from diagnostics.output import log, Colours
from diagnostics.cmd import run_cmd
from diagnostics.parental import ParentalSetting, get_parental_setting

NAME = 'WiFi'

INTERNET_IP = '8.8.8.8'
INTERNET_HOSTNAME = 'repo.kano.me'


def get_ip_address():
    out, _ = run_cmd('hostname -I')

    return ', '.join(out.strip().split(' '))


def get_wireless_status(iface='wlan0'):
    out, _ = run_cmd('sudo iwconfig {}'.format(iface))

    status = {}

    status['quality'] = ', '.join(re.findall(r'Link Quality=(\d+/\d\d)', out))
    status['rate'] = ', '.join(re.findall(r'Bit Rate=(.* Mb/s)', out))
    status['essid'] = ', '.join(re.findall(r'ESSID:"(.*)"', out))

    iwlist, _ = run_cmd('/sbin/iwlist {} channel'.format(iface))

    status['channel'] = ', '.join(
        re.findall(r'Current Frequency.+\(Channel (\d+)\)', iwlist)
    )

    iwlist_scan, _ = run_cmd('/sbin/iwlist {} scan'.format(iface))
    if re.findall(r'WPA2', iwlist_scan):
        status['encryption'] = 'WPA2'
    elif re.findall(r'WPA', iwlist_scan):
        status['encryption'] = 'WPA'
    elif re.findall(r'WEP', iwlist_scan):
        status['encryption'] = 'WEP'
    else:
        status['encryption'] = 'None'

    return out, status


def get_dns_settings():
    out, _ = run_cmd('cat /etc/resolv.conf')

    nameserver_regex = re.compile(r'^nameserver (.+)$', re.MULTILINE)
    nameservers = nameserver_regex.findall(out)

    return ', '.join(nameservers)


def get_routing_table():
    out, _ = run_cmd('ip route')

    return out



def ping_test(ip):
    proc = subprocess.Popen(
        'fping -c 10 -p 30ms -q {}'.format(ip).split(' '),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    proc.wait()

    return proc.returncode == 0


def get_gateway_ip():
    routing_table = get_routing_table()

    gw_re = re.compile(r'^default via (\d+\.\d+\.\d+\.\d+) .*$', re.MULTILINE)
    gws = gw_re.findall(routing_table)

    if gws:
        return gws[0]
    else:
        return ''


def test_connection():
    gateway_ip = get_gateway_ip()
    gateway_connected = ping_test(gateway_ip)

    internet_connected = ping_test(INTERNET_IP)

    nameserver_connected = ping_test(INTERNET_HOSTNAME)

    return gateway_connected, internet_connected, nameserver_connected


def run():
    '''
    Main test entry point
    '''

    local_conn, internet_conn, ns_conn = test_connection()

    log('Connection status:')
    log('    Local: ', newline=False)
    if local_conn:
        log('Connected', colour=Colours.GREEN)
    else:
        log('Not connected', colour=Colours.RED)

    log('    Internet: ', newline=False)
    if internet_conn:
        log('Connected', colour=Colours.GREEN)
    else:
        log('Not connected', colour=Colours.RED)

    log('    Nameserver resolution: ', newline=False)
    if ns_conn:
        log('Working', colour=Colours.GREEN)
    else:
        log('Not working', colour=Colours.RED)

    log('\nConnection details:')
    log('    IP Address: ', newline=False)
    log(get_ip_address(), colour=Colours.GREEN)

    log('    DNS Nameservers: ', newline=False)
    log(get_dns_settings(), colour=Colours.GREEN)

    log('    Parental setting: ', newline=False)
    if get_parental_setting() == ParentalSetting.ENABLED:
        log('Enabled', colour=Colours.GREEN)
    else:
        log('Disabled', colour=Colours.GREEN)

    wless, wl_status = get_wireless_status()
    log('\nWireless details:')
    log('    ESSID: ', newline=False)
    log(wl_status['essid'], colour=Colours.GREEN)

    log('    Link Quality: ', newline=False)
    log(wl_status['quality'], colour=Colours.GREEN)

    log('    Local Transfer Rate: ', newline=False)
    log(wl_status['rate'], colour=Colours.GREEN)

    log('    Channel: ', newline=False)
    log(wl_status['channel'], colour=Colours.GREEN)

    log('    Encryption: ', newline=False)
    log(wl_status['encryption'], colour=Colours.GREEN)

    print ''
