#!/usr/bin/python
""" A collection of def's for motor control and recording movements """

# from pudb import set_trace; set_trace()
# Modules needed to gy80 read (compass, acc, gyro)
import sys
from timeit import default_timer as timer
from time import sleep
from math import pi, sqrt
from gy80 import GY80
from gy80.quaternions import quaternion_to_euler_angles
import RPi.GPIO as GPIO
import readchar

imu = GY80()

# Quadrature Encoder count/distance
# ~78 posedge/cm 
quadencpercm = 78

def initgy80():
    """Initialize gy80 and exit if movement is detected"""
    imu = GY80()
    x, y, z = imu.read_accel()
    g = sqrt(x*x + y*y + z*z)
    print("Magnitude of acceleration %0.2fg (%0.2f %0.2f %0.2f)" % (g, x, y, z))
    if abs(g - 1) > 0.3:
        sys.stderr.write("Not starting from rest, acceleration %0.2f\n" % g)
        sys.exit(1)
    print("Starting q by acc/mag (%0.2f, %0.2f, %0.2f, %0.2f)" % imu._q_start)

def get_vector(ra_cntr, la_cntr, start_time, loop_name, vctfl):
    """Calculate and store trajectory - distance and direction"""
    rdist = ra_cntr*1.0/quadencpercm   # *1.0 converts int to float
    ldist = la_cntr*1.0/quadencpercm   # *1.0 converts int to float
    end_time = timer()
    travel_time = end_time - start_time 
    print(end_time)
    print(start_time)
    print(travel_time)
    ave_speed = (rdist + ldist)/(2*travel_time)
    imu.update()
    w, x, y, z = imu._current_hybrid_orientation_q
    yaw, pitch, roll = quaternion_to_euler_angles(w, x, y, z)
    print("G/A/C yaw %0.1f " % (yaw * 180.0 / pi))
    w, x, y, z = imu._current_gyro_only_q
    yaw, pitch, roll = quaternion_to_euler_angles(w, x, y, z)
    print("GQ    yaw %0.1f " % (yaw * 180.0 / pi))
    w, x, y, z = imu.current_orientation_quaternion_mag_acc_only()
    yaw, pitch, roll = quaternion_to_euler_angles(w, x, y, z)
    heading = yaw * 180.0/ pi
    print("A/CQ  yaw %0.1f " % heading)
    vctfl.write('{0:s}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4:.2f}\n'.format(loop_name, rdist, ldist, travel_time, heading))

def get_incdec(input_char, port, vctfl):
    """Increments and decrements speed and turn speed"""
    ra_cntr = rmotor_a_count
    la_cntr = lmotor_a_count
    loop_name = input_char
    start_time = timer()
    print(start_time)
    inner_loop_flag=1
    all_list = ['p', 'c', 'o', '.', ';', 'k', 'l', 'q']
    all_list.remove(loop_name)
    while(inner_loop_flag):
        if input_char in all_list:
            inner_loop_flag=0
            ra_cntr = rmotor_a_count - ra_cntr
            la_cntr = lmotor_a_count - la_cntr
            get_vector(ra_cntr, la_cntr, start_time, loop_name, vctfl)
        elif input_char == ('i'):
            if loop_name in [';', 'k']:
                port.write("increment_turn_strength\n")
                print ('turn strength incremented')
            else:
                port.write("increment_strength\n")
                print ('strength incremented')
            input_char = (readchar.readkey())
        elif input_char == ('d'):
            if loop_name in [';', 'k']:
                port.write("decrement_turn_strength\n")
                print ('turn strength decremented')
            else:
                port.write("decrement_strength\n")
                print ('strength decremented')
            input_char = (readchar.readkey())
        else:
            input_char = (readchar.readkey())
            print input_char
        sleep(0.10)
    return input_char

# Quadrature Encoder Pins
rmotor_a = 12
rmotor_b = 6
lmotor_a = 16
lmotor_b = 19

# Declare and initialize encoder counters and direction flags.
rmotor_a_count = 0L
rmotor_b_count = 0L
lmotor_a_count = 0L
lmotor_b_count = 0L
rforward = False
lforward = False

# Define IO interrupt action for quadrature encoder counters
def rma_callback(channel):
    """callback function for right motor a"""
    global rmotor_a_count
    global rforward
    rmotor_a_count += 1
    if(GPIO.input(rmotor_b) == False):
        rforward = True
    else:
        rforward = False
def rmb_callback(channel):
    """callback function for right motor b"""
    global rmotor_b_count
    rmotor_b_count += 1
def lma_callback(channel):
    """callback function for left motor a"""
    global lmotor_a_count
    lmotor_a_count += 1
def lmb_callback(channel):
    """callback function for left motor b"""
    global lmotor_b_count
    global lforward
    lmotor_b_count += 1
    if(GPIO.input(lmotor_a) == False):
        lforward = True
    else:
        lforward = False


# IO Pin functional definition
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(rmotor_a, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Right motor encoder output A
GPIO.setup(rmotor_b, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Right motor encoder output B
GPIO.setup(lmotor_a, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Left motor encoder output A
GPIO.setup(lmotor_b, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Left motor encoder output B
GPIO.add_event_detect(rmotor_a, GPIO.RISING, callback = rma_callback)  # add rising edge detection
GPIO.add_event_detect(rmotor_b, GPIO.RISING, callback = rmb_callback)  # add rising edge detection
GPIO.add_event_detect(lmotor_a, GPIO.RISING, callback = lma_callback)  # add rising edge detection
GPIO.add_event_detect(lmotor_b, GPIO.RISING, callback = lmb_callback)  # add rising edge detection

def get_protocol(input_char, port):
    invalid=1
    while invalid:
        try:
            if input_char == 'p':
                inprotocol = raw_input('Input new right:left strength: ')
            elif input_char == 'c':
                inprotocol = raw_input('Input new right:left turn strength: ')
            else:
                print("Error: get_protocol only exists for 'p' and 'c' options\n")
            print (inprotocol)
            larg, rarg = inprotocol.split(":")
            largi = int(larg)
            rargi = int(rarg)
            invalid=0
        except ValueError:
            print ('Not a valid number.  Try again. ')
    print("Left: " + larg)
    port.write(larg + "\n")
    print("Right: " +  rarg)
    port.write(rarg + "\n")
