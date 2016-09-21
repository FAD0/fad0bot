# Modules needed for motor control
# import vimpdb; vimpdb.set_trace()
# from pudb import set_trace; set_trace()
import serial
import readchar
import RPi.GPIO as GPIO
import kbhit
from mymod.fad0mod import *
from threading import Thread
import cv2
import freenect
from time import sleep

port =serial.Serial(
    "/dev/ttyACM0",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout = 0,
    timeout = 10)


def displayvid():
    while(1):
        array,_ = freenect.sync_get_video()
        array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
        cv2.imshow('img', array)
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(500) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

# initialize kbhit to sense keyboard input without carriage return
kb = kbhit.KBHit()

# Initialize gy80 and exit if movement is detected
initgy80()

# Pin definition BMC naming.
# Motor power enable
motor_enable = 18 # Broadcom pin 18
# Kinect power enable
kinect_enable = 17 # Broadcom pin 17

# IO Pin functional definition
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(motor_enable, GPIO.OUT) # Motor Enable
GPIO.setup(kinect_enable, GPIO.OUT) # Kinect Enable

# Enable motor power
GPIO.output(motor_enable, True)

print(port.isOpen()) 
sleep(2) # this delay is needed to let the arduino and/or serial port initialize
print("'p'  = protocol change strength")
print("'c'  = protocol change turn strength")
print("'o'  = forward")
print("'.'  = backward")
print("';'  = turn right")
print("'k'  = turn left")
print("'l'  = stop")
print("'i'  = incrementally increase f/b strength")
print("'d'  = incrementally decrease f/b strength")
print("'u'  = camera look up")
print("'m'  = camera look down")
print("'q'  = quit")

vctfl = open("vector_file.txt", 'w')
vctfl.write('CMD\tright\tleft\ttime\theading\n')


main_loop_flag=1
try:
    input_char = readchar.readkey()
    while (main_loop_flag):

        # Start of the protocol change strength command
        if input_char == 'p':
            port.write("protocol_change\n")
            get_protocol(input_char, port)
            input_char = get_incdec(input_char, port, vctfl)

        # Start of the protocol change turn strength command
        elif input_char == 'c':
            port.write("protocol_change_turn\n")
            get_protocol(input_char, port)
            input_char = get_incdec(input_char, port, vctfl)

        # Start of the forward command
        elif input_char == 'o':
            print ('forward')
            port.write("forward\n")
            input_char = get_incdec(input_char, port, vctfl)

        # Start of the backward command
        elif input_char == ('.'):
            print ('backward')
            port.write("backward\n")
            input_char = get_incdec(input_char, port, vctfl)

        # Start of the turn right command
        elif input_char == (';'):
            print ('right')
            port.write("right\n")
            input_char = get_incdec(input_char, port, vctfl)

        # Start of the turn left command
        elif input_char == ('k'):
            print ('left')
            port.write("left\n")
            input_char = get_incdec(input_char, port, vctfl)

        # Start of the stop command
        elif input_char == ('l'):
            print ('stop')
            port.write("stop\n")
            input_char = (readchar.readkey())

        # Start of the stop command
        elif input_char == ('u'):
            print ('camera tilting up')
            port.write('tilt_cam_up\n')
            input_char = (readchar.readkey())

        # Start of the stop command
        elif input_char == ('m'):
            print ('camera tilting down')
            port.write('tilt_cam_down\n')
            input_char = (readchar.readkey())

        # Start of the quit command
        elif input_char == ('q'):
            print ('quit')
            main_loop_flag=0
        else:
            input_char = (readchar.readkey())

finally:
    print('Stopping and disabling motor.')
    vctfl.close
    port.write("stop\n")
    GPIO.output(motor_enable, False)
    GPIO.remove_event_detect(rmotor_a)
    GPIO.remove_event_detect(rmotor_b)
    GPIO.remove_event_detect(lmotor_a)
    GPIO.remove_event_detect(lmotor_b)
