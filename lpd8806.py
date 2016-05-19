#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

class LPD8806:

	spidev = "/dev/spidev0.0"

	def __init__(self,nLeds):

		self.nLeds = nLeds
		self.reset()

	def reset(self):
		data = [0x00]					# Set ledstrip in "data-accept" mode
		for i in range(0,self.nLeds):
			data += [0x80,0x80,0x80]	# Set G,R,B with each MSB set high
										# (representing a color byte)
										# and remaining bits to 0
										# (the intensity bits)
										# resulting in a blank led

		data += [0x00]					# Already set ledstrip in "data-accept" mode + final latch
										# to speed-up next data push

		self.writeSpiBytes(data)

	def writeSpiBytes(self,data):
		with open(self.spidev,"wb") as l:
			l.write(bytes(data))
			l.flush()

	def rgbToLedGrb(self,rgb):
		if not 0 <= rgb[0] <= 255:
			raise Exception("r out of bounds")
		elif not 0 <= rgb[1] <= 255:
			raise Exception("g out of bounds")
		elif not 0 <= rgb[2] <= 255:
			raise Exception("b out of bounds")

		return [((rgb[1]//2)+128),((rgb[0]//2)+128),((rgb[2]//2)+128)] #GRB

	def hexToLedGrb(self,hexclr):
		m = re.match("#(\w\w)(\w\w)(\w\w)",hexclr)

		return self.rgbToLedGrb([ int(m.group(1),16), int(m.group(2),16), int(m.group(3),16) ])

	def setPixels(self,pixelcolors,colorFormat):
		if len(pixelcolors) > self.nLeds:
			raise Exception("pixelcolors out of bounds (%i)" %(len(pixelcolors)))

		data = [0x00]
		for i in range(0,len(pixelcolors)):
			if colorFormat == "rgb":
				data += self.rgbToLedGrb(pixelcolors[i])
			elif colorFormat == "hex":
				data += self.hexToLedGrb(pixelcolors[i])
			else:
				raise Exception("unknown color format")


		data += [0x00]
		self.writeSpiBytes(data)

