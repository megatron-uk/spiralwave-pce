#!/usr/bin/env python
#
# Translations tools to/from raw hex byte
# values using a translation table.
# For the PC-Engine game 'Spiral Wave'
#
# john@target-earth.net
#
import sys
import os
from config import TABLE_NAME

def parse_table(table_name):
	""" Load a CSV translation table and return a useable 
	Python list of values to loop over. """

	if os.path.isfile(table_name):
		ttable = {}
		print("parse_table(): Found translation table file [%s]" % table_name)
		f = open(table_name, "ro")
		for row in f.readlines():
			new_row = row.replace('"', '')
			columns = new_row.split(",")
			# 0 = hex code
			# 1 = unshifted symbol
			# 2 = unshifted printable yes/no
			# 3 = unshifted description
			# 4 = shifted symbol
			# 5 = shifted printable yes/no
			# 6 = shifted description
			# Only load entries we have data for...
			if (columns[1] != "") and (columns[4] != ""):
				ttable[columns[0]] = {
					"unshifted" : columns[1],
					"unshifted_printable" : columns[2],
					"shifted" : columns[4],
					"shifted_printable" : columns[5],
				}
		print("parse_table(): Loaded [%s] hex byte code translations" % len(ttable.keys()))
		return ttable
	else:
		print("parse_table(): Translation table file [%s] not found!" % table_name)
		sys.exit(1)

def bytes_to_text(bytelist, ttable):
	""" Takes a list of hex bytes - e.g. [0x30, 0x31, 0x21].
	and returns the string equivalent - e.g. '01!' """

	t = ""
	shifted = False
	shift_hex = "F9"
	for c in bytelist:
		if c in ttable.keys():
			if shifted:
				t += ttable[c]["shifted"]
				
			else:
				t += ttable[c]["unshifted"]
			if c == shift_hex:
				shifted = not(shifted)
		else:
			print("bytes_to_text(): Control code [%s] not found" % c)
			t += "<%s>" % c
	return t	

def text_to_bytes(text, ttable):
	""" Takes a string of text - e.g. '01!'
	and returns equivalent list of bytes - e.g. [0x30, 0x31, 0x21]. """

	pass

#b = ["DC", "9F", "A8", "A1", "9F", "E3"]
b = [ "FA", "53", "F9", "50", "F9", "49", "52", "41", "4C", "2E", "30", "30", "31"]
ttable = parse_table(TABLE_NAME)
t = bytes_to_text(b, ttable)
#
print t
