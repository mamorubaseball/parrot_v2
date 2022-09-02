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

if __name__ == "__main__":
    test_take_photo()
    


    