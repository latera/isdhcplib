#!/usr/bin/env python 
#-*- coding: utf-8 -*-

from isdhcplib.type_ipv4 import ipv4
from isdhcplib.type_strlist import strlist
import unittest

class TestIPv4(unittest.TestCase):
    orig_ip_str = "127.0.0.1"
    orig_ip_list = [127, 0, 0, 1]
    orig_ip_int  = 2130706433

    def setUp(self):
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
        self.assertRaises(ValueError, ipv4, "foobar")       # non dotted decimal
        self.assertRaises(ValueError, ipv4, "1.1.1.1.1")    # 5 octets
        self.assertRaises(ValueError, ipv4, [444,444,444,444])  # 444 > 255
        self.assertRaises(ValueError, ipv4, [1,1,1,1,1])    # 5 octets
        self.assertRaises(ValueError, ipv4, 99999999999)    # very big int


class TestStrlist(unittest.TestCase):
    orig_string = "test"
    orig_list   = [116, 101 , 115, 116]

    def setUp(self):
        self.strlist_str  = strlist(orig_string)
        self.strlist_list = strlist(orig_list)

    def testStrlist(self):
        self.assertEqual(str(self.strlist_list), self.orig_string)
        self.assertEqual(list(self.strlist_str), self.orig_list)

    def testExceptions(self):
        self.assertRaises(TypeError, strlist, {"foo": "bar"})   # valid only lists
        self.assertRaises(TypeError, strlist, ["foo", "bar", 1, 2, 3])  # list items should be int


if __name__ == "__main__":
    unittest.main()
