#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lpd8806 import LPD8806
from time import sleep

class ledEffects(LPD8806):

	def unicorn(self,flag,alt):
		#flags: 0->exit , 1->continue
		# R,B++ >> B,R-- >> B,G++ >> G,B-- >> G,R++ >> R,G--

		delta = 0
		r = 255
		g = 0
		b = 0
		pixels = []
		for i in range(0,self.nLeds):
			pixels.append([r,g,b])

		if alt == 0:
			delta = 1
		elif alt == 1:
			delta = 17
		elif alt == 2:
			delta = 51
		else:
			raise Exception("valid alt's are 0,1,2")

		while flag.value > 0:
			if r == 255 and g == 0 and 0 <= b < 255:
				b+=delta
			elif 255 >= r > 0 and g == 0 and b == 255:
				r-=delta
			elif r == 0 and 0 <= g < 255 and b == 255:
				g+=delta
			elif r == 0 and g == 255 and 255 >= b > 0:
				b-=delta
			elif 0 <= r < 255 and g == 255 and b == 0:
				r+=delta
			elif r == 255 and 255 >= g > 0 and b == 0:
				g-=delta

			pixels[0] = [r,g,b]
			for i in range(1,self.nLeds):
				pixels[self.nLeds-i] = pixels[self.nLeds-i-1] #shift

			self.setPixels(pixels,"rgb")
			sleep(0.05)
		
		print("unicorn exit")

	def custom(self,flag,shared):
		#flags: 0->exit , 1->load new , 2->skip
		r = 255
		g = 255
		b = 255
		alt = 0

		pixels = []
		blank = []
		for i in range(0,self.nLeds):
			blank.append([0,0,0])
			pixels.append([r,g,b])

		while flag.value > 0:
			if flag.value == 1:
				#load new values
				r = shared[0]
				g = shared[1]
				b = shared[2]
				alt = shared[3]

				for i in range(0,self.nLeds):
						pixels[i] = [r,g,b]

				self.setPixels(pixels,"rgb")
				#set flag to skip
				flag.value = 2	#this is not safe, main could have set the flag to 0 which will now be overwritten (no lock)
								#however, we don't expect this condition to happen (asking for exit right after new value load)


			if alt == 1:
				#blink
				self.setPixels(blank,"rgb")
				sleep(0.1)
				self.setPixels(pixels,"rgb")
				sleep(0.1)

		print("custom exit")


