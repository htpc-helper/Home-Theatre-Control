#!/usr/bin/python

import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import subprocess
import time
import os

#Define list of button parameters
PIN_CONFIG = [
{'pin':20, 'mqttTopic':'home/htpc/power/restart'},
{'pin':21, 'mqttTopic':'home/htpc/power/off'},
{'pin':13, 'mqttTopic':'home/htpc/kodi/on'},
{'pin':19, 'mqttTopic':'home/htpc/plex/on'},
{'pin':26, 'mqttTopic':'home/htpc/steam/on'}
]

#Define other inputs
HOST = '10.0.1.xxx'
MQTT_BROKER = '10.0.1.xxx'
IR_CMD = 'irsend SEND_ONCE samsung KEY_POWER2'
WOL_CMD = 'sudo etherwake xx:xx:xx:xx:xx:xx'

#Define functions
def MqttMessage(mqtt_topic, mqtt_broker):
  publish.single(mqtt_topic, '', hostname=mqtt_broker)
  print('MQTT message \"' + mqtt_topic + '\" sent via broker \"' + mqtt_broker + '\"')

def CmdBash(command, message):
  subprocess.call(['bash', '-c', command])
  if message != '': print(message)

def CheckStatus(host):
  print('Checking status of: ' + host)
  response = os.system("ping -c 1 " + host)
  if response:
    print('Fail, host \"' + host + '\" is unreachable')
    return False
  else:
    print('Success')
    return True

def Startup(host, mqtt_topic):
  #Ping HTPC to check if already powered on, else initiate startup sequence
  if CheckStatus(host): return True
  print('Initiating startup sequence instead')
  #Turn on TV then boot PC using WOL
  CmdBash(IR_CMD, 'IR power signal sent to TV')
  CmdBash(WOL_CMD, 'Magic packet sent to wake HTPC')

def Callback(channel):
  #Find mqttTopic corresponding to PIN
  for item in PIN_CONFIG:
    if item['pin'] == channel:
      mqtt_topic = item['mqttTopic']
  #Print details of instruction being processed
  print('Button ' + str(channel) + ' was pressed which corresponds to the command: ' + mqtt_topic)
  #Process topic
  if mqtt_topic == 'home/htpc/power/restart' or 'home/htpc/power/off':
    if CheckStatus(HOST):					        #check whether htpc already on
      MqttMessage(mqtt_topic, MQTT_BROKER)			#trigger shutdown directly
      if mqtt_topic == 'home/htpc/power/off':
        time.sleep(5)	   					        #wait 5s, then turn off TV
        CmdBash(IR_CMD, 'IR power signal sent to TV')
  else:
    if startup(HOST, mqtt_topic):	 			    #send MQTT message if PC on, else initiate startup sequence
      MqttMessage(mqtt_topic, MQTT_BROKER)

def GPIOsetup(pin):
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.add_event_detect(pin, GPIO.FALLING, callback=Callback, bouncetime=10000)

#@@@ MAIN PROGRAM @@@
#Setup buttons according to parameters defined in list
GPIO.setmode(GPIO.BCM)
for item in PIN_CONFIG:
  pin = item['pin']
  GPIOsetup(pin)

#Infinite loop to prevent program from ending
while True:
  continue