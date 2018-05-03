import snowboydecoder
import sys
import signal
from gopigo import *
from time import sleep
import RPi.GPIO as GPIO 
import time 
#au lieu de gopigo importer les gpio
# Demo code for listening two hotwords at the same time
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT) 
GPIO.setup(15,GPIO.OUT)

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


models = ["C:/Users/user1/Downloads/AVANCE.pmdl", "C:/Users/user1/Downloads/STOP.pmdl", "C:/Users/user1/Downloads/DROITE.pmdl", "C:/Users/user1/Downloads/RECULE.pmdl", "C:/Users/user1/Downloads/GAUCHE.pmdl"]

def AVANCE():
GPIO.output(7,True) 
GPIO.output(15,True)
time.sleep(3)
 STOP()

def STOP():
GPIO.output(7,False)
GPIO.output(13,False)
GPIO.output(11,False) 
GPIO.output(15,False) 
time.sleep(3) 
    STOP()

def DROITE():
GPIO.output(7,False) 
GPIO.output(13,True) 
GPIO.output(11,True)
GPIO.output(15,False)
 time.sleep(3)
    STOP()
    

def GAUCHE():
GPIO.output(7,True)
GPIO.output(13,False)
GPIO.output(11,False) 
GPIO.output(15,True) 
time.sleep(3) 
    STOP()

def RECULE():
 GPIO.output(11,False)
 GPIO.output(13,False)
 time.sleep(3)
  STOP()


    

    
# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
enable_servo()
servo(90)

sensitivity = 0.35
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: AVANCE(), lambda: RECULE(), lambda: DROITE(), lambda: GAUCHE(), lambda: STOP()]

print('Listening... Press Ctrl+C to exit')


# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
