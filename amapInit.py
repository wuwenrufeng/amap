#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File: amapInit.py
@Project: amap
@Desc: 第一步：高德地图-初始化出各省级(有边界信息)、市级和区级的初始信息
@Time: 2020/05/26 17:05:53
@Author: wuwenrufeng (wuwenrufeng@163.com)
@Last Modified: 2020/05/26 17:05:54
@Modified By: wuwenrufeng (wuwenrufeng@163.com)
@Version: 1.0
@License: Copyright(C) 2019 - 2020 Borland
"""



import json

import requests
from pony.orm import commit, db_session, select
from retrying import retry

from util.models import City, District, Province, db
from util.settings import KEY


class MapApi:
    def __init__(self, key=None):
        """
        初始化
        :param key: 高德开发者密钥
        """
        if key is None:
            raise ValueError("key is none")
        self.key = key

    @retry(stop_max_attempt_number=10, wait_random_min=1000, wait_random_max=3000)
    def query(self, keyword, subdistrict=3, extensions='all'):
        """
        通过高德的api查询行政区域信息
        keyword: 规则：只支持单个关键词语搜索关键词
                  支持：行政区名称、citycode、adcode
                  例如，在subdistrict=2，搜索省份（例如山东）,能够显示市（例如济南）,区（例如历下区） 
        
        subdistrict: 
                  规则：设置显示下级行政区级数（行政区级别包括：国家、省/直辖市、市、区/县4个级别）
                  可选值: 0、1、2、3
                  0：不返回下级行政区
                  1：返回下一级行政区
                  2：返回下两级行政区
                  3：返回下三级行政区
        
        extentsion: 此项控制行政区信息中返回行政区边界坐标点 
                 可选值: base、all
                 base: 不返回行政区边界坐标点
                 all: 只返回当前查询district的边界值，不返回子节点的边界值
        
        return: 查询结果(json格式)
        """
        url = 'https://restapi.amap.com/v3/config/district?key={key}&keywords={keyword}&subdistrict={sub}&extensions={exten}'.format(
            key=self.key, keyword=keyword, sub=subdistrict, exten=extensions)
        with requests.Session() as s:
            response = s.get(url)
        try:
            result = json.loads(response.text)
        except:
            RuntimeError('^_^^_^json解析出错了')            
        else:
            status = result['status']
            # 查询成功
            if status == '1':
                return result
            else:
                print('查询失败,keyword:%s'% keyword)

    def get_provinces(self):
        """
        获取所有的省级信息并入库
        """
        # 返回下一级行政区信息+不返回行政区边界坐标点
        result = self.query(keyword='中国', subdistrict=1, extensions='base')
        if result:
            districts = result['districts'][0]['districts']
            # 全国所有的省级行政区信息入库
            for district in districts:
                name = district['name']
                adcode = int(district['adcode'])
                center = district['center']
                Province(name=name, adcode=adcode, center=center)

    def parse(self, districts):
        """
        解析行政区查询结果并入库
        districts: 行政区列表
        """
        for district in districts:
            # 行政区名称
            name = district.get('name')
            # 区级代码
            adcode = district.get('adcode')
            # 行政区中心坐标
            center = district.get('center')
            # 边界坐标
            polyline = district.get('polyline')
            # 行政区级别，省、市、区
            level = district.get('level')
            # 更新省级的相关信息
            if level == 'province':
                province = Province.get(name=name)
                province.set(polyline=polyline)
            if level == 'city':
                City(name=name, adcode=adcode, center=center)
            if level == 'district':
                District(name=name, adcode=adcode, center=center)
            if level == 'street':
                pass
            # 默认查询该行政区下三级的行政区信息
            districtsMore = district.get('districts')
            if districtsMore:
                self.parse(districtsMore)

    @db_session
    def main(self):
        self.get_provinces()
        for province in Province.select():
            result = self.query(keyword=province.name)
            if result:
                districts = result['districts']
                self.parse(districts)
                commit()

if __name__ == '__main__':
    map = MapApi(key=KEY)
    map.main()
