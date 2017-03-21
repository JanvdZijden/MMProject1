#!/usr/bin/python

import pygame
import time
import os
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pygame.init()
windowInfo = pygame.display.Info()
screen_size = (windowInfo.current_w,windowInfo.current_h)
stap_lock = "Rechts"
key_Check= True
x = 50

def fotosladen():
	for file in os.listdir("/home/pi/usbdrv"):
		if file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG"):
			#image.append(file)
			image = pygame.image.load("/home/pi/usbdrv/"+file)
			image = pygame.transform.scale(image, (screen_size))
			yield image

screen = pygame.display.set_mode((windowInfo.current_w,(windowInfo.current_h)))
foto_generator = fotosladen()
image = foto_generator.next()
photo = image
volgende_foto = foto_generator.next()
next_foto = False
mannetje = pygame.image.load("/home/pi/Documents/staandop1beenkleur.png")

while True:
	if key_Check: 							#Checkt hoe je staat en vult het balkje (als nodig)
		sensor_value = (GPIO.input(23),GPIO.input(24))
		events = pygame.event.get()
		if (sensor_value == (0,1) and stap_lock=="Rechts"):
			if x < windowInfo.current_w:
				x += 100
			else:
				mannetje = pygame.transform.flip(mannetje, True, False)
				screen.blit(mannetje, (windowInfo.current_w - 500 - mannetje.get_width(),0))
				pygame.display.update()
				while sensor_value != (1,0):
				 	sensor_value = (GPIO.input(23),GPIO.input(24))
				#mannetje = pygame.transform.flip(mannetje, True, False)
				stap_lock = "Links"
				next_foto = True
				key_Check = False
		elif (sensor_value == (1,0) and stap_lock=="Links"):
			if x < windowInfo.current_w:
				x += 100
			else: 
				while sensor_value != (0,1):
					sensor_value = (GPIO.input(23),GPIO.input(24))
				mannetje =  pygame.transform.flip(mannetje, True, False) 
				stap_lock = "Rechts"
				next_foto = True
				key_Check = False
		for event in events:
			if event.key == pygame.K_ESCAPE:
				sys.exit(0)
	
	if next_foto:				# Als dit True is gaat het systeem naar de volgende foto
		x = 50
		image = volgende_foto
		photo = image
		screen.blit(photo, (0,0))
		pygame.display.flip()
		try:
			volgende_foto = foto_generator.next()
		except StopIteration:
			foto_generator = fotosladen()
			#photo = image
			volgende_foto = foto_generator.next()
		next_foto = False
		key_Check = True
	
	screen.blit(photo, (0,0))
	pygame.draw.rect(screen,(132,240,95),(0,windowInfo.current_h-(windowInfo.current_h/22),x,windowInfo.current_h),0)
	screen.blit(mannetje, (windowInfo.current_w - mannetje.get_width(),0))
	pygame.display.flip()  	

