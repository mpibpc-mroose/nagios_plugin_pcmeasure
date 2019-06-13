#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver
import threading
import unittest


from unittest import TestCase
from check_pcmeasure import CheckPcMeasure, STATUS_OK, STATUS_WARNING, STATUS_CRITICAL


class AlwaysReturnTwentyOneDotSevenRequestHandler(socketserver.BaseRequestHandler):
    """ Handler which always returns 21.7 as value"""

    def handle(self):
        self.data = self.request.recv(2096).strip()
        print("{client_ip} wrote: {data}".format(client_ip=self.client_address[0],
                                                 data=self.data))
        self.request.sendall('valid=1;value= {expected_value};\n'.format(expected_value=21.7).encode())


class TestServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class MessPCCheckTestCase(TestCase):
    host = "127.0.0.1"
    port = 4711
    server = None

    def start_server(self):
        self.server = TestServer((self.host, self.port), AlwaysReturnTwentyOneDotSevenRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        self.server_thread.start()

    def setUp(self):
        self.start_server()
        self.mess_pc_check = CheckPcMeasure(host=self.host, port=self.port)

    def tearDown(self):
        self.stop_server()
        self.mess_pc_check.close()
        del self.mess_pc_check

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()

    def test_01_get_value(self):
        value = self.mess_pc_check._get_value("com1.1")
        self.assertEqual(value, 21.7)

    def threshold_test(self, parameters):
        try:
            label = parameters["label"]
        except KeyError:
            label = False
        result = self.mess_pc_check.check(sensor_name="com1.1",
                                          warning_threshold=parameters["warning"],
                                          critical_threshold=parameters["critical"],
                                          label=label)
        self.assertEqual(result, parameters["expected"])

    def test_02_check_no_thresholds_exceeded(self):
        self.threshold_test({"warning": 22.0, "critical": 23.0, "expected": STATUS_OK})

    def test_03_check_warning_threshold_exceeded(self):
        self.threshold_test({"warning": 21.5, "critical": 23.0, "expected": STATUS_WARNING})

    def test_04_check_critical_threshold_exceeded(self):
        self.threshold_test({"warning": 20.0, "critical": 21.0, "expected": STATUS_CRITICAL})

    def test_05_check_no_thresholds_exceeded_with_label(self):
        self.threshold_test({"warning": 22.0, "critical": 23.0, "expected": STATUS_OK, "label": "celsius"})

    def test_06_check_warning_threshold_exceeded_with_label(self):
        self.threshold_test({"warning": 21.5, "critical": 23.0, "expected": STATUS_WARNING, "label": "celsius"})

    def test_07_check_critical_threshold_exceeded_with_label(self):
        self.threshold_test({"warning": 20.0, "critical": 21.0, "expected": STATUS_CRITICAL, "label": "celsius"})

if __name__ == '__main__':
    unittest.main()