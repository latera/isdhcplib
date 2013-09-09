#!/usr/bin/env python 
#-*- coding: utf-8 -*-

from isdhcplib.type_ipv4 import ipv4
from isdhcplib.type_strlist import strlist
from isdhcplib.type_rfc import RFC3046
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
        self.strlist_str  = strlist(self.orig_string)
        self.strlist_list = strlist(self.orig_list)

    def testStrlist(self):
        self.assertEqual(str(self.strlist_list), self.orig_string)
        self.assertEqual(list(self.strlist_str), self.orig_list)

    def testExceptions(self):
        self.assertRaises(TypeError, strlist, {"foo": "bar"})   # valid only lists
        self.assertRaises(TypeError, strlist, ["foo", "bar", 1, 2, 3])  # list items should be int

class TestRFC3046(unittest.TestCase):
    exp_ci_vlan = 1998
    exp_ci_port = 21
    exp_ri_mac  = [17, 34, 51, 68, 85, 102]
    exp_list    = [1, 6, 0, 4, 7, 206, 0, 21, 2, 8, 0, 6, 17, 34, 51, 68, 85, 102]

    def setUp(self):
        self.rfc3046 = RFC3046(self.exp_list)

    def testRFC3046(self):
        vlan, module, port = self.rfc3046.AgentCircuitId
        mac = self.rfc3046.AgentRemoteId

        self.assertEqual(vlan, self.exp_ci_vlan)
        self.assertEqual(port, self.exp_ci_port)
        self.assertEqual(mac, self.exp_ri_mac)


if __name__ == "__main__":
    unittest.main()

