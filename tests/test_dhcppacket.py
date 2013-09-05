#-*- coding: utf-8 -*-

import unittest

import os.path, sys
sys.path.insert(0, os.path.abspath('..'))

from isdhcplib.dhcp_packet import DhcpPacket
from isdhcplib.dhcp_constants import *
from isdhcplib.type_ipv4 import ipv4
from isdhcplib.type_strlist import strlist
from isdhcplib.type_rfc import *

dhcp_packet = [
# op / htype / hlen / hops
1,   1,   6,   1,
# xid
46,  155, 227, 41,
# secs(2) / flags(2)
0,   0,   0,   0,
# ciaddr
172, 27,  240, 5,
# yiaddr
0,   0,   0,   0,
# siaddr
0,   0,   0,   0,
# giaddr
172, 27,  240, 1,
# chaddr
0,   128, 72,  70,
98,  115, 0,   0,
# sname(64)
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
# file
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0,
0,   0,   0,   0,   0,   0,   0,   0, 
# MAGIC_COOKIE
99, 130, 83, 99,
# --- OPTIONS -------------------------------------------------------------
53, 1, 3, 
61, 7, 1, 0, 128, 72, 70, 98, 115, 
12, 12, 226, 165, 225, 226, 226, 165, 225, 226, 226, 165, 225, 226, 
81, 15, 0, 0, 0, 226, 165, 225, 226, 226, 165, 225, 226, 226, 165, 225, 226, 
60, 8, 77, 83, 70, 84, 32, 53, 46, 48, 
55, 12, 1, 15, 3, 6, 44, 46, 47, 31, 33, 121, 249, 43, 
82, 18, 1, 6, 0, 4, 7, 206, 0, 21, 2, 8, 0, 6, 132, 201, 178, 177, 222, 224, 
255
]

dhcp_packet_raw = ''.join(map(chr, dhcp_packet))
dp = DhcpPacket(dhcp_packet_raw)
print dp.IsDhcpPacket
print dp.GetOption("hlen")
print dp.GetOption("flags")
print "SET:", dp.SetOption("lpr_server", [127,0,0,1])
print dp.GetHardwareAddress()
print dp.EncodePacket()

print str(dp.CreateDhcpNackPacketFrom())
