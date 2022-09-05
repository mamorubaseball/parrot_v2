# -*- coding: UTF-8 -*-
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.Piloting import moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.move import extended_move_to
from olympe.messages.ardrone3.PilotingState import PositionChanged,FlyingStateChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.Piloting import TakeOff
from olympe.messages.ardrone3.GPSSettingsState import HomeChanged

from move import *
from photo import photo
import time
import os
import csv


DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

def up():
    drone = olympe.Drone("192.168.42.1")
    drone.connect()
    assert drone(TakeOff()).wait().success()
    time.sleep(3)
    drone(moveBy(0,0, -2, 0)).wait().success()
    assert drone(Landing()).wait().success()

def test_take_photo():
    drone = olympe.Drone("192.168.42.1")
    drone.connect()
    assert drone(TakeOff()).wait().success()
    os.system('python3 photo.py')
    drone(moveBy(1,0, 0, 0)).wait().success()
    os.system('python3 photo.py')
    assert drone(Landing()).wait().success()

def move_to_get_gps():
    #家の近く:
    # 小金井公園の椅子があるとこ： 35.71628807725536, 139.5167523197069
    #大学の中庭にある木の左側：35.70986171406717, 139.52302521204703
    GPS=[35.70986171406717, 139.52302521204703]
    GPS_DATA=[]
    drone = olympe.Drone("192.168.42.1")
    drone.connect()

    assert drone(TakeOff()).wait().success()

    # getGPS
    drone(GPSFixStateChanged(_policy = 'wait'))
    GPS_DATA.append(drone.get_state(PositionChanged))


    # 飛行プログラム開始
    drone(extended_move_to(GPS[0],GPS[1],2)).wait().success()
    drone(GPSFixStateChanged(_policy = 'wait'))
    GPS_DATA.append(drone.get_state(PositionChanged))

    drone(moveBy(1,0, 0, 0)).wait().success()
    drone(GPSFixStateChanged(_policy = 'wait'))
    GPS_DATA.append(drone.get_state(PositionChanged))
    with open('gps.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(GPS)

    drone(Landing()).wait().success()



def get_state():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    assert drone(TakeOff()).wait().success()
    GPS =[]
    # getGPS
    drone(GPSFixStateChanged(_policy = 'wait'))
    print("======GPS position before move : ", drone.get_state(PositionChanged))
    GPS.append(drone.get_state(PositionChanged))
    drone(moveBy(1,0, 0, 0)).wait().success()
    # getGPS
    drone(GPSFixStateChanged(_policy = 'wait'))
    print("=======GPS position after move : ", drone.get_state(PositionChanged))
    GPS.append(drone.get_state(PositionChanged))
    with open('gps.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(GPS)
    assert drone(Landing()).wait().success()
    drone.disconnect()

def get_state_v2():
    # Connection
    drone = olympe.Drone("192.168.42.1")
    drone.connect()
    # Wait for GPS fix
    drone(GPSFixStateChanged(_policy = 'wait'))

    print("GPS position before take-off :", drone.get_state(HomeChanged))
    
    # Take-off
    drone(TakeOff()).wait()

    print("GPS position after take-off : ", drone.get_state(PositionChanged))

    drone.disconnect()

# https://forum.developer.parrot.com/t/get-gps-position-before-the-take-off/9432/3
if __name__ == "__main__":
    # test_take_photo()
    # get_state()
    move_to_get_gps()