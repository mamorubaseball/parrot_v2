# 多摩キャンパスド3D地図作成
# -*- coding: UTF-8 -*-
import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
import os
from olympe.messages.ardrone3.Piloting import moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from photo import take_photo

# 4つの変数
# GPS1:35.615429, 139.299958
# GPS2:
# h = 40m
# L = 5m