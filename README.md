#Home Theatre Control

The aim of this project is to provide physical controls for a modern home theatre setup using Raspberry Pi GPIO pins. The project was initially developed to allow visiting relatives with poor digital literacy skills to power on and off and launch key programs on a home theatre system without using a keyboard, mouse, mobile phone, or tablet.

The software accepts input from buttons connected to the Pi’s GPIO pins, and controls a TV (and other home theatre devices if desired) via infrared signals, and a Windows HTPC using MQTT messages and EventGhost.

##Hardware Requirements
- a Raspberry Pi (any model will do), or similar, running a Debian based operating system (Minibian is my favourite).
- a breakout board connected to the Pi’s GPIO pins containing the following:
    - IR sender and receiver (see Alex Bain’s blog article in the references for how to assemble this as well as LIRC configuration).
    - A number of buttons, each connected between a separate GPIO pin and ground.

##Assumptions
- LIRC has been configured to turn on the TV and for any other home theatre devices you wish to control.
- There is a functioning and tested MQTT broker on the network.
- Event Ghost has been configured on the HTPC to listen for MQTT messages to restart and shutdown the system as well as any other functionality desired (Kodi / Plex / Steam etc).

##Installation instructions
###Install dependencies
sudo apt-get install python python-pip etherwake
sudo pip install RPi.GPIO paho-mqtt

###Install buttons script
- Save the file buttons.py to your desired location
- Ensure the PIN_CONFIG variable aligns to the pin configuration on the breakout board
- Ensure HOST and MQTT_BROKER variables align to HTPC and MQTT Broker IP addresses on the network.
- Ensure IR_CMD aligns to the LIRC command used to power on and off the TV
- Ensure the MAC address of the WOL_CMD variable aligns to the MAC address of the HTPC.

###Install init script
Save the file buttons.init as /etc/init.d/buttons
Update the DAEMON variable to the location of the buttons.py script
(note: the script has to run as root to allow access to the GPIO pins)
Enable the init script at startup
sudo update-rc.d buttons defaults
Start the script
Sudo service buttons start
Check for error messages
Sudo service buttons status

##Further Work
Subsequent to the implementation of this project, a [FLIRC](flirc.tv) device was configured to allow a remote control for a stereo system to control navigation of the program running on the HTPC. This allows remote control to provide power and volume controls for the stereo, as well as navigation controls for the HTPC.

As the Raspberry Pi in this project is operates both an infrared receiver and transmitter, it can be configured to receive signals from a remote control and retransmit them to different devices. I have used this to allow my stereo system remote control, manufactured by Pioneer, to power off the TV, manufactured by Samsung, for instances where I wish to power off the TV but leave the HTPC on for other tasks. Discussion on how this can be configured is beyond the scope of this article.

##Final Thoughts etc
I have recently implemented the fantastic open source home automation software [Home Assistant](https://home-assistant.io) which duplicates much of the functionality of this project, but not all. I intend on Home Theatre Control in my living room even if I do not use it every day as it is useful when I have visitors with poor digital literacy skills, or who I do not wish to grant access to Home Assistant.

##References
http://alexba.in/blog/2013/03/09/raspberrypi-ir-schematic-for-lirc/
