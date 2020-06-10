#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File: amapMaxMin.py
@Project: amap
@Desc: 第三步：计算出province, city, district表中的最大最小边界经纬度，并填充到数据库中
@Time: 2020/04/30 15:13:03
@Author: wuwenrufeng (wuwenrufeng@163.com)
@Last Modified: 2020/04/30 15:13:06
@Modified By: wuwenrufeng (wuwenrufeng@163.com)
@Version: 1.0
@License: Copyright(C) 2019 - 2020 Borland
"""



from pony.orm import commit, db_session, select, delete
from util.models import Province, City, District, db


class MaxMin:
    def trimPolyline(self, model):
        """
        将由多个区域组成的行政区分离出来
        model: 行政区Entity
        """
        for row in model.select():
            polylineRaw = row.polyline
            if '|' in polylineRaw:
                polylines = polylineRaw.split('|')
                for polyline in polylines:
                    model(name=row.name, adcode=row.adcode, center=row.center, polyline=polyline)
                # 删除包含所有区域的原始记录
                delete(m for m in model if m.id == row.id)

    def calculate(self, polyline):
        """
        计算当前边界坐标中的最大坐标点和最小坐标点
        polyline: 边界坐标
        return: 最大坐标点,最小坐标点
        """
        # ['116.58289,39.623118';'116.58289,39.623118';...]
        polylines = polyline.split(';')
        # 所有经度纬度
        lats=lons = []
        for polyline in polylines:
            lat,lon = polyline.split(',')
            lats.append(float(lat))
            lons.append(float(lon))
        # 多边形的最大经纬度
        maxPoint = str(max(lats)) + ',' + str(max(lons))
        # 多边形的最小经纬度
        minPoint = str(min(lats)) + ',' + str(min(lons))
        return maxPoint, minPoint

    @db_session
    def main(self, model):
        """
        model: 行政区Entity
        """
        # 行政区区域分离
        self.trimPolyline(model)
        for row in model.select():
            max_point, min_point = self.calculate(row.polyline)
            # 更新行政区表中的最大最小坐标点 
            model[row.id].set(max_point=max_point, min_point=min_point)
            commit()


if __name__ == '__main__':
    maxMin = MaxMin()
    for model in (Province, City, District):
        maxMin.main(model)
