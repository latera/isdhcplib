#!/usr/bin/python

from isdhcplib.dhcp_packet import DhcpPacket
from isdhcplib.type_strlist import strlist
from isdhcplib.type_ipv4 import ipv4


packet = DhcpPacket()

packet.SetOption("op", [1])
packet.SetOption("domain_name", list(strlist("anemon.org")))
packet.SetOption("router", list(ipv4("192.168.0.1")) + [6, 4, 2, 1])
packet.SetOption("time_server", [100, 100, 100, 7, 6, 4, 2, 1])
packet.SetOption("yiaddr", [192, 168, 0, 18])

print(packet)
