#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import math
import numpy as np
import sys
from time import sleep
from common.serialtalking import BYTE, LONG, FLOAT, INT
from common.serialtalking import SerialTalking
from logs.logger import Logger

# Instructions
SET_VELOCITIES_OPCODE           = 0x10

START_PUREPURSUIT_OPCODE        = 0x11
START_TURNONTHESPOT_OPCODE      = 0x12

SET_OPENLOOP_VELOCITIES_OPCODE  = 0x13

POSITION_REACHED_OPCODE         = 0x14

SET_POSITION_OPCODE	            = 0x15
GET_POSITION_OPCODE	            = 0x16
GET_VELOCITIES_OPCODE           = 0x17

SET_PARAMETER_VALUE_OPCODE      = 0x18
GET_PARAMETER_VALUE_OPCODE      = 0x19

RESET_PUREPURSUIT_OPCODE        = 0x1A
ADD_PUREPURSUIT_WAYPOINT_OPCODE = 0x1B

GET_CODEWHEELS_COUNTERS_OPCODE  = 0x1C
GET_VELOCITIES_WANTED_OPCODE    = 0x1D
GOTO_DELTA_OPCODE               = 0x1E
RESET_PARAMETERS_OPCODE         = 0x1F
SAVE_PARAMETERS_OPCODE          = 0x20
PRINT_PARAMS_OPCODE             = 0x22

START_TURNONTHESPOT_DIR_OPCODE = 0x21

LEFTWHEEL_RADIUS_ID	            = 0x10
LEFTWHEEL_CONSTANT_ID           = 0x11
LEFTWHEEL_MAXPWM_ID             = 0x12
RIGHTWHEEL_RADIUS_ID            = 0x20
RIGHTWHEEL_CONSTANT_ID          = 0x21
RIGHTWHEEL_MAXPWM_ID            = 0x22
LEFTCODEWHEEL_RADIUS_ID	        = 0x40
LEFTCODEWHEEL_COUNTSPERREV_ID   = 0x41
RIGHTCODEWHEEL_RADIUS_ID        = 0x50
RIGHTCODEWHEEL_COUNTSPERREV_ID  = 0x51
ODOMETRY_AXLETRACK_ID           = 0x60
ODOMETRY_SLIPPAGE_ID            = 0x61
VELOCITYCONTROL_AXLETRACK_ID    = 0x80
VELOCITYCONTROL_MAXLINACC_ID    = 0x81
VELOCITYCONTROL_MAXLINDEC_ID    = 0x82
VELOCITYCONTROL_MAXANGACC_ID    = 0x83
VELOCITYCONTROL_MAXANGDEC_ID    = 0x84
VELOCITYCONTROL_SPINSHUTDOWN_ID = 0x85
LINVELPID_KP_ID                 = 0xA0
LINVELPID_KI_ID                 = 0xA1
LINVELPID_KD_ID                 = 0xA2
LINVELPID_MINOUTPUT_ID          = 0xA3
LINVELPID_MAXOUTPUT_ID          = 0xA4
ANGVELPID_KP_ID                 = 0xB0
ANGVELPID_KI_ID                 = 0xB1
ANGVELPID_KD_ID                 = 0xB2
ANGVELPID_MINOUTPUT_ID	        = 0xB3
ANGVELPID_MAXOUTPUT_ID	        = 0xB4
POSITIONCONTROL_LINVELKP_ID     = 0xD0
POSITIONCONTROL_ANGVELKP_ID     = 0xD1
POSITIONCONTROL_LINVELMAX_ID    = 0xD2
POSITIONCONTROL_ANGVELMAX_ID    = 0xD3
POSITIONCONTROL_LINPOSTHRESHOLD_ID  = 0xD4
POSITIONCONTROL_ANGPOSTHRESHOLD_ID  = 0xD5
PUREPURSUIT_LOOKAHEAD_ID        = 0xE0
PUREPURSUIT_LOOKAHEADBIS_ID     = 0xE2


"""
This class acts as an interface between the raspeberry pi and the arduino.
It contains methods for each action of the wheeled base. 
It allows the raspeberry pi to ask the arduino to perform an action via a specific OPCODE.
"""
class WheeledBase():
    #Doc de la classe sur le owncloud
    
    '''
    _DEFAULT = {
        GET_CODEWHEELS_COUNTERS_OPCODE : Deserializer(LONG(0) + LONG(0)),
        POSITION_REACHED_OPCODE : Deserializer(BYTE(0) + BYTE(0)),
        GET_VELOCITIES_WANTED_OPCODE : Deserializer(FLOAT(0) + FLOAT(0)),
        GET_POSITION_OPCODE : Deserializer(FLOAT(0) + FLOAT(0)+ FLOAT(0)),
        GET_VELOCITIES_OPCODE :  Deserializer(FLOAT(0) + FLOAT(0)),
        GET_PARAMETER_VALUE_OPCODE : Deserializer(LONG(0) + LONG(0))

    }
    '''

    FORWARD = 1
    BACKWARD = 2
    NO_DIR = 0

    LATCH_TIMESTEP = 0.2

    class Parameter():
        def __init__(self, parent, id, type):
            self.parent = parent
            self.id   = id
            self.type = type
        def get(self): return self.parent.get_parameter_value(self.id, self.type)
        def set(self, value): self.parent.set_parameter_value(self.id, value, self.type)

    def __init__(self, uuid='wheeledbase'):
        if 'linux' in sys.platform:
            self.wheeledbase = SerialTalking("/dev/arduino/"+uuid)
        else:
            self.wheeledbase = SerialTalking(uuid)

        self.log = Logger("wheeledbase")
        self.log.init()

        self.left_wheel_radius              = WheeledBase.Parameter(self, LEFTWHEEL_RADIUS_ID, FLOAT)
        self.left_wheel_constant            = WheeledBase.Parameter(self, LEFTWHEEL_CONSTANT_ID, FLOAT)
        self.left_wheel_maxPWM              = WheeledBase.Parameter(self, LEFTWHEEL_MAXPWM_ID, FLOAT)

        self.right_wheel_radius             = WheeledBase.Parameter(self, RIGHTWHEEL_RADIUS_ID, FLOAT)
        self.right_wheel_constant           = WheeledBase.Parameter(self, RIGHTWHEEL_CONSTANT_ID, FLOAT)
        self.right_wheel_maxPWM             = WheeledBase.Parameter(self, RIGHTWHEEL_MAXPWM_ID, FLOAT)

        self.left_codewheel_radius          = WheeledBase.Parameter(self, LEFTCODEWHEEL_RADIUS_ID, FLOAT)
        self.left_codewheel_counts_per_rev  = WheeledBase.Parameter(self, LEFTCODEWHEEL_COUNTSPERREV_ID, LONG)

        self.right_codewheel_radius         = WheeledBase.Parameter(self, RIGHTCODEWHEEL_RADIUS_ID, FLOAT)
        self.right_codewheel_counts_per_rev = WheeledBase.Parameter(self, RIGHTCODEWHEEL_COUNTSPERREV_ID, LONG)

        self.codewheels_axletrack           = WheeledBase.Parameter(self, ODOMETRY_AXLETRACK_ID, FLOAT)
        self.odometry_slippage              = WheeledBase.Parameter(self, ODOMETRY_SLIPPAGE_ID, FLOAT)

        self.wheels_axletrack               = WheeledBase.Parameter(self, VELOCITYCONTROL_AXLETRACK_ID, FLOAT)
        self.max_linacc                     = WheeledBase.Parameter(self, VELOCITYCONTROL_MAXLINACC_ID, FLOAT)
        self.max_lindec                     = WheeledBase.Parameter(self, VELOCITYCONTROL_MAXLINDEC_ID, FLOAT)
        self.max_angacc                     = WheeledBase.Parameter(self, VELOCITYCONTROL_MAXANGACC_ID, FLOAT)
        self.max_angdec                     = WheeledBase.Parameter(self, VELOCITYCONTROL_MAXANGDEC_ID, FLOAT)
        self.spin_shutdown                  = WheeledBase.Parameter(self, VELOCITYCONTROL_SPINSHUTDOWN_ID, BYTE)

        self.linvel_KP                      = WheeledBase.Parameter(self, LINVELPID_KP_ID, FLOAT)
        self.linvel_KI                      = WheeledBase.Parameter(self, LINVELPID_KI_ID, FLOAT)
        self.linvel_KD                      = WheeledBase.Parameter(self, LINVELPID_KD_ID, FLOAT)

        self.angvel_KP                      = WheeledBase.Parameter(self, ANGVELPID_KP_ID, FLOAT)
        self.angvel_KI                      = WheeledBase.Parameter(self, ANGVELPID_KI_ID, FLOAT)
        self.angvel_KD                      = WheeledBase.Parameter(self, ANGVELPID_KD_ID, FLOAT)

        self.linpos_KP                      = WheeledBase.Parameter(self, POSITIONCONTROL_LINVELKP_ID, FLOAT)
        self.angpos_KP                      = WheeledBase.Parameter(self, POSITIONCONTROL_ANGVELKP_ID, FLOAT)
        self.max_linvel                     = WheeledBase.Parameter(self, POSITIONCONTROL_LINVELMAX_ID, FLOAT)
        self.max_angvel                     = WheeledBase.Parameter(self, POSITIONCONTROL_ANGVELMAX_ID, FLOAT)
        self.linpos_threshold               = WheeledBase.Parameter(self, POSITIONCONTROL_LINPOSTHRESHOLD_ID, FLOAT)
        self.angpos_threshold               = WheeledBase.Parameter(self, POSITIONCONTROL_ANGPOSTHRESHOLD_ID, FLOAT)

        self.lookahead                      = WheeledBase.Parameter(self, PUREPURSUIT_LOOKAHEAD_ID, FLOAT)
        self.lookaheadbis                   = WheeledBase.Parameter(self, PUREPURSUIT_LOOKAHEADBIS_ID, FLOAT)
        self.x                              = 0
        self.y                              = 0
        self.theta                          = 0
        self.previous_measure               = 0
        self.direction = self.NO_DIR
        self.final_angle = 0

        self.latch = None
        self.latch_time = None

    def set_openloop_velocities(self, left, right):
        self.wheeledbase.order(SET_OPENLOOP_VELOCITIES_OPCODE, FLOAT(left), FLOAT(right))

    def get_codewheels_counter(self):
        left, right = self.wheeledbase.request(GET_CODEWHEELS_COUNTERS_OPCODE, LONG, LONG)
        return left, right

    def set_velocities(self, linear_velocity, angular_velocity):
        self.wheeledbase.order(SET_VELOCITIES_OPCODE, FLOAT(linear_velocity), FLOAT(angular_velocity))

    def purepursuit(self, waypoints, direction='forward', finalangle=None, lookahead=None, lookaheadbis=None, linvelmax=None, angvelmax=None, **kwargs):
        if len(waypoints) < 2:
            raise ValueError('not enough waypoints')
        self.wheeledbase.order(RESET_PUREPURSUIT_OPCODE)
        for x, y in waypoints:
            self.wheeledbase.order(ADD_PUREPURSUIT_WAYPOINT_OPCODE, FLOAT(x), FLOAT(y))
        if lookahead is not None:
            self.set_parameter_value(PUREPURSUIT_LOOKAHEAD_ID, lookahead, FLOAT)
        if lookaheadbis is not None:
            self.set_parameter_value(PUREPURSUIT_LOOKAHEADBIS_ID, lookaheadbis, FLOAT)
        if linvelmax is not None:
            self.set_parameter_value(POSITIONCONTROL_LINVELMAX_ID, linvelmax, FLOAT)
        if angvelmax is not None:
            self.set_parameter_value(POSITIONCONTROL_ANGVELMAX_ID, angvelmax, FLOAT)
        if finalangle is None:
            finalangle = math.atan2(waypoints[-1][1] - waypoints[-2][1], waypoints[-1][0] - waypoints[-2][0])
        self.direction = {'forward':self.FORWARD, 'backward':self.BACKWARD}[direction]
        self.final_angle = finalangle
        self.log.sendLog("start purepursuit")
        self.wheeledbase.order(START_PUREPURSUIT_OPCODE, BYTE({'forward':0, 'backward':1}[direction]), FLOAT(finalangle))

    def start_match(self):
        START_MATCH_OPCODE=0x23
        self.wheeledbase.order(START_MATCH_OPCODE)

    def purepursuit_stop(self, waypoints,sensors, direction='forward', finalangle=None, lookahead=None, lookaheadbis=None,
                    linvelmax=None, angvelmax=None):
        self.purepursuit(waypoints,direction,finalangle,lookahead,lookaheadbis,linvelmax,angvelmax)
        while not self.isarrived(raiseSpinUrgency=False):
            m=np.min(sensors.get_all_sensors()[0:4])
            print(self.get_position(),m)
            if (m < 500 or np.min(sensors.get_all_sensors()[4:]) < 300):
                interrupt = True
                self.stop()
                self.log.sendLog("arret")

        self.log.sendLog("ARRIVE")
    def start_purepursuit(self):
        self.wheeledbase.order(START_PUREPURSUIT_OPCODE, BYTE({self.NO_DIR:0, self.FORWARD:0, self.BACKWARD:1}[self.direction]),
                  FLOAT(self.final_angle))

    def turnonthespot(self, theta, direction=None, way='forward'):
        if direction is None:
            self.wheeledbase.order(START_TURNONTHESPOT_OPCODE, FLOAT(theta), BYTE({'forward':0, 'backward':1}[way]))
        else:
            self.wheeledbase.order(START_TURNONTHESPOT_DIR_OPCODE, FLOAT(theta), BYTE({'clock':0, 'trig':1}[direction]))

    def isarrived(self,raiseSpinUrgency=True):
        isarrived, spinurgency = self.wheeledbase.request(POSITION_REACHED_OPCODE, BYTE, BYTE)
        if bool(spinurgency)and raiseSpinUrgency:
            raise RuntimeError('spin urgency')
        return bool(isarrived)

    def get_velocities_wanted(self,real_output=False):
        return self.wheeledbase.request(GET_VELOCITIES_WANTED_OPCODE, FLOAT, FLOAT, send_args=[BYTE(int(real_output))])

    def wait(self, timestep=0.1, timeout=200, command=None, **kwargs):
        init_time = time.time()
        while not self.isarrived(**kwargs):
            time.sleep(timestep)
            if (time.time()-init_time>timeout) and (not command is None):
                print("RESCUE wheeledbase !")
                command()
                time.sleep(timestep)

    def goto_delta(self, x, y):
        self.wheeledbase.order(GOTO_DELTA_OPCODE, FLOAT(x),  FLOAT(y))

    def goto(self, x, y, theta=None, direction=None, finalangle=None, lookahead=None, lookaheadbis=None, linvelmax=None, angvelmax=None, **kwargs):
        # Compute the preferred direction if not set
        if direction is None:
            x0, y0, theta0 = self.get_position()
            if math.cos(math.atan2(y - y0, x - x0) - theta0) >= 0:
                direction = 'forward'
            else:
                direction = 'backward'

        # Go to the setpoint position
        self.purepursuit([(x0,y0), (x, y)], direction, finalangle, lookahead, lookaheadbis, linvelmax, angvelmax)
        #self.wait(**kwargs)
        while not self.isarrived(raiseSpinUrgency=False):
            pass
        # Get the setpoint orientation
        if theta is not None:
            self.turnonthespot(theta)
            self.wait(**kwargs)

    def goto_waypoints(self, waypoints, theta=None, direction=None, finalangle=None, lookahead=None, lookaheadbis=None, linvelmax=None, angvelmax=None, **kwargs):
        # Compute the preferred direction if not set
        if direction is None:
            x0, y0, theta0 = self.get_position()
            if math.cos(math.atan2(waypoints[0][1] - y0, waypoints[0][0] - x0) - theta0) >= 0:
                direction = 'forward'
            else:
                direction = 'backward'

        # Go to the setpoint position
        waypoints.insert(0,(x0,y0))
        self.purepursuit(waypoints, direction, finalangle, lookahead, lookaheadbis, linvelmax, angvelmax)
        #self.wait(**kwargs)
        while not self.isarrived(raiseSpinUrgency=True):
            pass
        # Get the setpoint orientation
        if theta is not None:
            self.turnonthespot(theta)
            self.wait(**kwargs)

    def goto_stop(self, x, y,sensors, theta=None, direction=None, finalangle=None, lookahead=None, lookaheadbis=None, linvelmax=None, angvelmax=None, **kwargs):
        """if(sensors is None):
            print("None")
            self.goto(x,y,theta=theta,finalangle=finalangle)
            return"""
        print(sensors.get_all_sensors())
        # Compute the preferred direction if not set
        x0, y0, theta0 = self.get_position()
        if direction is None:
            if math.cos(math.atan2(y - y0, x - x0) - theta0) >= 0:
                direction = 'forward'
            else:
                direction = 'backward'

        # Go to the setpoint position
        self.purepursuit([self.get_position()[0:2], (x, y)], direction, finalangle, lookahead, lookaheadbis, linvelmax, angvelmax)
        interrupt=False
        try:
            while not self.isarrived(raiseSpinUrgency=False):
                sen = sensors.get_all_sensors()

                if(np.min(sen[0:4])<300 or np.min(sen[4:])<500 or sen[5]<600):
                    interrupt=True
                    self.stop()
                    print("arret:",sen,sensors.get_sensor1_range())
                elif interrupt:
                    print("reprise:",sen)
                    interrupt=False
                    self.log.sendLog("Reprise")
                    
                    x0, y0, theta0 = self.get_position()
                    if direction is None:
                        if math.cos(math.atan2(y - y0, x - x0) - theta0) >= 0:
                            direction = 'forward'
                        else:
                            direction = 'backward'
                    print([(x0,y0), (x, y)],finalangle)
                    self.purepursuit([(x0,y0), (x, y)], direction, finalangle, lookahead, lookaheadbis, linvelmax, angvelmax)

            
            self.log.sendLog("ARRIVE")
            
            # Get the setpoint orientation
            if theta is not None:
                if(theta<0):
                    theta+=2*math.pi
                rPos=self.get_position()
                radiusRobot=370
                ang=rPos[2]%(2*math.pi)
                
                #fait en sorte que |ang-theta|<pi pr trouver le sens du robot
                if(theta-ang>math.pi):
                    theta-=2*math.pi
                if(ang-theta>math.pi):
                    ang-=2*math.pi
                print(ang,theta)
                trigo=theta>ang#va ds le sens trigo
                print(trigo)
                #le rbot va bouger ds l'intervalle [a;b] inclus ds [-pi;2pi]
                a=min(ang,theta)
                b=max(ang,theta)

                #optimise le x et y (condition optimilité ss contrainte donne borne du problème)
                xmin=math.cos(theta)*radiusRobot+rPos[0]
                xmax=xmin
                ymin=math.sin(theta)*radiusRobot+rPos[1]
                ymax=ymin
                #test x-
                if(a<=-math.pi or (a<math.pi and b >math.pi)):
                    xmin=-radiusRobot+rPos[0]
                if(b>=math.pi*2 or (a<0 and b>0)):
                    xmax=radiusRobot+rPos[0]
                if((a<math.pi/2 and b >math.pi/2)):
                    ymax=radiusRobot+rPos[1]
                if((a<3*math.pi/2 and b >3*math.pi/2) or (a<-math.pi/2 and b >-math.pi/2)):
                    ymin=radiusRobot+rPos[1]
                
                #print(trigo,ang,theta)
                #print("     ",xmin,xmax,ymin,ymax)    
                if(xmin<0 or xmax>3000 or ymin<0 or ymax>2000):
                    trigo =not trigo
                
                #print(trigo,['clock','trig'][trigo])
                while(np.min(sensors.get_all_sensors())<600):
                    print("sensors detection")
                    sleep(0.1)
                print("fin trigo:",trigo,rPos)
                self.turnonthespot(theta,direction=['clock','trig'][trigo])
                print("fin commande turn on the spot")
                self.wait(**kwargs)

        except RuntimeError:
            self.goto_stop(x, y,sensors, theta, direction, finalangle, lookahead, lookaheadbis, linvelmax, angvelmax)
            print("FUUUUCK runtime")
        except TimeoutError:
            print("FUUUUUUUUUCk")
            self.wheeledbase.disconnect()
            time.sleep(0.5)
            self.wheeledbase.connect()

    def stop(self):
        self.set_openloop_velocities(0, 0)

    def set_position(self, x, y, theta):
        self.wheeledbase.order(SET_POSITION_OPCODE, FLOAT(x), FLOAT(y), FLOAT(theta))

    def reset(self):
        self.set_position(0, 0, 0)

    def print_params(self):
        self.wheeledbase.order(PRINT_PARAMS_OPCODE)

    def get_position(self):
        self.x, self.y, self.theta = self.wheeledbase.request(GET_POSITION_OPCODE, FLOAT, FLOAT, FLOAT)
        self.previous_measure = time.time()
        return self.x, self.y, self.theta

    def get_position_latch(self):
        if self.latch is None or time.time() - self.latch_time > self.LATCH_TIMESTEP:
            self.latch = self.get_position()
            self.latch_time = time.time()
        return self.latch

    def get_position_previous(self, delta):
        if time.time()-self.previous_measure>delta:
            self.get_position()
        return self.x, self.y, self.theta

    def get_velocities(self):
        linvel, angvel = self.wheeledbase.request(GET_VELOCITIES_OPCODE, FLOAT, FLOAT)
        return linvel, angvel

    def set_parameter_value(self, id, value, valuetype):
        self.wheeledbase.order(SET_PARAMETER_VALUE_OPCODE, BYTE(id), valuetype(value))
        time.sleep(0.01)

    def get_parameter_value(self, id, valuetype):
        value = self.wheeledbase.request(GET_PARAMETER_VALUE_OPCODE, valuetype, send_args=[BYTE(id)])
        return value

    def reset_parameters(self):
        self.wheeledbase.order(RESET_PARAMETERS_OPCODE)

    def save_parameters(self):
        self.wheeledbase.order(SAVE_PARAMETERS_OPCODE)

    def publish_logs(self):
        pass