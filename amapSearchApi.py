#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File: amapSearchApi.py
@Project: amap
@Desc: api接口查询
@Time: 2020/06/10 13:49:53
@Author: wuwenrufeng (wuwenrufeng@163.com)
@Last Modified: 2020/06/10 16:18:47
@Modified By: wuwenrufeng (wuwenrufeng@163.com)
@Version: 1.0
@License: Copyright(C) 2019 - 2020 Borland
"""


import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from amapRegionSearch import RegionSearch

app = Flask(__name__)
CORS(app)


@app.route('/search', methods=['GET'])
def receive():
    point = request.args.get('point')
    if point:
        result = RegionSearch().search(point)
        return jsonify({'result': result, 'code': 200})
    else:
        return jsonify({'message': '请传入坐标点', 'code': 400})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
