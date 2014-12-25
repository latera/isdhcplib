# isdhcplib
# Copyright (c) 2013 Alexander V. Ignatyev <ialx84@ya.ru>
# Based on pydhcplib by Mathieu Ignacio -- mignacio@april.org
#
# This file is part of isdhcplib.
# Isdhcplib is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import socket
import select

from isdhcplib.dhcp_packet import DhcpPacket
import IN


class DhcpNetwork(object):
    def __init__(self, listen_address="0.0.0.0", listen_port=67, emit_port=68):
        self.listen_port = int(listen_port)
        self.emit_port = int(emit_port)
        self.listen_address = listen_address
        self.so_reuseaddr = False
        self.so_broadcast = True
        self.dhcp_socket = None
        
    # Networking stuff
    def CreateSocket(self):
        try:
            self.dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpNetwork socket '
                             'creation error : %s' % msg)

        try:
            if self.so_broadcast:
                self.dhcp_socket.setsockopt(socket.SOL_SOCKET,
                                            socket.SO_BROADCAST, 1)
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpNetwork socket error '
                             'in setsockopt SO_BROADCAST : %s' % msg)

        try:
            if self.so_reuseaddr:
                self.dhcp_socket.setsockopt(socket.SOL_SOCKET,
                                            socket.SO_REUSEADDR, 1)
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpNetwork socket error '
                             'in setsockopt SO_REUSEADDR : %s' % msg)
        
    def EnableReuseaddr(self):
        self.so_reuseaddr = True

    def DisableReuseaddr(self):
        self.so_reuseaddr = False

    def EnableBroadcast(self):
        self.so_broadcast = True

    def DisableBroadcast(self):
        self.so_broadcast = False

    def BindToDevice(self):
        try :
            self.dhcp_socket.setsockopt(socket.SOL_SOCKET,
                                        IN.SO_BINDTODEVICE,
                                        self.listen_address + '\0')
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpNetwork.BindToDevice error '
                             'in setsockopt SO_BINDTODEVICE : %s' % msg)

        try:
            self.dhcp_socket.bind(('', self.listen_port))
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpNetwork.BindToDevice '
                             'error : %s' % msg)

    def BindToAddress(self):
        try:
            self.dhcp_socket.bind((self.listen_address, self.listen_port))
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpNetwork.BindToAddress '
                             'error : %s' % msg)

    def GetNextDhcpPacket(self, timeout=60):
        data = ""

        while data == "":
            
            data_input, data_output, data_except = select.select(
                [self.dhcp_socket], [], [], timeout)

            if data_input != []:
                data, source_address = self.dhcp_socket.recvfrom(2048)
            else:
                return None

            if data != "":
                packet = DhcpPacket()
                packet.source_address = source_address
                packet.DecodePacket(data)

                self.HandleDhcpAll(packet)
                
                if packet.IsDhcpDiscoverPacket():
                    self.HandleDhcpDiscover(packet)
                elif packet.IsDhcpRequestPacket():
                    self.HandleDhcpRequest(packet)
                elif packet.IsDhcpDeclinePacket():
                    self.HandleDhcpDecline(packet)
                elif packet.IsDhcpReleasePacket():
                    self.HandleDhcpRelease(packet)
                elif packet.IsDhcpInformPacket():
                    self.HandleDhcpInform(packet)
                elif packet.IsDhcpOfferPacket():
                    self.HandleDhcpOffer(packet)
                elif packet.IsDhcpAckPacket():
                    self.HandleDhcpAck(packet)
                elif packet.IsDhcpNackPacket():
                    self.HandleDhcpNack(packet)
                else:
                    self.HandleDhcpUnknown(packet)

                return packet

    def SendDhcpPacketTo(self, packet, _ip, _port):
        return self.dhcp_socket.sendto(packet.EncodePacket(), (_ip, _port))

    # Server side Handle methods
    def HandleDhcpDiscover(self, packet):
        pass

    def HandleDhcpRequest(self, packet):
        pass

    def HandleDhcpDecline(self, packet):
        pass

    def HandleDhcpRelease(self, packet):
        pass

    def HandleDhcpInform(self, packet):
        pass

    # client-side Handle methods
    def HandleDhcpOffer(self, packet):
        pass
        
    def HandleDhcpAck(self, packet):
        pass

    def HandleDhcpNack(self, packet):
        pass

    # Handle unknown options or all options
    def HandleDhcpUnknown(self, packet):
        pass

    def HandleDhcpAll(self, packet):
        pass


class DhcpServer(DhcpNetwork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.EnableBroadcast()
        self.DisableReuseaddr()

        self.CreateSocket()
        self.BindToAddress()


class DhcpClient(DhcpNetwork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.EnableBroadcast()
        self.EnableReuseaddr()

        self.CreateSocket()


class DhcpClientOld(DhcpNetwork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpClient socket creation '
                             'error : %s' % msg)

        try:
            self.dhcp_socket.setsockopt(socket.SOL_SOCKET,
                                        socket.SO_BROADCAST, 1)
            self.dhcp_socket.setsockopt(socket.SOL_SOCKET,
                                        socket.SO_REUSEADDR, 1)
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpClient socket error in '
                             'setsockopt SO_BROADCAST or '
                             'SO_REUSEADDR : %s' % msg)

    def BindToDevice(self):
        try:
            self.dhcp_socket.setsockopt(socket.SOL_SOCKET,
                                        IN.SO_BINDTODEVICE,
                                        self.listen_address + '\0')
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpClient socket error '
                             'in setsockopt SO_BINDTODEVICE : %s' % msg)

        try:
            self.dhcp_socket.bind(('', self.listen_port))
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpClient bind error : %s' % msg)

    def BindToAddress(self):
        try:
            self.dhcp_socket.bind((self.listen_address, self.listen_port))
        except socket.error as msg:
            sys.stderr.write( 'pydhcplib.DhcpClient bind error : %s' % msg)


class DhcpServerOld(DhcpNetwork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        try:
            self.dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpServer socket creation '
                             'error : %s' % msg)

        try:
            self.dhcp_socket.setsockopt(socket.SOL_SOCKET,
                                        socket.SO_BROADCAST, 1)
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpServer socket error '
                             'in setsockopt SO_BROADCAST : %s' % msg)

        try:
            self.dhcp_socket.bind((self.listen_address, self.listen_port))
        except socket.error as msg:
            sys.stderr.write('pydhcplib.DhcpServer bind error : %s' % msg)


