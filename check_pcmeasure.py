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
        version = "0.2.0"
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent(os.path.basename(__file__) + " " + version +
                                                                     " (GPLv3) 2018 - " + time.strftime("%Y")),
                                         epilog=textwrap.dedent("GitHub: https://github.com/mpibpc-mroose/"
                                                                "nagios_plugin_pcmeasure"))
        parser.add_argument("-H", dest="host", type=str, required=True, help="hostname of the etherbox")
        parser.add_argument("-p", type=int, dest="port", default=4000, required=False, help="port to use")
        parser.add_argument("-S", dest="sensor_name", type=str, required=True, help="sensor name, e.g. com1.1")
        parser.add_argument("-w", dest="warning_threshold", type=float, required=True, help="warning threshold")
        parser.add_argument("-c", dest="critical_threshold", type=float, required=True, help="critical threshold")
        parser.add_argument("-l", dest="label", type=str, required=False, help="label for perfdata, e.g. 'celsius'")
        self.arguments = parser.parse_args()

        if self.arguments.label:
            self.label_perfdata = self.arguments.label
            self.arguments.label = " " + self.arguments.label
        else:
            self.label_perfdata = "sensor_output"
            self.arguments.label = ""

        if self.arguments.warning_threshold > self.arguments.critical_threshold:
            print("UNKNOWN: warning threshold should be lower than critical threshold")
            sys.exit(STATUS_UNKNOWN)

        self.socket = self._connect()

    def _connect(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(0.5)
        try:
            _socket.connect((self.arguments.host, self.arguments.port))
        except socket.timeout:
            print("UNKNOWN: timeout on connect to {host}:{port}".format(host=self.arguments.host,
                                                                        port=self.arguments.port))
            sys.exit(STATUS_UNKNOWN)
        return _socket

    def __delete__(self, instance):
        self.socket.close()

    def _get_value(self, sensor_name) -> float:
        self.socket.send(b'pcmeasure.' + bytes(sensor_name, 'utf-8') + b'\n')
        raw_data = self.socket.recv(2096).decode()
        sensor_reply_pattern = re.compile(r"value=\s(?P<value>.+);")
        return float(sensor_reply_pattern.findall(raw_data)[0])

    def check(self):
        try:
            value = self._get_value(sensor_name=self.arguments.sensor_name)
            if value > self.arguments.critical_threshold:
                print("CRITICAL: {value} exceeds {threshold} | "
                      "{label_perfdata}={value};;;0".format(value=value,
                                                            label=self.arguments.label,
                                                            label_perfdata=self.label_perfdata,
                                                            threshold=self.arguments.critical_threshold))
                sys.exit(STATUS_CRITICAL)
            elif value > self.arguments.warning_threshold:
                print("WARNING: {value} exceeds {threshold} | "
                      "{label_perfdata}={value};;;0".format(value=value,
                                                            label=self.arguments.label,
                                                            label_perfdata=self.label_perfdata,
                                                            threshold=self.arguments.warning_threshold))
                sys.exit(STATUS_WARNING)
            else:
                print("OK: {value}{label} | {label_perfdata}={value};;;0".format(value=value,
                                                                                 label_perfdata=self.label_perfdata,
                                                                                 label=self.arguments.label))
                sys.exit(STATUS_OK)
        except UnicodeDecodeError:
            print("UNKNOWN: can not read from sensor '{sensor_name}'! "
                  "use {app_name} -h for further information!".format(sensor_name=self.arguments.sensor_name,
                                                                      app_name=os.path.basename(__file__)))
            sys.exit(STATUS_UNKNOWN)
        except Exception as error:
            print("UNKNOWN: " + str(error))
            sys.exit(STATUS_UNKNOWN)


if __name__ == '__main__':
    check_pcmeasure = CheckPcMeasure()
    check_pcmeasure.check()
