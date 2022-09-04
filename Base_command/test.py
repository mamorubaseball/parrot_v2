# -*- coding: UTF-8 -*-
from moveby import main
import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
import os
from olympe.messages.ardrone3.Piloting import moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from move import *
from photo import take_photo
from olympe.messages.move import extended_move_to
from olympe.messages.ardrone3.PilotingState import PositionChanged
from olympe.messages.ardrone3.GPSSettingsState import HomeChanged

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
    take_photo()
    time.sleep(3)
    assert drone(Landing()).wait().success()

def move_to():
    #家の近く:
    # 小金井公園の椅子があるとこ： 35.71628807725536, 139.5167523197069
    #大学の中庭にある木の左側：35.70986876013675, 139.52304838602245
    GPS=[35.615429, 139.299958]

    drone = olympe.Drone("192.168.42.1")
    drone.connect()
    assert drone(TakeOff()).wait().success()
    # 飛行プログラム開始
    drone(extended_move_to(GPS[0],GPS[1],0)).wait().success()

def get_state():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    print("Drone = ", drone.get_state())
    print("GPS position after take-off : ", drone.get_state(PositionChanged))
    drone.disconnect()

# https://forum.developer.parrot.com/t/get-gps-position-before-the-take-off/9432/3
# 
if __name__ == "__main__":
    # test_take_photo()
    get_state()



    