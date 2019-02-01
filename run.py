import sys
sys.path.append("/home/pi/.local/lib/python3.5/site-packages")

import RPi.GPIO as GPIO
from time import sleep
import sounddevice as sd
import numpy as np
import csv
from time import strftime

lokaal = 'HL15-4.099'

i = 0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

def lamp_rood():
    GPIO.output(18,True)
    GPIO.output(24,False)
    GPIO.output(25,False)

def lamp_oranje():
    GPIO.output(24,True)
    GPIO.output(18,False)
    GPIO.output(25,False)

def lamp_groen():
    GPIO.output(25, True)
    GPIO.output(18, False)
    GPIO.output(24, False)

duration = 1

def niveau():
    def print_sound(indata, outdata, frames, time, status):
        volume_norm = int(np.linalg.norm(indata)*25)
        decibel = int(volume_norm)
        if int(volume_norm) >= 0 and int(volume_norm) < 15:
            print("Groen!")
            lamp_groen()

        if int(volume_norm) >= 15 and int(volume_norm) < 80:
            print("Oranje!")
            lamp_oranje()

        if int(volume_norm) >= 80:
            print("Rood!")
            lamp_rood()

        tijd  = strftime("%H:%M:%S")
	seconden = int(tijd[6:]) 
	if seconden == 00:
	    with open('metingen.csv', mode='w') as csv_file:
		csv_file.truncate()
		csv_file.close()
	    print('CSV')
            with open('metingen.csv', mode='a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=('datum', 'tijd', 'lokaal', 'decibel'))
                writer.writerow({'datum': (strftime("%Y-%m-%d")), 'tijd': (strftime("%H:%M:%S")), 'lokaal': (lokaal), 'decibel': (int(decibel))})
		csv_file.close()
        else:
            print(seconden)

    with sd.Stream(callback=print_sound):
        sd.sleep(duration * 1)

while True:
    niveau()
    sleep(1)