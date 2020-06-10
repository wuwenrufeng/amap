#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File: models.py
@Project: amap
@Desc: ORM的声明与创建
@Time: 2020/06/09 9:24:00
@Author: wuwenrufeng (wuwenrufeng@163.com)
@Last Modified: 2020/06/09 9:24:06
@Modified By: wuwenrufeng (wuwenrufeng@163.com)
@Version: 1.0
@License: Copyright(C) 2019 - 2020 Borland
"""

from pony.orm import *
from .settings import MYSQL_PARAM

db = Database()

class Province(db.Entity):
    """省级"""
    _table_ = 'province'

    id = PrimaryKey(int, auto=True)
    # 行政区名称
    name = Required(str, max_len=200)
    # 区域编码
    adcode = Required(int, size=24, unsigned=True)
    # 区域中心点
    center = Required(str, max_len=100)
    # 行政区边界坐标点
    polyline = Optional(LongStr)
    # 最大行政区边界坐标点
    max_point = Optional(str, max_len=100)
    # 最小行政区边界坐标点
    min_point = Optional(str, max_len=100)

class City(db.Entity):
    """市级"""
    _table_ = 'city'

    id = PrimaryKey(int, auto=True)
    name = Required(str, max_len=200)
    adcode = Required(int, size=24, unsigned=True)
    center = Required(str, max_len=100)
    polyline = Optional(LongStr)
    max_point = Optional(str, max_len=100)
    min_point = Optional(str, max_len=100)

class District(db.Entity):
    """区级"""
    _table_ = 'district'

    id = PrimaryKey(int, auto=True)
    name = Required(str, max_len=200)
    adcode = Required(int, size=24, unsigned=True)
    center = Required(str, max_len=100)
    polyline = Optional(LongStr)
    max_point = Optional(str, max_len=100)
    min_point = Optional(str, max_len=100)

# 数据库连接
db.bind(**MYSQL_PARAM)
# 数据库表映射
db.generate_mapping(create_tables=True)

