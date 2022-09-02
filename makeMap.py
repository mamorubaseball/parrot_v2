# 多摩キャンパスド3D地図作成
# -*- coding: UTF-8 -*-
import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.move import extended_move_to
import os
from olympe.messages.ardrone3.Piloting import moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from photo import take_photo
from olympe.messages import gimbal
import math

# 4つの変数
# GPS1:35.615429, 139.299958
# GPS2:35.61503573425537, 139.299653451925
# h = 40m
# L = 5m
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
H = 40
L = 5
GPS_1=(35.615429, 139.299958)
GPS_2=(35.61503573425537, 139.299653451925)

def set_gimbal(drone,angle):
    drone(gimbal.set_target(
    gimbal_id=0,
    control_mode="position",
    yaw_frame_of_reference="none",   # None instead of absolute
    yaw=0.0,
    pitch_frame_of_reference="absolute",
    pitch=-angle,
    roll_frame_of_reference="none",     # None instead of absolute
    roll=0.0,
)).wait()

def main():
    drone = olympe.Drone("192.168.42.1")
    drone.connect()
    angle = math.pi/4
    set_gimbal(drone=drone,angle=angle)
    time.sleep(2)
    assert drone(TakeOff()).wait().success()
    # 飛行プログラム開始
    drone(moveBy(0,0, -H, 0)).wait().success()
    drone(extended_move_to(35.615429, 139.299958,40)).wait().success()
    
    for i in range(13):
        for j in range(10):
            if i%2 == 0:
                if i%4 == 0:l = L
                else:l = -L
                drone(moveBy(0,l,0, 0)).wait().success()
                take_photo(drone)
                time.sleep(2)
            #iが奇数の時は5m前に進む
            elif i%2 == 1:
                drone(moveBy(L,0,0,0)).wait().success()
                time.sleep(2)
    assert drone(Landing()).wait().success()

if __name__ == "__main__":
    main()