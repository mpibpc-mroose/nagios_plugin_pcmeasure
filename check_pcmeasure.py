#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import socket
import sys
import textwrap
import time


STATUS_OK = 0
STATUS_WARNING = 1
STATUS_CRITICAL = 2
STATUS_UNKNOWN = 3


class CheckPcMeasure(object):
    def __init__(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent("check_pcmeasure.py 0.1.0 (GPLv3) 2018 - " +
                                                                     time.strftime("%Y")),
                                         epilog=textwrap.dedent("GitHub: https://github.com/mpibpc-mroose/"
                                                                "nagios_plugin_pcmeasure"))
        parser.add_argument("-H", dest="host", type=str, required=True, help="hostname of the MessPC unit")
        parser.add_argument("-p", type=int, dest="port", default=4000, required=False, help="port to use")
        parser.add_argument("-S", dest="sensor_name", type=str, required=True, help="sensor name, e.g. com1.1")
        parser.add_argument("-w", dest="warning_threshold", type=float, required=True, help="warning threshold")
        parser.add_argument("-c", dest="critical_threshold", type=float, required=True, help="critical threshold")
        parser.add_argument("-l", dest="label", type=str, required=False, help="label for perfdata, e.g. Celsius")
        self.arguments = parser.parse_args()

        if self.arguments.warning_threshold > self.arguments.critical_threshold:
            print("UNKNOWN: warning threshold should be lower than critical threshold")
            sys.exit(STATUS_UNKNOWN)

        try:
            self.socket = self._connect()
        except TimeoutError:
            print("CRITICAL: timeout on connect to {host}:{port}".format(host=self.arguments.host,
                                                                         port=self.arguments.port))
            sys.exit(STATUS_CRITICAL)

    def _connect(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(0.5)
        _socket.connect((self.arguments.host, self.arguments.port))
        return _socket

    def __delete__(self, instance):
        self.socket.close()

    def _get_value(self, sensor_name: bytes) -> float:
        self.socket.send(b'pcmeasure.' + bytes(sensor_name, 'utf-8') + b'\n')
        raw_data = self.socket.recv(2096).decode()
        sensor_reply_pattern = re.compile(r"value=\s(?P<value>.+);")
        return float(sensor_reply_pattern.findall(raw_data)[0])

    def check(self):
        try:
            value = self._get_value(sensor_name=self.arguments.sensor_name)
            if value > self.arguments.critical_threshold:
                print("CRITICAL: {value} exceeds {threshold}".format(value=value,
                                                                     threshold=self.arguments.critical_threshold))
                sys.exit(STATUS_CRITICAL)
            elif value > self.arguments.warning_threshold:
                print("WARNING: {value} exceeds {threshold}".format(value=value,
                                                                    threshold=self.arguments.warning_threshold))
                sys.exit(STATUS_WARNING)
            else:
                if self.arguments.label:
                    print("OK: {value} | {label} {value}".format(value=value,
                                                                 label=self.arguments.label))
                else:
                    print("OK: {value}".format(value=value))
                sys.exit(STATUS_OK)
        except UnicodeDecodeError:
            print("UNKNOWN: can not read from sensor '{sensor_name}'! "
                  "use {app_name} -h for further information".format(sensor_name=self.arguments.sensor_name,
                                                                     app_name=os.path.basename(__file__)))
            sys.exit(STATUS_UNKNOWN)
        except Exception as error:
            print("UNKNOWN: " + str(error))
            sys.exit(STATUS_UNKNOWN)


if __name__ == '__main__':
    check_pcmeasure = CheckPcMeasure()
    check_pcmeasure.check()

