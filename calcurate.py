from tkinter import X
from unicodedata import name
import pandas as pd
import math
import os, csv, time, tempfile

#多摩キャンパス白い旗が目印。
start = [35.61512787299106, 139.2997882319244, 1]

def calcurate(pre,to):
    lat1,log1,alt1=pre[0],pre[1],pre[2]
    lat2,log2,alt2=to[0],to[1],to[2]
    disctance=get_distance(lat1,log1,lat2,log2,8)
    direction=get_direction(lat1,log1,lat2,log2)
    x=disctance*math.cos(math.radians(direction))
    y=disctance*math.sin(math.radians(direction))
    z=0
    if x>5:x=5
    elif x<-5:x=-5
    if y>5:y=5
    elif y<-5:y=-5
    return x,y,z,direction

#ソース元：
#モジュールがあるgeopy: https://h-memo.com/python-geopy-distance
def get_distance(lat1,log1,lat2,log2,precision):
    distance=0
    if abs(lat1-lat2)<0.00001 and abs(log1-log2)<0.00001:
        distance=0
    else:
        lat1=lat1*math.pi/180
        lat2=lat2*math.pi/180
        log1=log1*math.pi/180
        log2=log2*math.pi/180
        A = 6378137
        B = 6356755
        F = (A - B) / A
        P1=math.atan((B/A)*math.tan(lat1))
        P2=math.atan((B/A)*math.tan(lat2))
        X=math.acos(math.sin(P1)*math.sin(P2)+math.cos(P1)*math.cos(P2)*math.cos(log1-log2))
        L=(F/8)*((math.sin(X)-X)*math.pow((math.sin(P1)+math.sin(P2)),2)/math.pow(math.cos(X/2),2)-(math.sin(X)-X)*math.pow(math.sin(P1)-math.sin(P2),2)/math.pow(math.sin(X),2))
        distance = A * (X + L)
        decimal_no = math.pow(10, precision)
        distance = round(decimal_no * distance / 1) / decimal_no
        return distance

def get_direction(lat1,log1,lat2,log2):
    Y = math.cos(log2 * math.pi / 180) * math.sin(lat2 * math.pi / 180 - lat1 * math.pi / 180)
    X = math.cos(log1 * math.pi / 180) * math.sin(log2 * math.pi / 180) - math.sin(log1 * math.pi / 180) * math.cos(
        log2 * math.pi / 180) * math.cos(lat2 * math.pi / 180 - lat1 * math.pi / 180)
    dirE0 = 180 * math.atan2(Y, X) / math.pi;#東向けがゼロ
    if dirE0<0:
        dirE0+=360
    dirN0=(dirE0+90)%360
    dirN0=dirN0/360*math.pi
    
    return dirN0 #北を基準に角度を決める

def x_y_z_direction_csv():
    df = pd.read_csv('CSV/lat_lon_10data.csv')
    ans_list = []
    for index,row in df.iterrows():
        to = [row.lat,row.lon,row.h]
        x,y,z,direction=calcurate(start,to)
        start = to

        ans_list.append([x,y,z,direction])

    df = pd.DataFrame(ans_list,columns=['x','y','z','direction'])
    df.to_csv('x_y_Z_direction.csv')

x_y_z_direction_csv()