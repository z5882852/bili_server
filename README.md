# bili_server

> B站视频反馈优化系统（后端）

### v1.0.1

## 关于项目

### 介绍

本项目为前后端分离项目，本项目为后端。

功能:
- 用户鉴权
- 解析视频信息
- 获取用户信息
- 分析弹幕数据并可视化显示
- 文心一言根据弹幕反馈提供优化建议

[前端地址](https://github.com/z5882852/bili_web)

### 技术栈

- python
- fastAPI
- SQLAlchemy
- redis
- mysql

## 如何使用

### 安装Python

**请安装Python3.10以上**

### 安装依赖
```shell
pip install -r requirements.txt
```

### 修改配置文件

将`config.template.yml`重命名为`config.yml`

填写配置文件中`redis`和`mysql`的地址和密码。

通过百度千帆大模型平台获取千帆api，并将api填写进配置文件中

### 启动服务

监听内网
```shell
python main.py
```

监听外网, port参数修改为你想监听的端口
```shell
uvicorn main:app --host 0.0.0.0 --port 8088
```


## 参考

[哔哩哔哩-API收集整理 | bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)

[bilidown-web | Zhouqluo/bilidown-web](https://github.com/Zhouqluo/bilidown-web)

