#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File: amapPopulate.py
@Project: amap
@Desc: 第二步：高德地图-补充市、区的边界信息 (ps: 高德不提供有关街道的边界顶点信息)
@Time: 2020/05/26 17:06:19
@Author: wuwenrufeng (wuwenrufeng@163.com)
@Last Modified: 2020/05/26 17:06:19
@Modified By: wuwenrufeng (wuwenrufeng@163.com)
@Version: 1.0
@License: Copyright(C) 2019 - 2020 Borland
"""



from pony.orm import commit, db_session, select

from amapInit import MapApi
from util.models import City, District, db
from util.settings import KEY


class MapApiPopu(MapApi):
    """ 继承amapInit中的MapApi """

    def parse(self, pk, districts):
        """
        解析行政区查询结果并入库
        pk: pk 
        districts: 行政区列表
        """
        for district in districts:
            polyline = district.get('polyline', '')
            level = district.get('level', '')
            if level == 'city':
                City[pk].set(polyline=polyline)
            if level == 'district':
                District[pk].set(polyline=polyline)

    @db_session
    def main(self, model):
        """
        model: 行政区Entity
        """
        for row in select(m for m in model if m.polyline==''): 
            # 查询行政区信息
            result = self.query(keyword=row.adcode, subdistrict=0)
            if result:
                districts = result['districts']
                self.parse(row.id, districts)
                commit()

if __name__ == '__main__':
    popu = MapApiPopu(key=KEY)
    for model in (City, District):
        popu.main(model)
