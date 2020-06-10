# 🌐amap 根据经纬度快速查询全国行政区域信息、省市区信息
行政区域查询，根据经纬度快速地查找特定的省市区行政区域信息。

## Features
- [x] 免费，免费，免费
- [x] 数据源可靠，数据源来自国内一级地图服务提供商
- [x] 手把手教你自建全国行政区域信息库
- [x] 手把手教你实现行政区域信息查询算法
- [x] 快速地查找特定的行政区域信息
- [x] APi接口调用

## 项目由来
官方服务有请求限制，升级plus又太贵，伤不起😂



## 使用
运行环境：需要运行在 python 3.7.4 （其它版本暂未测试)

**1. 安装依赖**
```bash
git clone https://github.com/wuwenrufeng/amap.git

pip install -r requirements.txt
```

## 运行效果
#### 测试环境：个人PC
#### 1.查询耗时

![](https://github.com/wuwenrufeng/amap/blob/master/docs/time.png)

#### 2.查询准确率
![](https://github.com/wuwenrufeng/amap/blob/master/docs/test.png)

**PS: 准确率测试是使用区级center进行查询的，所得准确率应该是100%，丢失的准确率是因为官方将center标记错误了
**
😜
![](https://github.com/wuwenrufeng/amap/blob/master/docs/fushun.png)
