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

import operator
from struct import unpack
from struct import pack
from dhcp_basic_packet import *
from dhcp_constants import *
from type_ipv4 import ipv4
from type_strlist import strlist
from type_hwmac import hwmac
import sys
from collections    import Iterable

class DhcpPacket(DhcpBasicPacket):
    def str(self):
        # Process headers : 
        printable_data = "# Header fields\n"

        op = self.packet_data[DhcpFields['op'][0]:DhcpFields['op'][0]+DhcpFields['op'][1]]
        printable_data += "op : " + DhcpFieldsName['op'][str(op[0])] + "\n"

        
        for opt in  ['htype','hlen','hops','xid','secs','flags',
                     'ciaddr','yiaddr','siaddr','giaddr','chaddr','sname','file'] :
            begin = DhcpFields[opt][0]
            end = DhcpFields[opt][0]+DhcpFields[opt][1]
            data = self.packet_data[begin:end]
            result = ''
            if DhcpFieldsTypes[opt] == "int" : result = str(data[0])
            elif DhcpFieldsTypes[opt] == "int2" : result = str(data[0]*256+data[1])
            elif DhcpFieldsTypes[opt] == "int4" : result = str(ipv4(data).int())
            elif DhcpFieldsTypes[opt] == "str" :
                for each in data :
                    if each != 0 : result += chr(each)
                    else : break

            elif DhcpFieldsTypes[opt] == "ipv4" : result = ipv4(data).str()
            elif DhcpFieldsTypes[opt] == "hwmac" :
                result = []
                hexsym = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
                for iterator in range(6) :
                    result += [str(hexsym[data[iterator]/16]+hexsym[data[iterator]%16])]

                result = ':'.join(result)

            printable_data += opt+" : "+result  + "\n"

        # Process options : 
        printable_data += "# Options fields\n"

        for opt in self.options_data.keys():
            data = self.options_data[opt]
            result = ""
            optnum  = DhcpOptions[opt]
            if opt=='dhcp_message_type' : result = DhcpFieldsName['dhcp_message_type'][str(data[0])]
            elif DhcpOptionsTypes[optnum] == "char" : result = str(data[0])
            elif DhcpOptionsTypes[optnum] == "16-bits" : result = str(data[0]*256+data[0])
            elif DhcpOptionsTypes[optnum] == "32-bits" : result = str(ipv4(data).int())
            elif DhcpOptionsTypes[optnum] == "string" :
                for each in data :
                    if each != 0 : result += chr(each)
                    else : break
        
            elif DhcpOptionsTypes[optnum] == "ipv4" : result = ipv4(data).str()
            elif DhcpOptionsTypes[optnum] == "ipv4+" :
                for i in range(0,len(data),4) :
                    if len(data[i:i+4]) == 4 :
                        result += ipv4(data[i:i+4]).str() + " - "
            elif DhcpOptionsTypes[optnum] == "char+" :
                if optnum == 55 : # parameter_request_list
                    result = ','.join([DhcpOptionsList[each] for each in data])
                else : result += str(data)
                
            printable_data += opt + " : " + result + "\n"

        return printable_data

    def AddLine(self,_string) :
        (parameter,junk,value) = _string.partition(':')
        parameter = parameter.strip()
        # If value begin with a whitespace, remove it, leave others
        if len(value)>0 and value[0] == ' ' : value = value[1:]
        value = self._OptionsToBinary(parameter,value)
        if value : self.SetOption(parameter,value)

    def _OptionsToBinary(self,parameter,value) :
        # Transform textual data into dhcp binary data

        p = parameter.strip()
        # 1- Search for header informations or specific parameter
        if p == 'op' or p == 'htype' :
            value = value.strip()
            if value.isdigit() : return [int(value)]
            try :
                value = DhcpNames[value.strip()]
                return [value]
            except KeyError :
                return [0]

        elif p == 'hlen' or p == 'hops' :
            try :
                value = int(value)
                return [value]
            except ValueError :
                return [0]

        elif p == 'secs' or p == 'flags' :
            try :
                value = ipv4(int(value)).list()
            except ValueError :
                value = [0,0,0,0]

            return value[2:]

        elif p == 'xid' :
            try :
                value = ipv4(int(value)).list()
            except ValueError :
                value = [0,0,0,0]
            return value

        elif p == 'ciaddr' or p == 'yiaddr' or p == 'siaddr' or p == 'giaddr' :
            try :
                ip = ipv4(value).list()
            except ValueError :
                ip = [0,0,0,0]
            return ip
        
        elif p == 'chaddr' :
            try:
                value = hwmac(value).list()+[0]*10
            except ValueError,TypeError :
                value = [0]*16
            return value
            
        elif p == 'sname' :
            return
        elif p == 'file' :
            return
        elif p == 'parameter_request_list' :
            value = value.strip().split(',')
            tmp = []
            for each in value:
                if DhcpOptions.has_key(each) : tmp.append(DhcpOptions[each])
            return tmp
        elif  p=='dhcp_message_type' :
            try :
                return [DhcpNames[value]]
            except KeyError:
                return

        # 2- Search for options
        try : option_type = DhcpOptionsTypes[DhcpOptions[parameter]]
        except KeyError : return False

        if option_type == "ipv4" :
            # this is a single ip address
            try :
                binary_value = map(int,value.split("."))
            except ValueError : return False
            
        elif option_type == "ipv4+" :
            # this is multiple ip address
            iplist = value.split(",")
            opt = []
            for single in iplist :
                opt += (ipv4(single).list())
            binary_value = opt

        elif option_type == "32-bits" :
            # This is probably a number...
            try :
                digit = int(value)
                binary_value = [digit>>24&0xFF,(digit>>16)&0xFF,(digit>>8)&0xFF,digit&0xFF]
            except ValueError :
                return False

        elif option_type == "16-bits" :
            try :
                digit = int(value)
                binary_value = [(digit>>8)&0xFF,digit&0xFF]
            except ValueError : return False


        elif option_type == "char" :
            try :
                digit = int(value)
                binary_value = [digit&0xFF]
            except ValueError : return False

        elif option_type == "bool" :
            if value=="False" or value=="false" or value==0 :
                binary_value = [0]
            else : binary_value = [1]
            
        elif option_type == "string" :
            binary_value = strlist(value).list()

        else :
            binary_value = strlist(value).list()
        
        return binary_value
    
    # FIXME: This is called from IsDhcpSomethingPacket, but is this really
    # needed?  Or maybe this testing should be done in
    # DhcpBasicPacket.DecodePacket().

    # Test Packet Type
    def IsDhcpSomethingPacket(self,type):
        if self.IsDhcpPacket() == False : return False
        if self.IsOption("dhcp_message_type") == False : return False
        if self.GetOption("dhcp_message_type") != type : return False
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


    def GetMultipleOptions(self,options=()):
        result = {}
        for each in options:
            result[each] = self.GetOption(each)
        return result

    def SetMultipleOptions(self,options={}):
        for each in options.keys():
            self.SetOption(each,options[each])






    # Creating Response Packet

    # Server-side functions
    # From RFC 2132 page 28/29
    def CreateDhcpOfferPacketFrom(self,src): # src = discover packet
        self.SetOption("htype",src.GetOption("htype"))
        self.SetOption("xid",src.GetOption("xid"))
        self.SetOption("flags",src.GetOption("flags"))
        self.SetOption("giaddr",src.GetOption("giaddr"))
        self.SetOption("chaddr",src.GetOption("chaddr"))
        self.SetOption("ip_address_lease_time",src.GetOption("ip_address_lease_time"))
        self.TransformToDhcpOfferPacket()

    def TransformToDhcpOfferPacket(self):
        self.SetOption("dhcp_message_type",[2])
        self.SetOption("op",[2])
        self.SetOption("hlen",[6]) 

        self.DeleteOption("secs")
        self.DeleteOption("ciaddr")
        self.DeleteOption("request_ip_address")
        self.DeleteOption("parameter_request_list")
        self.DeleteOption("client_identifier")
        self.DeleteOption("maximum_message_size")





    """ Dhcp ACK packet creation """
    def CreateDhcpAckPacketFrom(self,src): # src = request or inform packet
        self.SetOption("htype",src.GetOption("htype"))
        self.SetOption("xid",src.GetOption("xid"))
        self.SetOption("ciaddr",src.GetOption("ciaddr"))
        self.SetOption("flags",src.GetOption("flags"))
        self.SetOption("giaddr",src.GetOption("giaddr"))
        self.SetOption("chaddr",src.GetOption("chaddr"))
        self.SetOption("ip_address_lease_time",src.GetOption("ip_address_lease_time"))
        self.TransformToDhcpAckPacket()

    def CreateDhcpInformAckPacketFrom(self,src): # src = request or inform packet
        self.SetOption("htype",src.GetOption("htype"))
        self.SetOption("xid",src.GetOption("xid"))
        self.SetOption("ciaddr",src.GetOption("ciaddr"))
        self.SetOption("flags",src.GetOption("flags"))
        self.SetOption("giaddr",src.GetOption("giaddr"))
        self.SetOption("chaddr",src.GetOption("chaddr"))
        self.TransformToDhcpAckPacket()

    def TransformToDhcpAckPacket(self): # src = request or inform packet
        self.SetOption("op",[2])
        self.SetOption("hlen",[6]) 
        self.SetOption("dhcp_message_type",[5])

        self.DeleteOption("secs")
        self.DeleteOption("request_ip_address")
        self.DeleteOption("parameter_request_list")
        self.DeleteOption("client_identifier")
        self.DeleteOption("maximum_message_size")


    """ Dhcp NACK packet creation """
    def CreateDhcpNackPacketFrom(self,src): # src = request or inform packet
        
        self.SetOption("htype",src.GetOption("htype"))
        self.SetOption("xid",src.GetOption("xid"))
        self.SetOption("flags",src.GetOption("flags"))
        self.SetOption("giaddr",src.GetOption("giaddr"))
        self.SetOption("chaddr",src.GetOption("chaddr"))
        self.TransformToDhcpNackPacket()

    def TransformToDhcpNackPacket(self):
        self.SetOption("op",[2])
        self.SetOption("hlen",[6]) 
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
        self.SetOption("dhcp_message_type",[6])







    """ GetClientIdentifier """

    def GetClientIdentifier(self) :
        if self.IsOption("client_identifier") :
            return self.GetOption("client_identifier")
        return []

    def GetGiaddr(self) :
        return self.GetOption("giaddr")

    def GetHardwareAddress(self) :
        length = self.GetOption("hlen")[0]
        full_hw = self.GetOption("chaddr")
        if length!=[] and length<len(full_hw) : return full_hw[0:length]
        return full_hw







    """ Helper functions for oneliners """
    def ip_to_int(self, ip):
        return reduce(lambda x, y: ( x << 8 ) + y, ip, 0)

    # Make alias for MAC 2 Int func. They are same
    mac_to_int = ip_to_int

    def int_to_mac(self, val):
        return [(val >> 8 * (5 - i)) % 256 for i in xrange(6)]

    def int_to_ip(self, val):
        return [(val >> 8 * (3 - i)) % 256 for i in xrange(4)]

    def ip_to_str(self, ip):
        if isinstance(ip, (int, long)):
            ip = int_to_ip(ip)

        return '.'.join(['%d' %c for c in ip]) if isinstance(ip, Iterable) else None

    def mac_to_str(self, hwaddr):
        if isinstance(hwaddr, (int, long)):
            hwaddr = int_to_mac(hwaddr)

        return ':'.join(['%02x' %c for c in hwaddr]) if isinstance(hwaddr, Iterable) else None


    # Oneliners

    # CHADDR
    @property
    def chaddr(self):
        return self.mac_to_int(self.GetHardwareAddress())

    @property
    def chaddr_str(self):
        return self.mac_to_str(self.GetHardwareAddress())

    # GIADDR
    @property
    def giaddr(self):
        return self.ip_to_int(self.GetOption('giaddr'))

    @property
    def giaddr_str(self):
        return self.ip_to_str(self.GetOption('giaddr'))

    # CIADDR
    @property
    def ciaddr(self):
        return self.ip_to_int(self.GetOption('ciaddr'))

    @property
    def ciaddr_str(self):
        return self.ip_to_str(self.GetOption('ciaddr'))

    # SIADDR
    @property
    def siaddr(self):
        return self.ip_to_int(self.GetOption('siaddr'))

    @property
    def siaddr_str(self):
        return self.ip_to_str(self.GetOption('siaddr'))

    # server_identifier
    @property
    def server_identifier(self):
        return self.ip_to_int(self.GetOption('server_identifier'))

    @property
    def server_identifier_str(self):
        return self.ip_to_str(self.GetOption('server_identifier'))


    # request_ip_address
    @property
    def request_ip_address(self):
        return self.ip_to_int(self.GetOption('request_ip_address'))

    @property
    def request_ip_address_str(self):
        return self.ip_to_str(self.GetOption('request_ip_address'))

    # HOSTNAME
    @property
    def host_name(self):
        return ''.join([chr(c) for c in self.GetOption('host_name') if c != 0]).decode("cp866")

    # parameter_request_list
    @property
    def parameter_request_list(self):
        return self.GetOption('parameter_request_list')

    # relay_agent
    @property
    def relay_agent(self):
        return self.GetOption('relay_agent')

    @property
    def flag_broadcast(self):
        return 128 in self.GetOption('flags')

