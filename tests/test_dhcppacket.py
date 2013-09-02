#-*- coding: utf-8 -*-

import unittest

import os.path, sys
sys.path.insert(0, os.path.abspath('..'))

from isdhcplib.dhcp_packet import DhcpPacket
from isdhcplib.dhcp_constants import *
from isdhcplib.type_ipv4 import ipv4
from isdhcplib.type_strlist import strlist
from isdhcplib.type_rfc import *

dhcp_packet = [1, 1, 6, 1, 46, 155, 227, 41, 0, 0, 0, 0, 172, 27, 240, 5, 0, 0, 0, 0, 0, 0, 0, 0, 172, 27, 240, 
1, 0, 128, 72, 70, 98, 115, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 130, 83, 99,
53, 1, 3, 
61, 7, 1, 0, 128, 72, 70, 98, 115, 
12, 12, 226, 165, 225, 226, 226, 165, 225, 226, 226, 165, 225, 226, 
81, 15, 0, 0, 0, 226, 165, 225, 226, 226, 165, 225, 226, 226, 165, 225, 226, 
60, 8, 77, 83, 70, 84, 32, 53, 46, 48, 
55, 12, 1, 15, 3, 6, 44, 46, 47, 31, 33, 121, 249, 43, 
82, 18, 1, 6, 0, 4, 7, 206, 0, 21, 2, 8, 0, 6, 132, 201, 178, 177, 222, 224, 
255]

dp = DhcpPacket()
dp.DecodePacket(''.join(map(chr, dhcp_packet)))



print dp.GetOption("giaddr")

from struct import Struct, pack, unpack
#import struct

def decoder(data, fixed_len, min_len, multiplicator):
	data_len = len(data)
	if (fixed_len and data_len == fixed_len) or (min_len <= data_len and data_len % multiplicator == 0):
		return data
	else: False


class DHCP_DECODER(object):
	def decode(self, type_spec, data, data_len):
		if type_spec not in self._type_map:
			print "No decoder for spec: %s" % type_spec

			return data[:data_len]

		decoder = self._type_map[type_spec]
		return decoder(self, data, data_len)

	def __call__(self, *args, **kwargs):
		return self.decode(*args, **kwargs)

	def validate_len(self, type_spec, data_len):
		spec = self._spec_map.get(type_spec, None)
		if not spec:
			print "No decoder for spec: %s" % type_spec
			return False

		if (spec[0] != 0 and spec == data_len) \
			or (spec[1] <= data_len and data_len % spec[2] == 0):
			return True

		return False

	def _decode_char(self, data, data_len):
		# spec: fixed_len: 1, min_len: 1, multiplicator: 0
		if len(data) == 1:
			return data[0]

		return False

	def _decode_char_plus(self, data, data_len):
		# spec: fixed_len: 0, min_len: 1, multiplicator: 1
		if len(data) >= 1:
			return data[:data_len]

		return False

	def _decode_ipv4(self, data, data_len):
		# spec: fixed_len: 4, min_len: 4, multiplicator: 0
		if len(data) == 4 and data_len == 4:
			return ipv4(data)

		return False

	def _decode_ipv4_plus(self, data, data_len):
		# spec: fixed_len: 0, min_len: 4, multiplicator: 4
		if len(data) >= 4 and data_len % 4 == 0:
			return data

		return False

	def _decode_string(self, data, data_len):
		# spec: fixed_len: 0, min_len: 1, multiplicator: 1
		if len(data) >= 1:
			return data[:data_len]

		return False

	def _decode_rfc4702(self, data, data_len):
		# spec: fixed_len: 0, min_len: 3, multiplicator: 0
		if len(data) >= 3 and data_len >= 3:
			return data[:data_len]
		return False

	def _decode_rfc3046(self, data, data_len):
		return RFC3046(data)

	def _decode_rfc3442(self, data, data_len):
		return RFC3442(data)

	_type_map = {
		"char":   _decode_char,
		"char+":  _decode_char_plus,
		"ipv4":   _decode_ipv4,
		"ipv4+":  _decode_ipv4_plus,
		"string": _decode_string,
		"RFC3046": _decode_rfc3046,
		"RFC3442": _decode_rfc3442,
		"RFC4702": _decode_rfc4702,
	}

	_spec_map = {
		"char":   [1, 1, 0],
		"char+":  [0, 0, 1],
		"ipv4":   [4, 4, 0],
		"ipv4+":  [0, 4 ,4],
		"string": [0, 0, 1],
		"RFC3046": None,
		"RFC3442": None,
		"RFC4702": [0, 3, 1],
	}


class DHCPPacket(object):
	_struct_fields = Struct(">B B B B I H H I I I I 16B 64B 128B 4B")
	_struct_option = Struct(">B B")
	_offset_options = 236
	HEAD_OPTIONS = (53, )
	TAIL_OPTIONS = (82, )

	decoder = DHCP_DECODER()

	def __init__(self, data):
		self._cache = {}

		# multimethod?
		if (not data): return False

		if isinstance(data, basestring):
			# calc data length
			data_len = len(data)

			# unpack to tuple of integers
			raw_data = unpack("!%dB" % data_len, data)

			# packet_data is header with magic cookie
			self.fields_data  = raw_data[:self._offset_options + 4]
			self.options_data = {}

			# lookup magic cookie. ideally it should be found exactly after fields.
			# but as reported some clients can make offset before magic cookie
			for offset in xrange(self._offset_options, data_len):
				if raw_data[offset:offset+4] == MAGIC_COOKIE: 
					break
			else:
				print "MAGIC COOKIE NOT FOUND:", offset
				# Raise at here?
			
			# set offset after magic cookie
			offset += 4

			while (offset < data_len):
				option_start = option_end = offset

				if raw_data[offset] == 255:
					break
				elif raw_data[offset] == 0:
					offset += 1
					continue
				else:
					# parse option header
					option, option_len = raw_data[option_start:option_start + 2]

					# calculate position of last option byte
					option_end = option_start + option_len + 2

					# get option data
					option_data = raw_data[option_start + 2:option_end]

					# update offset
					offset = option_end

					# pase option data
					name, option_type = DHCP_OPTIONS.get(option, (None, None))

					if not name or not option_type:
						print "Unknown DHCP OPTION: %s" % option
						continue

					self.options_data[name] = (option, option_type, option_len, option_data)

		else:
			pass

		print self.options_data

	def cache(func):
		def wrapper(*args, **kwargs):
			cls, option_name = args

			if option_name not in cls._cache: 
				cls._cache[option_name] = func(*args, **kwargs)

			print "CACHE:", cls._cache
			return cls._cache[option_name]
		return wrapper

	def uncache(func):
		def wrapper(*args, **kwargs):
			cls, option_name = args

			if option_name in cls._cache: 
				del cls._cache[option_name]

			return func(*args, **kwargs)
		return wrapper

	@cache
	def GetOption(self, name):
		# Requested field
		if name in DHCP_FIELDS:
			# Get option data
			pos, option_len, option_type = DHCP_FIELDS[name]
			option_data = self.fields_data[pos:pos + option_len]
		# Requested option
		elif name in self.options_data:
			# Get option data
			option_num, option_type, option_len, option_data = self.options_data[name]
		else:
			return False
		
		# Decode & return result
		return self.decoder(option_type, option_data, option_len)

	@uncache
	def DeleteOption(self, name):
		# Requested field
		if name in DHCP_FIELDS:
			# Get option data
			pos, option_len, option_type = DHCP_FIELDS[name]
			self.fields_data[pos:pos + option_len] = [0] * option_len
			return True
		# Requested option
		elif name in self.options_data:
			# Get option data
			if name in self.options_data:
				del self.options_data[name]
				return True
		else:
			return False
		
		# Decode & return result
		return False

	def SetOption(self, name, value):
		if name in DHCP_FIELDS:
			# validate value
			pos, field_len, field_type = DHCP_FIELDS[name]

			if len(value) != field_len:
				print "Wrong value=%d for field %s. Expected %d" % (len(value), name, field_len)
				return False

			self.fields_data[pos:pos + field_len] = value
			return True
		# Requested options
		elif name in DHCP_OPTION_NUM:
			# Get option data
			option_num = DHCP_OPTION_NUM[name]

			option_name, option_type = DHCP_OPTIONS[option_num]
			if self.decoder.validate_len(option_type, len(value)):
				print "LEN VALID"
				self.options_data[name] = (option_num, option_type, len(value), value)
				return True

		else:
			print "Unknown option: %s" % name
			return False



	def GetHardwareAddress(self):
		hwaddr_len = self.GetOption("hlen")
		hwaddr = self.GetOption("chaddr")
		return hwaddr[:hwaddr_len]

	@property
	def IsDhcpPacket(self):
		return self.fields_data[236:240] == MAGIC_COOKIE

	def EncodePacket(self):
		# MUST set options in order to respect the RFC (see router option)
		head_options, tail_options, options = [], [], []

		for option_name, option in self.options_data.iteritems():
			print "OPTION:",option_name,  option
			#option_num, option_type, option_len, option_data = option

			payload = [option[0], option[2]]	# type, len
			payload += option[3]				# raw value

			if option[0] in self.HEAD_OPTIONS:
				head_options += payload
			elif option[0] in self.TAIL_OPTIONS:
				tail_options += payload
			else:
				options += payload

		options = head_options + options + tail_options

		packet = list(self.fields_data[:240]) + options
		packet.append(255) # add end option

		packet_len = len(packet)

		print packet
		return pack("%dB" % packet_len, *packet)


dp = DHCPPacket(''.join(map(chr, dhcp_packet)))
print dp.IsDhcpPacket
print dp.GetOption("hlen")
print "SET:", dp.SetOption("lpr_server", [127,0,0,1])
print dp.GetHardwareAddress()
print dp.EncodePacket()

#print unpack(">BBBBIHHIIII16B64c128c", ''.join(map(chr, dhcp_packet))[:236])
