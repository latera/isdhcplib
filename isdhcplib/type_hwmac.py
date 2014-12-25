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

from functools import reduce


class hwaddr(object):
    def __init__(self, value="00:00:00:00:00:00"):
        self._hw_numlist = []
        self._hw_string = ""
        self._hw_long = 0

        if isinstance(value, str):
            if not self.ValidString(value):
                raise ValueError("Wrong string for HWADDR")

            self._hw_string = value
            self._hw_numlist = self._StringToNumlist(value)
            self._hw_long = self._NumlistToLong(self._hw_numlist)
        elif isinstance(value, (list, tuple)):
            if not self.ValidNumlist(value):
                raise ValueError("Wrong list for HWADDR")

            self._hw_numlist = value
            self._hw_string = self._NumlistToString(value)
            self._hw_long = self._NumlistToLong(value)
        elif isinstance(value, int):
            if not self.ValidLong(value):
                raise ValueError("Wrong interger for HWADDR")

            self._hw_long = value
            self._hw_numlist = self._LongToNumlist(value)
            self._hw_strling = self._NumlistToString(self._hw_numlist)
        else:
            raise TypeError('Valid types for HWADDR are str, list or int')

    #
    # Private converters
    #

    def _StringToNumlist(self, value):
        # Normalize string value
        hex_list = value.split(":")

        return [int(octet, 16) for octet in hex_list]

    # Convert NumList type ip to String type ip
    def _NumlistToString(self, value):
        return ":".join(['%x' % octet for octet in value])

    def _NumlistToLong(self, value):
        return reduce(lambda x, y: (x << 8) + y, value, 0)

    def _LongToNumlist(self, value):
        return [(value >> 8 * (5 - i)) % 256 for i in range(6)]
    #
    # Public validators
    #

    def ValidString(self, value):
        octets = value.split(":")
        return len(octets) == 6

    def ValidNumlist(self, value):
        return len([octet
                    for octet in value
                    if type(octet) == int and not octet >> 8]) == 6

    def ValidLong(self, value):
        return not value >> 48 or False

    # Convert String type ip to NumList type ip
    def __str__(self):
        return self._hw_string

    def __int__(self):
        return self._hw_long

    # return ip list (useful for DhcpPacket class)
    def __iter__(self):
        for octet in self._hw_numlist:
            yield octet

    def __hash__(self):
        return self._hw_long

    def __repr__(self):
        return "<%s / %s>" % (self.__class__, self._hw_string)

    def __cmp__(self, other):
        if isinstance(other, int):
            return (self.__int__() > other) - (self.__int__() < other)

        if self._hw_string == other:
            return 0
        return 1

    def __nonzero__(self):
        if self._hw_string != "00:00:00:00:00:00":
            return 1

        return 0


