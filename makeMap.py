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
import argparse

# 変数の指定
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
    parser = argparse.ArgumentParser(description='飛行パラメータの指定をここで行う')
    parser.add_argument('-H','--height',default=20)
    parser.add_argument('-L','--height',default=2)
    drone = olympe.Drone("192.168.42.1")
    drone.connect()

    angle = math.pi/4
    set_gimbal(drone=drone,angle=angle)
    time.sleep(2)
    assert drone(TakeOff()).wait().success()
    # 飛行プログラム開始
    drone(moveBy(0,0, -H, 0)).wait().success()
    # drone(extended_move_to(35.615429, 139.299958,40)).wait().success()
    
    for i in range(13):
        # iが偶数の時は左右に動く
        if i%2 == 0:
            for j in range(10):
                if i%4 == 0:
                    drone(moveBy(0,L,0, 0)).wait().success()
                    take_photo(drone)
                    time.sleep(2)
                else:
                    drone(moveBy(0,-L,0, 0)).wait().success()
                    take_photo(drone)
                    time.sleep(2)
        else:
            drone(moveBy(L,0,0,0)).wait().success()
            time.sleep(2)
    assert drone(Landing()).wait().success()


if __name__ == "__main__":
    main()