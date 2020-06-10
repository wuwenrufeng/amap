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