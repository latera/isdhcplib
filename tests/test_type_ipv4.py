#!/usr/bin/env python 
#-*- coding: utf-8 -*-

from isdhcplib.type_ipv4 import ipv4
import unittest

class TestIPv4(unittest.TestCase):
    orig_ip_str = "127.0.0.1"
    orig_ip_list = [127, 0, 0, 1]
    orig_ip_int  = 2130706433

    def setUp(self):
        print "TTT"
        self.ip_str = ipv4(self.orig_ip_str)
        self.ip_list = ipv4(self.orig_ip_list)
        self.ip_int = ipv4(self.orig_ip_int)

    def testIpv4Str(self):
        self.assertEqual(str(self.ip_str), self.orig_ip_str)
        self.assertEqual(list(self.ip_str), self.orig_ip_list)
        self.assertEqual(int(self.ip_str), self.orig_ip_int)

    def testExceptions(self):
        # ipv4 accepts str, list and int
        self.assertRaises(TypeError, ipv4, {"foo": "bar"})

        # test validators
        self.assertRaises(ValueError, ipv4, "foobar")    # non dotted decimal
        self.assertRaises(ValueError, ipv4, "1.1.1.1.1")    # 5 octets
        self.assertRaises(ValueError, ipv4, [444,444,444,444])  # 444 > 255
        self.assertRaises(ValueError, ipv4, [1,1,1,1,1])    # 5 octets
        self.assertRaises(ValueError, ipv4, 99999999999)    # very big int



if __name__ == "__main__":
    unittest.main()

