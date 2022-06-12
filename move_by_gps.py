from __future__ import print_function
from ast import main  # python2/3 compatibility for the print function
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveTo, moveBy, Circle, PCMD
import pandas as pd
import os, csv, time, tempfile
from photo import take_photo
from set_gimbal import set_gimbal

olympe.log.update_config({"loggers": {"olympe": {"level": "INFO"}}})
DRONE_IP = "192.168.42.1"
SKYCTRL_IP = "192.168.53.1"
DRONE_SSID = os.environ.get("DRONE_SSID", "Anafi_PC_000000")
DRONE_SECURITY_KEY = os.environ.get("DRONE_SECURITY_KEY", "")
DRONE_SERIAL = os.environ.get("DRONE_SERIAL", "000000")

def move_to(drone):
    assert drone(TakeOff()).wait().success()
    df = pd.read_csv('lat_lon_10data.csv')
    for index,rows in df.iterrows():
        lat = rows.lat
        lon = rows.lon
        h = rows.h
        time.sleep(1)
        drone(moveTo(latitude=lat, longitude=lon, altitude=h,max_horizontal_speed=0.1))
        time.sleep(1)

def main(drone):
    move_to(drone)
    set_gimbal(drone,30)
    #take_photo()
    take_photo(drone)
    #landing
    assert drone(Landing()).wait().success()

if __name__ == '__main__':
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    main(drone)