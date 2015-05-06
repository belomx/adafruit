#!/usr/bin/python
import os
import pygame, sys
import gaugette.rotary_encoder
import thread
import time

from pygame.locals import *
import pygame.camera

def get_path ( initialPath):
	for dirname, dirnames, filenames in os.walk(initialPath):
        	isMountFounded = False
        	for subdirname in dirnames:
                	path = os.path.join(dirname, subdirname)
                	if os.path.ismount(os.path.join(dirname, subdirname)):
				return path
	return "/home"


def get_camera (cam, width, height):
        if (cam == None):
                #initialise pygame
                pygame.init()
                pygame.camera.init()
                cam = pygame.camera.Camera("/dev/video0",(width,height))
        return cam


def take_picture(cam, width, height):
	#setup window
	cam.start()
	windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
	pygame.display.set_caption('Camera')
	#take a picture
	image = cam.get_image()
	cam.stop()
	#display the picture
	catSurfaceObj = image
	windowSurfaceObj.blit(catSurfaceObj,(0,0))
	pygame.display.update()
	return windowSurfaceObj


def get_rotary_encoder():
	A_PIN  = 7
	B_PIN  = 9
	encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
	encoder.start()
	return encoder


def save_picture(path, windowSurfaceObj):
	#save picture
	if windowSurfaceObj != None:
		pygame.image.save(windowSurfaceObj,path+'/picture.jpg')
 

def get_encoder_delta(encoder):
	delta = encoder.get_delta()
	return delta


def encoder_worker(path, cam, width, height, encoder):
	delta = 0
	while 1:
		delta += get_encoder_delta(encoder)
		if delta > 5:
			windowSurfaceObj = thread.start_new_thread(take_picture, (cam, width, height))
			thread.start_new_thread(save_picture, (path, windowSurfaceObj))
			windowSurfaceObj = None
			

try: 
	#get path to save in the pen drive
	path = get_path( "/media")
	print "the path = %s" %  path
	#get the encoder
	encoder = get_rotary_encoder()
	#define the scale of the pictures
	width = 352 
	height = 288 
	cam = None
	#get the camera
	cam = get_camera(cam, width, height)
	#start the worker
	encoder_worker(path, cam, width, height, encoder)
finally:
	print "end"
