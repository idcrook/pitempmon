#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 - read internal Pi CPU temperature
   - (OPTIONALLY) log sensor data to a phant server
"""

__author__ = 'David Crook'
__copyright__ = 'Copyright 2019'
__credits__ = []
__license__ = 'MIT'
__maintainer__ = 'David Crook'
__email__ = 'idcrook@users.noreply.github.com'
__status__ = "Development"

import json
from pprint import pprint
import signal
import ssl
import sys
from time import sleep

import requests  # so can handle HTTP exceptions
from gpiozero import CPUTemperature
from phant3.Phant import Phant

# Logging sensor readings to Phant
LOGGING = True
# LOGGING = False
LOGGING_COUNT = 0

# Read in config file
with open('app_config.json') as config_file:
    config = json.loads(config_file.read())
# pprint(config)
# pprint(config["temperature_range"])
# pprint(config["durations"]["logging_interval"])

# How long to wait (in seconds) between logging measurements.
LOGGING_INTERVAL = config["durations"]["logging_interval"]

if LOGGING:
    # Read in Phant config file
    phant_json_file = 'phant-config.json'
    phant = Phant(jsonPath=phant_json_file)
    print('Logging "{0}" every {1} seconds.'.format(phant.title,
                                                    LOGGING_INTERVAL))

# create an accessor object using its defaults
cpu = CPUTemperature()


def log_error(error_type='UnknownError'):
    """Record error of passed type (string)."""
    global ERROR_TABLES
    if error_type not in ERROR_TABLES:
        ERROR_TABLES[error_type] = 1
    else:
        ERROR_TABLES[error_type] = ERROR_TABLES[error_type] + 1


def print_error_tables():
    """Print any recorded errors."""
    global ERROR_TABLES
    print(ERROR_TABLES, end=' ')
    print('number of samples {}'.format(LOGGING_COUNT))
    sys.stdout.flush()


def handler_stop_signals(signum, frame):
    print_error_tables()
    sys.exit(0)


# systemd: time_display.service: State 'stop-sigterm' timed out. Killing.
signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

print('Press Ctrl-C to quit.')
ERROR_TABLES = {}

while True:
    try:
        temp = cpu.temperature
        print('CPU temperature: {}°C - '.format(temp), end='')
        if LOGGING:
            try:
                phant.log(temp)
                print('Wrote a row to "{0}" - '.format(phant.title), end='')
                # print((phant.remaining_bytes, phant.cap))
            except ValueError as errv:
                print('-E- Error logging to {}'.format(phant.title))
                print('-W- Is phant server down?')
                print('ValueError: {}'.format(str(errv)))
                log_error(error_type='ValueError')
            except requests.exceptions.ConnectionError as errec:
                print("Error Connecting:", errec)
                print('-W- Is network down?')
                log_error(error_type='ConnectionError')
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
                log_error(error_type='Timeout')
            LOGGING_COUNT = LOGGING_COUNT + 1
            print('log count {0}'.format(LOGGING_COUNT))

    except KeyboardInterrupt:
        log_error(error_type='KeyboardInterrupt')
        print_error_tables()
        sys.exit(0)

    except ssl.SSLError:
        # we had a network issue, try again later
        log_error(error_type='ssl.SSLError')
        print_error_tables()

    finally:
        print_error_tables()
        # pause here
        sleep(LOGGING_INTERVAL)
