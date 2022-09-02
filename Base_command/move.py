# -*- coding: UTF-8 -*-
import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
import os
from olympe.messages.ardrone3.Piloting import moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged


DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")


def main():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    time.sleep(10)
    
def Left(d):
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    drone(moveBy(0,d, 0, 0)
              >> FlyingStateChanged(state="hovering", _timeout=3)).wait().success()

def Right(d):
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    drone(moveBy(0,d, 0, 0)
              >> FlyingStateChanged(state="hovering", _timeout=3)).wait().success()

def Down(h):
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    drone(moveBy(0,0, h, 0)
              >> FlyingStateChanged(state="hovering", _timeout=3)).wait().success()

def Landing():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    assert drone(Landing()).wait().success()
    time.sleep(10)

if __name__ == "__main__":
    main()
