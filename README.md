# 🌐amap 根据经纬度快速查询全国行政区域信息、省市区信息
行政区域查询，根据经纬度快速地查找特定的省市区、行政区域信息。

## Features
- [x] 免费，免费，免费
- [x] 打破官方请求量限制，一次生产，终生使用
- [x] 数据源可靠，数据源来自高德地图开放的HTTP接口
- [x] 手把手教你自建全国行政区域信息库
- [x] 手把手教你实现行政区域信息查询算法
- [x] 快速地查找特定的行政区域信息
- [x] APi接口调用

## 项目由来
官方服务有请求限制，又不想升级plus

![](https://github.com/wuwenrufeng/amap/blob/master/docs/gaode1.png)

## 配置环境
运行环境：需要运行在 python 3.7.4+ 

**1. 安装依赖**
```bash
git clone https://github.com/wuwenrufeng/amap.git

pip install -r requirements.txt
```
## 快速开始
**1. 下载数据库文件cn_area.sql,并导入到mysql中**

链接：https://pan.baidu.com/s/1zJZTccPjrY4RD_TgAUh84A 
提取码：cmuv 

**2. 数据库访问配置**

文件地址：amap/utils/settings.py

```python
# mysql
MYSQL_PARAM = {
    'provider': 'mysql',
    'host': 'localhost',
    'port': 3306,
    'user': 'admin',
    'passwd': '123456',
    'db': 'cn_area'
}
```
**3. 开启api查询服务**
```python
   python amapSearchApi.py
```
**4. 开始查询**

URL: http://127.0.0.1/search?point=117.195907,39.118327

![](https://github.com/wuwenrufeng/amap/blob/master/docs/api.png)
## 使用手册
**第一步：高德地图-初始化出各省级(有边界信息)、市级和区级的初始信息**
```python
   python amapInit.py
```

**第二步：高德地图-补充市、区的边界信息 (ps: 高德不提供有关街道的边界顶点信息)**
```python
   python amapPopulate.py
```

**第三步：计算出province, city, district表中的最大最小边界经纬度，并填充到数据库中**
```python
   python amapMaxMin.py
```

**第四步：开启服务，查询给定坐标点所属的行政区域信息**
```python
   python amapSearchApi.py
```
## 点在区域内的判定算法
使用外包矩形+闭合路径包含算法

**一级过滤：外包矩形算法**
```python
   def in_box(point, maxP, minP):
    """
    判断点是否在多边形的外包矩形中 
    point: 待判定的坐标点 
    maxP: 最大坐标点 
    minP: 最小坐标点 
    """
    return (minP.x <= point.x <= maxP.x) and (minP.y <= point.y <= maxP.y)
```

**二级过滤：闭合路径包含算法**
```python
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
```

## 测试结果
#### 测试环境：个人PC
#### 1.查询耗时

![](https://github.com/wuwenrufeng/amap/blob/master/docs/time.png)

#### 2.查询准确率
![](https://github.com/wuwenrufeng/amap/blob/master/docs/test.png)

##### PS: 准确率测试是使用区级center进行查询的，所得准确率应该是100%，丢失的准确率是因为官方将center标记错误了！
😜
![](https://github.com/wuwenrufeng/amap/blob/master/docs/fushun.png)

## 后续更新。。。

**GPS坐标、mapbar坐标、baidu坐标转换成高德坐标**

**逆地址地理信息解析**

## 交流 & 讨论

如果您对amap有任何疑问，欢迎添加作者微信来交流讨论。或者，您可以扫下方二维码给作者打赏去升级其他地图api套件或买一杯咖啡哈🥰。

<p align="center">
    <img src="https://github.com/wuwenrufeng/amap/blob/master/docs/chat.jpg" height="260">
</p>
