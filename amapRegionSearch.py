#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File: amapRegionSearch.py
@Project: amap
@Desc: 查询给定坐标点所属的行政区域信息
@Time: 2020/05/14 13:42:20
@Author: wuwenrufeng (wuwenrufeng@163.com)
@Last Modified: 2020/05/14 13:42:23
@Modified By: wuwenrufeng (wuwenrufeng@163.com)
@Version: 1.0
@License: Copyright(C) 2019 - 2020 Borland
"""



import time

from pony.orm import commit, db_session, left_join, select

from amapTheorem import Point, in_box, in_polyline
from util.models import City, District, Province, db


class RegionSearch:
    def to_point(self, pointStr):
        """
        将字符串形式的坐标('x,y')转换为Point对象 
        pointStr: 字符串形式的坐标点 
        return: Point对象 
        """
        p = pointStr.split(',')
        return Point(float(p[0]), float(p[1]))

    @db_session
    def box_filter(self, point, sql):
        """
        外包矩形过滤 
        point: 坐标点 
        sql: mysql查询语句 
        return: 在外包矩形内的所有行政区主键的列表
        """
        result = []
        for row in db.select(sql):
            if in_box(point, self.to_point(row.max_point), self.to_point(row.min_point)):
                result.append((row.id,row.name,row.adcode,row.polyline))
        return result

    def polyline_filter(self, point, boxResult):
        """
        区域边界过滤 
        point: 坐标点 
        boxResult: 外包矩形过滤后的结果集[(pk,name,adcode,polyline),]
        return: 筛选后的行政区列表
        """
        result = []
        for boxR in boxResult:
            polyline = boxR[-1]
            polylines = polyline.split(';')
            polylineList = []
            for polyline in polylines:
                polylineList.append(self.to_point(polyline))
            if in_polyline(point, polylineList):
                result.append(boxR)
        return result
    
    def filter(self, point):
        """
        查询过滤 
        point: 坐标点 
        return: 省市区信息
        """
        result = {
            'province': ('', ''),
            'city': ('', ''),
            'district': ('', '')
        }

        # 省级
        sql = 'select id,name,adcode,polyline,max_point,min_point from province'
        provinceBoxs = self.box_filter(point, sql)
        if len(provinceBoxs) == 1:
            provinceContains = provinceBoxs
            result['province'] = provinceBoxs[0][1:-1]
        else:
            provinceContains = self.polyline_filter(point, provinceBoxs)
            if provinceContains:
                result['province'] = provinceContains[0][1:-1]
            else:
                provinceContains = provinceBoxs

        # 市级
        for provinceContain in provinceContains:
            adcode = provinceContain[-2]
            sql = 'select id,name,adcode,polyline,max_point,min_point from city where adcode>=%s and adcode<%s'% (adcode, adcode+10000)
            cityBoxs = self.box_filter(point, sql)
            if len(cityBoxs) == 1:
                cityContains = cityBoxs
                result['province'] = provinceContain[1:-1]
                result['city'] = cityBoxs[0][1:-1]
            else:
                cityContains = self.polyline_filter(point, cityBoxs)
                if cityContains:
                    result['province'] = provinceContain[1:-1]
                    result['city'] = cityContains[0][1:-1]
                else:
                    cityContains = cityBoxs
            # 区级
            for cityContain in cityContains:
                adcode = cityContain[-2]
                sql = 'select id,name,adcode,polyline,max_point,min_point from district where adcode>=%s and adcode<%s'% (adcode, adcode+100)
                districtBoxs = self.box_filter(point, sql)
                if len(districtBoxs) == 1:
                    result['city'] = cityContain[1:-1]
                    result['district'] = districtBoxs[0][1:-1]
                    return result
                else:
                    districtContains = self.polyline_filter(point, districtBoxs)
                    if districtContains:
                        result['city'] = cityContain[1:-1]
                        result['district'] = districtContains[0][1:-1]
                        return result

        province = result['province'][0]
        district = result['district'][0]
        if province=='' and  not district=='' :
            districtAdcode = district[2]
            cityAdcode = districtAdcode // 100 *100
            provinceAdcode = districtAdcode // 10000 *10000
            sql = 'SELECT province.id,province.name,province.adcode,city.id,city.name,city.adcode,district.id,district.name,district.adcode FROM district LEFT JOIN city on city.adcode=%s LEFT JOIN province ON province.adcode=%s WHERE district.adcode=%s'% (cityAdcode, provinceAdcode, districtAdcode)
            row = db.select(sql)[0]
            result['province'], result['city'], result['district'] = row[:3], row[3:6], row[6:]
        return result

    def search(self, pointStr):
        """
        查询 
        pointStr: 字符串形式的坐标点 
        return: 查询到的省市区信息
        """
        point = self.to_point(pointStr)
        result = self.filter(point)
        return result

    @db_session 
    def test(self):
        """
        利用数据库中的区信息进行自测 
        结果：
            一共有2822个地区
            正确匹配了2777次
            正确率0.996811
        """
        rows = select((d.adcode, d.center) for d in District)
        num = 0
        for row in rows:
            districtAdcode = row[0]
            center = row[1]
            result = self.search(center)
            province = result['province'][0]
            city = result['city'][0]
            district = result['district'][0]
            print('搜索结果：省: %s'% province, ' 市: %s'% city, ' 区: %s'% district)
            cityAdcode = districtAdcode // 100 *100
            provinceAdcode = districtAdcode // 10000 *10000
            sql = 'SELECT province.name,city.name,district.name FROM district LEFT JOIN city on city.adcode=%s LEFT JOIN province ON province.adcode=%s WHERE district.adcode=%s'% (cityAdcode, provinceAdcode, districtAdcode)
            newRows = db.select(sql)[0]
            raw_province, raw_city, raw_district = newRows
            print('实际内容：省: %s'% raw_province, ' 市: %s'% raw_city, ' 区: %s'% raw_district)
            if province == raw_province and city == raw_city and district == raw_district:
                num += 1
            else:
                print(province)
        total = len(rows)
        print('*'*40)
        print('一共有%s个地区'% total)
        print('正确匹配了%s次'% num)
        print('正确率%f'% (num/total))
        print('*'*40)

if __name__ == '__main__':
    regionSearch = RegionSearch()
    pointStr = '113.3881,23.126796'
    start = time.time()
    result = regionSearch.search(pointStr) 
    print(result)
    print('total cost of time is %.2fs'% (time.time() - start))
    # regionSearch.test()
