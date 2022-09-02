# -*- coding: UTF-8 -*-
from moveby import main
import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
import os
from olympe.messages.ardrone3.Piloting import moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from move import *

DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

def main():
    drone = olympe.Drone("192.168.42.1")
    drone.connection()
    assert drone(TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)).wait().success()
    Down(-2)
    Landing()

if __name__ == "__main__":
    main()


    