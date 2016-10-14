#!/usr/bin/env python
import rospy
import std_msgs
import roslib
#roslib.load_manifest("baxter_pick_and_place")
import readline
import time
import pygame
import thread
from ein.msg import EinState
import math

import pyaudio
import wave

class EinClientBoth:
    def __init__(self,publish_topic_l, state_topic_l, publish_topic_r, state_topic_r):
        self.forth_command_publisher_l = rospy.Publisher(publish_topic_l, 
                                                       std_msgs.msg.String, queue_size=10)
        self.forth_command_publisher_r = rospy.Publisher(publish_topic_r, 
                                                       std_msgs.msg.String, queue_size=10)
        self.state = None
        self.stack = []
        
	self.forth_command_publisher_l.publish("1 setRepeatHalo")
	self.forth_command_publisher_r.publish("0 setRepeatHalo")


    def state_callback(self, msg):
        self.state = msg
        self.stack = self.state.stack

    def printStack(self):
        print "Call Stack: "
        for word in reversed(self.stack):
            print " ".rjust(15), word
    def face(self):
	for y in range(1,5):
		for x in range(0,10):
			self.forth_command_publisher_l.publish("\"song01_0000"+str(x)+".tif\" publishImageFileToFace")
			time.sleep(.5)
		for x in range(11,100):
			self.forth_command_publisher_l.publish("\"song01_000"+str(x)+".tif\" publishImageFileToFace")
			time.sleep(.5)

    def ultrasoundm(self):
	self.forth_command_publisher_l.publish("assumeCrane1 ;")
	self.forth_command_publisher_r.publish("assumeCrane1 ;")
	time.sleep(1)
	self.forth_command_publisher_r.publish("0 setRepeatHalo")
	time.sleep(3)
	self.forth_command_publisher_l.publish("\"wiki\" import ")
	time.sleep(.5)
	self.forth_command_publisher_l.publish("0 setRedHalo ")
	self.forth_command_publisher_l.publish("setControlModeAngles")	
	thread.start_new_thread(ultras,())
	time.sleep(2)
	self.forth_command_publisher_l.publish("blink_sonar_swoop ;")
	
	self.forth_command_publisher_l.publish("0 0 0 0 0 0.3 0 moveJointsByAngles ;")
	self.forth_command_publisher_r.publish("0 0 0 0 0 0.3 0 moveJointsByAngles")
	time.sleep(1)

	self.forth_command_publisher_l.publish("0 0 0 0 0 -.3 0 moveJointsByAngles ;")
	self.forth_command_publisher_r.publish("0 0 0 0 0 -.3 0 moveJointsByAngles ;")
	time.sleep(1)

	self.forth_command_publisher_l.publish("blink_sonar_swoop ;")
	self.forth_command_publisher_l.publish("openGripper ;")
	self.forth_command_publisher_r.publish("openGripper ;")
	time.sleep(1)

	self.forth_command_publisher_l.publish("closeGripper ;")
	self.forth_command_publisher_r.publish("closeGripper ;")
	time.sleep(1)

	self.forth_command_publisher_l.publish("blink_sonar_swoop ;")
	self.forth_command_publisher_l.publish("openGripper ;")
	self.forth_command_publisher_r.publish("openGripper ;")
	time.sleep(1)

	self.forth_command_publisher_l.publish("closeGripper ;")
	self.forth_command_publisher_r.publish("closeGripper ;")
	time.sleep(3)

	self.forth_command_publisher_l.publish("blink_sonar_swoop  ;")
	self.forth_command_publisher_l.publish("openGripper ;")
	self.forth_command_publisher_r.publish("openGripper ;")
	time.sleep(1)

	self.forth_command_publisher_l.publish("closeGripper ;")
	self.forth_command_publisher_r.publish("closeGripper ;")
	time.sleep(4)
	self.forth_command_publisher_l.publish("100 setRedHalo ;")
	time.sleep(1)
    def servosm(self):
	self.forth_command_publisher_l.publish("assumeFacePose ;")
	self.forth_command_publisher_r.publish("0 setRepeatHalo")
	al = "( oZDown ) "
	bl = "( oZUp ) "
	cl = "( oXUp ) "
	dl = "( oXDown ) "
	el = "( oYDown ) "
	fl = "( oYUp ) "
	self.forth_command_publisher_r.publish(".85 -0.59 0.22 0.12 0.7 -0.08 0.69 moveToEEPose ;")
	br = "( oZDown ) "
	ar = "( oZUp ) "
	dr = "( oXUp ) "
	cr = "( oXDown ) "
	er = "( oYDown ) "
	fr = "( oYUp ) "
	time.sleep(2.5)
	self.forth_command_publisher_l.publish("0 setRedHalo ")
	time.sleep(.5)
	#self.forth_command_publisher_l.publish("blink_arms ;")
	#time.sleep(2)
	thread.start_new_thread(IKs,())
	time.sleep(1.9)
	self.forth_command_publisher_l.publish(al + "100 replicateWord ;")
	self.forth_command_publisher_r.publish(ar + "100 replicateWord ;")
	time.sleep(.8)
	self.forth_command_publisher_l.publish(bl + "200 replicateWord ;")
	self.forth_command_publisher_r.publish(br + "200 replicateWord ;")
	time.sleep(.8)
	self.forth_command_publisher_l.publish(al + "100 replicateWord ;")
	self.forth_command_publisher_r.publish(ar + "100 replicateWord ;")
	time.sleep(.5)

	self.forth_command_publisher_l.publish(cl + "70 replicateWord ;")
	self.forth_command_publisher_r.publish(cr + "70 replicateWord ;")
	time.sleep(.8)
	self.forth_command_publisher_l.publish(dl + "70 replicateWord waitUntilAtCurrentPosition "+dl+"70 replicateWord waitUntilAtCurrentPosition ;")
	self.forth_command_publisher_r.publish(dr + "70 replicateWord waitUntilAtCurrentPosition "+dr+"70 replicateWord waitUntilAtCurrentPosition ;")
	time.sleep(.8)
	self.forth_command_publisher_l.publish(cl + "70 replicateWord ;")
	self.forth_command_publisher_r.publish(cr + "70 replicateWord ;")
	time.sleep(.5)

	self.forth_command_publisher_l.publish(el + "50 replicateWord ;")
	self.forth_command_publisher_r.publish(er + "50 replicateWord ;")
	time.sleep(.8)
	self.forth_command_publisher_l.publish(fl + "50 replicateWord waitUntilAtCurrentPosition "+fl+"50 replicateWord waitUntilAtCurrentPosition ;")
	self.forth_command_publisher_r.publish(fr + "50 replicateWord waitUntilAtCurrentPosition "+fr+"50 replicateWord waitUntilAtCurrentPosition ;")
	time.sleep(.8)
	self.forth_command_publisher_l.publish(el + "50 replicateWord ;")
	self.forth_command_publisher_r.publish(er + "50 replicateWord ;")
	time.sleep(2.5)

	self.forth_command_publisher_l.publish(bl + "100 replicateWord ;")
	self.forth_command_publisher_r.publish(br + "100 replicateWord ;")
	time.sleep(.8)
	self.forth_command_publisher_l.publish(al + "200 replicateWord ;")
	self.forth_command_publisher_r.publish(ar + "200 replicateWord ;")
	time.sleep(.8)
	self.forth_command_publisher_l.publish(bl + "100 replicateWord ;")
	self.forth_command_publisher_r.publish(br + "100 replicateWord ;")
	time.sleep(5)
	self.forth_command_publisher_l.publish("100 setRedHalo ;")
	time.sleep(1);

    def IKm(self):
	time.sleep(.5)
	self.forth_command_publisher_l.publish("assumeBeeHome ;")
	self.forth_command_publisher_r.publish("0 setRepeatHalo")
	time.sleep(.3)
	al = "( xDown ) "
	bl = "( xUp ) "
	cl = "( zUp ) "
	dl = "( zDown ) "
	self.forth_command_publisher_r.publish("0.23 -0.78 0.06 -0.05 0.99 -0.04 -0.002 moveToEEPose ;")
	br = "( xDown ) "
	ar = "( xUp ) "
	cr = "( zUp ) "
	dr = "( zDown ) "
	time.sleep(2)
	self.forth_command_publisher_l.publish("0 setRedHalo ;")
	time.sleep(1)
	#self.forth_command_publisher_l.publish("blink_arms ;")
	#time.sleep(2)
	thread.start_new_thread(servoss,())
	time.sleep(1.8)
	self.forth_command_publisher_l.publish(al + "20 replicateWord ;")
	self.forth_command_publisher_r.publish(ar + "20 replicateWord ;")
	time.sleep(.7)
	self.forth_command_publisher_l.publish(bl + "40 replicateWord ;")
	self.forth_command_publisher_r.publish(br + "40 replicateWord ;")
	time.sleep(.7)
	self.forth_command_publisher_l.publish(al + "20 replicateWord ;")
	self.forth_command_publisher_r.publish(ar + "20 replicateWord ;")
	time.sleep(1)
	self.forth_command_publisher_l.publish(cl + "30 replicateWord ;")
	self.forth_command_publisher_r.publish(cr + "30 replicateWord ;")
	time.sleep(.5)
	self.forth_command_publisher_l.publish(dl + "30 replicateWord ;")
	self.forth_command_publisher_r.publish(dr + "30 replicateWord ;")
	time.sleep(.5)
	self.forth_command_publisher_l.publish(cl + "30 replicateWord ;")
	self.forth_command_publisher_r.publish(cr + "30 replicateWord ;")

	time.sleep(1)
	self.forth_command_publisher_l.publish(al + "20 replicateWord ;")
	self.forth_command_publisher_r.publish(ar + "20 replicateWord ;")
	time.sleep(.7)
	self.forth_command_publisher_l.publish(bl + "40 replicateWord ;")
	self.forth_command_publisher_r.publish(br + "40 replicateWord ;")
	time.sleep(.7)
	self.forth_command_publisher_l.publish(al + "20 replicateWord ;")
	self.forth_command_publisher_r.publish(ar + "20 replicateWord ;")
	time.sleep(2.8)

	self.forth_command_publisher_l.publish(dl + "30 replicateWord ;")
	self.forth_command_publisher_r.publish(dr + "30 replicateWord ;")
	time.sleep(.5)
	self.forth_command_publisher_l.publish(cl + "20 replicateWord ;")
	self.forth_command_publisher_r.publish(cr + "20 replicateWord ;")
	time.sleep(.5)
	self.forth_command_publisher_l.publish(dl + "20 replicateWord ;")
	self.forth_command_publisher_r.publish(dr + "20 replicateWord ;")
	time.sleep(4)
	self.forth_command_publisher_l.publish("0 setRedHalo ;")
	time.sleep(1)

    def grippersm(self):
	self.forth_command_publisher_l.publish("clearStack ;")
	self.forth_command_publisher_r.publish("0 setRepeatHalo")
	time.sleep(.5)
	self.forth_command_publisher_l.publish("\"wiki\" import ;")
	time.sleep(.3)
	self.forth_command_publisher_l.publish("closeGripper ;")
	self.forth_command_publisher_r.publish("closeGripper ;")
	time.sleep(.3)
	self.forth_command_publisher_l.publish("100 setGreenHalo 100 setRedHalo ;")
	self.forth_command_publisher_r.publish("100 setGreenHalo 100 setRedHalo ;")
	time.sleep(.5)
	
	#self.forth_command_publisher_l.publish("1.13 .30 .337 0.02 .80 -0.053 .588 moveToEEPose ;")
	#self.forth_command_publisher_r.publish("1.13 -0.3 0.38 0.02 0.8 0.01 0.59 moveToEEPose ;")

	self.forth_command_publisher_l.publish("assumeShrugPose ;")
	self.forth_command_publisher_r.publish("assumeShrugPose ;")
	
	time.sleep(4)
	self.forth_command_publisher_l.publish("0 setRedHalo ;")
	time.sleep(.2)
	#self.forth_command_publisher_l.publish("blink_arms ;")
	#time.sleep(2)
	#thread.start_new_thread(self.face,())
	thread.start_new_thread(gripperss,())
	time.sleep(2.1)
	self.forth_command_publisher_l.publish("openGripper ;")
	self.forth_command_publisher_r.publish("openGripper ;")
	time.sleep(1)
	self.forth_command_publisher_l.publish("closeGripper ;")
	self.forth_command_publisher_r.publish("closeGripper ;")
	time.sleep(1.1)
	self.forth_command_publisher_l.publish("openGripper ;")
	self.forth_command_publisher_r.publish("openGripper ;")
	time.sleep(1)
	self.forth_command_publisher_l.publish("closeGripper ;")
	self.forth_command_publisher_r.publish("closeGripper ;")
	time.sleep(1.1)
	self.forth_command_publisher_l.publish("openGripper ;")
	self.forth_command_publisher_r.publish("openGripper ;")
	time.sleep(1)
	self.forth_command_publisher_l.publish("closeGripper ;")
	self.forth_command_publisher_r.publish("closeGripper ;")
	time.sleep(3.1)
	self.forth_command_publisher_l.publish("openGripper ;")
	self.forth_command_publisher_r.publish("openGripper ;")
	time.sleep(1)
	self.forth_command_publisher_l.publish("closeGripper ;")
	self.forth_command_publisher_r.publish("closeGripper ;")
	time.sleep(5)
	self.forth_command_publisher_l.publish("100 setRedHalo ;")
	time.sleep(1)

    def ask(self):
	self.forth_command_publisher_l.publish("happyFace")
	time.sleep(1)
	self.grippersm()
	self.servosm()
	self.IKm()

def save_history_hook():
    import os
    histfile = os.path.join(os.path.expanduser("~"), ".ein_client_history")
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    import atexit
    atexit.register(readline.write_history_file, histfile)

def grippers():
	pygame.init()

	pygame.mixer.music.load("grippers.wav")
	pygame.mixer.music.play()

def gripperss():
	"""pygame.mixer.init(44100, -16, 2, 1024)
	pygame.mixer.music.load("grippers.mid")
	pygame.mixer.music.play()"""

	chunk = 1024
	f = wave.open("./test1.wav","rb")
	
	p = pyaudio.PyAudio()
	
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
			channels = f.getnchannels(),
			rate = f.getframerate(),
			output = True)

	data = f.readframes(chunk)
	
	while data != '':
		stream.write(data)
		data = f.readframes(chunk)

	stream.stop_stream()
	stream.close()
	
	p.terminate()

def servoss():
	chunk = 1024
	f = wave.open("./IKs_john.wav","rb")
	
	p = pyaudio.PyAudio()
	
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
			channels = f.getnchannels(),
			rate = f.getframerate(),
			output = True)

	data = f.readframes(chunk)
	
	while data != '':
		stream.write(data)
		data = f.readframes(chunk)

	stream.stop_stream()
	stream.close()
	
	p.terminate()

def ultras():
	chunk = 1024
	f = wave.open("./ultras_john.wav","rb")
	
	p = pyaudio.PyAudio()
	
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
			channels = f.getnchannels(),
			rate = f.getframerate(),
			output = True)

	data = f.readframes(chunk)
	
	while data != '':
		stream.write(data)
		data = f.readframes(chunk)

	stream.stop_stream()
	stream.close()
	
	p.terminate()

def IKs():
	chunk = 1024
	f = wave.open("./servos_john.wav","rb")
	
	p = pyaudio.PyAudio()
	
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
			channels = f.getnchannels(),
			rate = f.getframerate(),
			output = True)

	data = f.readframes(chunk)
	
	while data != '':
		stream.write(data)
		data = f.readframes(chunk)

	stream.stop_stream()
	stream.close()
	
	p.terminate()



def main():
    import sys

    arml = "left"
    armr = "right"
    rospy.init_node("ein_client_%s" % arml, anonymous=True)
    client = EinClientBoth("/ein/%s/forth_commands" % arml,
                       "/ein_%s/state" % arml,
                       "/ein/%s/forth_commands" % armr,
                       "/ein_%s/state" % armr,
                       )

    client.ask()


    
if __name__=='__main__':
    main()
