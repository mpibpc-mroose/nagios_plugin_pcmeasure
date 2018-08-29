#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import re
import socket
import sys

NAGIOS_OK = 0
NAGIOS_WARNING = 1
NAGIOS_CRITICAL = 2
NAGIOS_UNKNOWN = 3


class MessPCCheck(object):
    def __init__(self, host, port=4000):
        self.host = host
        self.port = port
        self.socket = self.connect()

    def connect(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(0.5)
        _socket.connect((self.host, self.port))
        return _socket

    def __delete__(self, instance):
        self.socket.close()

    def _get_value(self, sensor_name: bytes) -> float:
        self.socket.send(
            b'pcmeasure.' + sensor_name + b'\n'
        )
        raw_data = self.socket.recv(2096).decode()
        sensor_reply_pattern = re.compile(r"value=\s(?P<value>.+);")
        return float(sensor_reply_pattern.findall(raw_data)[0])

    def check(self, sensor_name: bytes, warning_threshold: float, critical_threshold: float) -> int:
        try:
            value = self._get_value(sensor_name=sensor_name)
            if value > critical_threshold:
                print("CRITICAL: {value} exceeds {threshold}".format(
                    value=value,
                    threshold=critical_threshold
                ))
                return NAGIOS_CRITICAL
            elif value > warning_threshold:
                print("WARNING: {value} exceeds {threshold}".format(
                    value=value,
                    threshold=warning_threshold
                ))
                return NAGIOS_WARNING
            else:
                print("OK: {value}".format(
                    value=value
                ))
                return NAGIOS_OK
        except Exception as error:
            print("UNKNOWN: " + str(error))
            return NAGIOS_UNKNOWN


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    """
    check_pcmeasure2.pl -H <host> -S <sensor>[,<sensor] [-p <port>] 
   [-w <threshold>] [-c <threshold>]
    """
    parser.add_argument(
        "-H",
        dest="host",
        type=str,
        required=True,
        help="hostname of the MessPC unit"
    )
    parser.add_argument(
        "-p",
        type=int,
        dest="port",
        default=4000,
        required=False,
        help="port to use for communication"
    )
    parser.add_argument(
        "-S",
        dest="sensor_name",
        type=str,
        required=True,
        help="sensor name, e.g. com1.1"
    )
    parser.add_argument(
        "-w",
        dest="warning_threshold",
        type=float,
        required=True,
        help="warning threshold"
    )
    parser.add_argument(
        "-c",
        dest="critical_threshold",
        type=float,
        required=True,
        help="critical threshold"
    )
    arguments = parser.parse_args()

    if arguments.warning_threshold > arguments.critical_threshold:
        print("UNKNOWN: warning threshold should be lower than critical threshold")
        sys.exit(NAGIOS_UNKNOWN)

    try:
        mess_pc = MessPCCheck(
            host=arguments.host, port=arguments.port
        )
    except TimeoutError:
        print(
            "CRITICAL: timeout on connect to {host}:{port}".format(
                host=arguments.host,
                port=arguments.port
            ))
        sys.exit(NAGIOS_CRITICAL)

    return_code = mess_pc.check(
        sensor_name=arguments.sensor_name.encode(),
        warning_threshold=arguments.warning_threshold,
        critical_threshold=arguments.critical_threshold
    )
    sys.exit(return_code)
