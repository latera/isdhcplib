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

from isdhcplib.dhcp_basic_packet import *
from isdhcplib.dhcp_constants import *
from isdhcplib.type_hwmac import hwaddr


class DhcpPacket(DHCPBasicPacket):
    def __str__(self):
        # Process headers : 
        printable_data = "# --- Header fields ------------------------------------ \n"

        for field in DHCP_FIELDS:
            printable_data += "%s: " % field + repr(self.GetOption(field)) + "\n"

        printable_data += "# --- Options ------------------------------------ \n"

        for option, data in self.options_data.iteritems():
            printable_data += "%s: %s" % (option, repr(data)) + "\n"

        return printable_data
    
    # FIXME: This is called from IsDhcpSomethingPacket, but is this really
    # needed?  Or maybe this testing should be done in
    # DhcpBasicPacket.DecodePacket().

    # Test Packet Type
    def IsDhcpSomethingPacket(self, type):
        if self.IsDhcpPacket() == False:
            return False

        if self.IsOption("dhcp_message_type") == False:
            return False

        if self.GetOption("dhcp_message_type") != type:
            return False

        return True
    
    def IsDhcpDiscoverPacket(self):
        return self.IsDhcpSomethingPacket([1])

    def IsDhcpOfferPacket(self):
        return self.IsDhcpSomethingPacket([2])

    def IsDhcpRequestPacket(self):
        return self.IsDhcpSomethingPacket([3])

    def IsDhcpDeclinePacket(self):
        return self.IsDhcpSomethingPacket([4])

    def IsDhcpAckPacket(self):
        return self.IsDhcpSomethingPacket([5])

    def IsDhcpNackPacket(self):
        return self.IsDhcpSomethingPacket([6])

    def IsDhcpReleasePacket(self):
        return self.IsDhcpSomethingPacket([7])

    def IsDhcpInformPacket(self):
        return self.IsDhcpSomethingPacket([8])

    def GetMultipleOptions(self, options=()):
        result = {}
        for each in options:
            result[each] = self.GetOption(each)
        return result

    def SetMultipleOptions(self, options=None):
        options = options or {}

        for each in options.keys():
            print(each, options[each])
            self.SetOption(each, options[each])

    # Creating Response Packet

    # Server-side functions
    # From RFC 2132 page 28/29
    def CreateDhcpOfferPacket(self): # src = discover packet
        dhcp_offer = DhcpPacket(self.EncodePacket())

        for option in ("htype", "xid", "flags", "giaddr", "chaddr",
                        "ip_address_lease_time"):
            option_data = self.GetOption(option)
            print("%s = %s" % (option, option_data))
            if option_data is None:
                continue

            dhcp_offer.SetOption(option, option_data)
            
        dhcp_offer.TransformToDhcpOfferPacket()

        return dhcp_offer

    def TransformToDhcpOfferPacket(self):
        self.SetOption("dhcp_message_type", [2])
        self.SetOption("op", [2])
        self.SetOption("hlen", [6])

        self.DeleteOption("secs")
        self.DeleteOption("ciaddr")
        self.DeleteOption("request_ip_address")
        self.DeleteOption("parameter_request_list")
        self.DeleteOption("client_identifier")
        self.DeleteOption("maximum_message_size")


    """ Dhcp ACK packet creation """
    def CreateDhcpAckPacketFrom(self): # src = request or inform packet
        dhcp_ack = DhcpPacket(self.EncodePacket())
        for option in ("htype", "xid", "ciaddr", "flags", "giaddr", "chaddr",
                        "ip_address_lease_time"):
            option_data = self.GetOption(option)
            if option_data is None: continue

            dhcp_ack.SetOption(option, option_data)

        dhcp_ack.TransformToDhcpAckPacket()

        return dhcp_ack

    def CreateDhcpInformAckPacketFrom(self): # src = request or inform packet
        dhcp_inform = DhcpPacket(self.EncodePacket())
        dhcp_inform.SetOption("htype", [self.GetOption("htype")])
        dhcp_inform.SetOption("xid", self.GetOption("xid"))
        dhcp_inform.SetOption("ciaddr", self.GetOption("ciaddr"))
        dhcp_inform.SetOption("flags", self.GetOption("flags"))
        dhcp_inform.SetOption("giaddr", self.GetOption("giaddr"))
        dhcp_inform.SetOption("chaddr", self.GetOption("chaddr"))
        dhcp_inform.TransformToDhcpAckPacket()

        return dhcp_inform

    def TransformToDhcpAckPacket(self):
        # src = request or inform packet
        self.SetOption("op", [2])
        self.SetOption("hlen", [6])
        self.SetOption("dhcp_message_type", [5])

        self.DeleteOption("secs")
        self.DeleteOption("request_ip_address")
        self.DeleteOption("parameter_request_list")
        self.DeleteOption("client_identifier")
        self.DeleteOption("maximum_message_size")

    def CreateDhcpNackPacketFrom(self):
        # src = request or inform packet
        """ Dhcp NAK packet creation """
        dhcp_nak = DhcpPacket(self.EncodePacket())

        # copy fields from packet
        for option in ("htype", "xid", "flags", "giaddr", "chaddr"):
            option_data = self.GetOption(option)
            if option_data is None:
                continue

            dhcp_nak.SetOption(option, option_data)

        dhcp_nak.TransformToDhcpNackPacket()

        return dhcp_nak

    def TransformToDhcpNackPacket(self):
        self.SetOption("op", [2])
        self.SetOption("hlen", [6])
        self.DeleteOption("secs")
        self.DeleteOption("ciaddr")
        self.DeleteOption("yiaddr")
        self.DeleteOption("siaddr")
        self.DeleteOption("sname")
        self.DeleteOption("file")
        self.DeleteOption("request_ip_address")
        self.DeleteOption("ip_address_lease_time")
        self.DeleteOption("parameter_request_list")
        self.DeleteOption("client_identifier")
        self.DeleteOption("maximum_message_size")
        self.SetOption("dhcp_message_type", [6])

    """ GetClientIdentifier """

    def GetClientIdentifier(self):
        if self.IsOption("client_identifier"):
            return self.GetOption("client_identifier")

        return []

    def GetGiaddr(self):
        return self.GetOption("giaddr")

    def GetHardwareAddress(self):
        hwaddr_len = self.GetOption("hlen")[0]
        hwaddr_list = self.GetOption("chaddr")

        return hwaddr(hwaddr_list[:hwaddr_len])
