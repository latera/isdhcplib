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


# Check and convert ipv4 address type
class ipv4:
    def __init__(self, value="0.0.0.0") :
        self._ip_string = "0.0.0.0"
        self._ip_numlist = (0,0,0,0)
        self._ip_long = 0

        if isinstance(value, basestring):
            if not self.ValidString(value) : raise ValueError, "ipv4 string argument is not an valid ip "

            self._ip_string  = value
            self._ip_numlist = self._StringToNumlist(value) # convert to list
            self._ip_long    = self._StringToLong(value)    # convert lo int
        elif isinstance(value, (list, tuple)):
            if not self.ValidList(value) : raise ValueError, "ipv4 list argument is not an valid ip "

            self._ip_numlist = value
            self._ip_string  = self._NumlistToString(value)
            self._ip_long    = self._NumlistToLong(value)
        elif isinstance(value, (int, long)):
            if not self.ValidInteger(value) : raise ValueError, "ipv4 int argument is not an valid ip "

            self._ip_long    = value
            self._ip_string  = self._LongToString(value)
            self._ip_numlist = self._LongToNumlist(value)

        else : raise TypeError , 'ipv4 init : Valid types are str, list, int or long'

    #
    # Private conversion methods
    #

    # Convert String type ip to NumList type ip
    def _StringToNumlist(self, value):
        return map(int, value.split('.'))

    # Convert String type ip to Long type ip
    def _StringToLong(self, value):
        ip_numlist = map(int, value.split('.'))
        return self._NumlistToLong(ip_numlist)

    # Convert NumList type ip to String type ip
    def _NumlistToString(self, value) :
        return ".".join(map(str, value))

    def _NumlistToLong(self, value) :
        return reduce(lambda x, y: ( x << 8 ) + y, value, 0)

    # Convert Long type ip to str ip
    def _LongToString(self, value):
        # Convert IPv4 long integer to string
        ip_numlist = self._LongToNumlist(value)
        return self._NumlistToString(ip_numlist)

    # Convert Long type ip to numlist ip
    def _LongToNumlist(self, value):
        # Convert IPv4 long integer to list
        return [(self._ip_long >> 8 * (3 - i)) % 256 for i in xrange(4)]

    #
    # Public validators
    #

    # Check if _ip_numlist is valid and raise error if not.
    def ValidList(self, octets):
        return len([octet for octet in octets if not octet >> 8]) == 4

    # Check if _ip_numlist is valid and raise error if not.
    def ValidString(self, value):
        octets = value.strip().split('.')
        return len([octet.isdigit() for octet in octets]) == 4

    def ValidInteger(self, value):
        return not value >> 32 or False


    """ Useful function for native python operations """

    def __bool__(self):
        return bool(self._ip_long)

    def __len__(self):
        return len(self._ip_numlist)

    def __hash__(self) :
        return self._ip_long.__hash__()

    def __repr__(self) :
        return self._ip_string

    def __cmp__(self, other):
        if type(self) == type(other):
            return cmp(self._ip_long, other._ip_long)
        elif isinstance(other, (int, long)):
            return cmp(self._ip_long, other)

        raise TypeError("IPV4 can be compared with IPV4 and integers")

    def __nonzero__(self) :
        if self._ip_long != 0 : return 1
        return 0

    def __str__(self):
        return self._ip_string

    def __int__(self) :
        return self._ip_long

    def __iter__(self):
        for octet in self._ip_numlist:
            yield octet


