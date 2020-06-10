#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File: amapTheorem.py
@Project: amap
@Desc: 判定点是否在区域内的算法
@Time: 2020/05/27 16:06:59
@Author: guojie.bian (guojie.bian@drcnet.com.cn)
@Last Modified: 2020/05/27 16:06:59
@Modified By: guojie.bian (guojie.bian@drcnet.com.cn>)
@Version: 1.0
@License: Copyright(C) 2019 - 2020 DRCNET, SRIT DRCNET
"""



import math
import numpy as np
from matplotlib.path import Path


class Point:
    """点坐标"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def in_box(point, maxP, minP):
    """
    判断点是否在多边形的外包矩形中 
    point: 待判定的坐标点 
    maxP: 最大坐标点 
    minP: 最小坐标点 
    """
    return (minP.x <= point.x <= maxP.x) and (minP.y <= point.y <= maxP.y)

def in_polyline(point, polyline):
    """
    根据经纬度，判断是否在区域内 
    point: 待判定的坐标点 
    polyline: 边界坐标
    """
    lats = []
    lngs = []
    for pol in polyline:
        lats.append(pol.x)
        lngs.append(pol.y)
    xc = np.array(lats)
    yc = np.array(lngs)
    xycrop=np.vstack((xc,yc)).T
    pth=Path(xycrop,closed=False)
    mask=pth.contains_points([[point.x,point.y]])
    if mask:
        return True
    return False
