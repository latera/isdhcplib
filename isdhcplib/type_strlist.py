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

class strlist:
    def __init__(self, value=""):
        self._str = ""
        self._numeric_list = []
        
        if isinstance(value, basestring):
            self._str          = value
            self._numeric_list = self._StringToNumericList(value)
        elif isinstance(value, (list, tuple)):
            if not self.ValidNumericList(value): raise TypeError("List can't be converted to string")

            self._numeric_list = value
            self._str = self._NumericListToString(value)
        else : raise TypeError , 'strlist init : Valid types are str and  list of int'

    #
    # Private converters
    #
    def _StringToNumericList(self, value):
        return map(ord, value)
    
    def _NumericListToString(self, value):
        return "".join(map(chr, value))
    #
    # Public validators
    #
    def ValidNumericList(self, value):
        return len([byte for byte in value if type(byte) == int]) > 0


    """ Useful function for native python operations """

    def __hash__(self) :
        return self._str.__hash__()

    def __repr__(self) :
        return self._str

    def __nonzero__(self) :
        if self._str != "" : return 1
        return 0

    def __cmp__(self,other) :
        if self._str == other : return 0
        return 1

    # return string
    def __str__(self):
        return self._str

    # return list (useful for DhcpPacket class)
    def __iter__(self):
        for byte in self._numeric_list:
            yield byte

    # return int
    # TODO: FIXME
    def __int__(self):
        return 0
