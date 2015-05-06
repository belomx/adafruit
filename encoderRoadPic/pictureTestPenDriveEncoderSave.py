#!/usr/bin/python
import os
import pygame, sys
import gaugette.rotary_encoder
import thread
import time
import RPi.GPIO as GPIO
import Queue

from pygame.locals import *

import pygame.camera

def get_path ( initialPath):
	for dirname, dirnames, filenames in os.walk(initialPath):
        	isMountFounded = False
        	for subdirname in dirnames:
                	path = os.path.join(dirname, subdirname)
                	if os.path.ismount(os.path.join(dirname, subdirname)):
				return path
	return "/home/pics"


def get_camera (width, height):
        #initialise pygame
        pygame.init()
        pygame.camera.init()
        cam = pygame.camera.Camera("/dev/video0",(width,height))
        return cam


def take_picture(cam, width, height, queue):
	#setup window
	#cam.start()
	#windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
	#pygame.display.set_caption('Camera')
	#take a picture
	image = cam.get_image()
	#cam.stop()
	#display the picture
	#catSurfaceObj = image
	#windowSurfaceObj.blit(catSurfaceObj,(0,0))
	#pygame.display.update()
	#return image 
	queue.put(image)


def get_rotary_encoder():
	A_PIN  = 7
	B_PIN  = 9
	encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
	encoder.start()
	return encoder


def save_picture(path, windowSurfaceObj):
	#save picture
	if windowSurfaceObj != None:
		pygame.image.save(windowSurfaceObj,path+'/picture'+str(time.time())+'.jpg')
 

def get_encoder_delta(encoder):
	delta = encoder.get_delta()
	return delta


def encoder_worker(path, width, height, encoder):
	cam = get_camera(width, height)	
	cam.start()
	delta = 0
	queue = Queue.Queue()
	while 1:
		delta += get_encoder_delta(encoder)
		if delta > 5:
			thread.start_new_thread(take_picture, (cam, width, height, queue))
			#thread.start_new_thread(save_picture, (path, windowSurfaceObj))
			#windowSurfaceObj = take_picture(get_camera(width, height), width, height)
			if not queue.empty():
				thread.start_new_thread(save_picture, (path, queue.get_nowait()))
			delta = 0
			

try: 
	#Turn on LED
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(11, GPIO.OUT)
	GPIO.output(11, GPIO.HIGH)
	#get path to save in the pen drive
	path = get_path( "/media")
	print "the path = %s" %  path
	#get the encoder
	encoder = get_rotary_encoder()
	#define the scale of the pictures
	width = 352 
	height = 288 
	#get the camera
	#cam = get_camera(width, height)
	#start the worker
	encoder_worker(path, width, height, encoder)
finally:
	GPIO.output(11, GPIO.LOW)
	print "end"
