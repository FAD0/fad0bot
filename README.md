# fad0bot
Software for my fad0bot robot

fad0bot3b.py is the "master" program that resides in the master processor, which is an RPi2.  Presently it recieves input from the keyboard and sends commands to an Arduino Uno, which in turn sends PWM signals to the motor controller.

fad0mod.py acts as a library that contains functions called in fad0bot3b.py.

fad0bot3b.ino is the Arduino C program downloaded into the Arduino Uno.  It takes commands from the RPi2 through the USB, and outputs corresponding PWM signals sent to the motor controller.

server_stream.py Copyright 2013-2015 Dave Jones. was copied from https://picamera.readthedocs.io/en/release-1.12/recipes1.html, and opens a video socket for streaming from the PRi3 with picam onto my MacAir.

client_stream.py Copyright 2013-2015 Dave Jones, was copied from https://picamera.readthedocs.io/en/release-1.12/recipes2.html, and is run on the RPi3 with picam to connected to the socket opened by my MacAir.
