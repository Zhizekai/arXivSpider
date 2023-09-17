
# arXivSpider

## 介绍

本项目是arXiv论文网站的爬虫监控系统，可以把网站的最新论文爬取并且发送到指定的邮箱

## 技术
beautifulsoup4==4.11.1
PyYAML==6.0
PyYAML==6.0.1
Requests==2.31.0
streamlit==1.26.0

## 启动
在命令行输入
```
streamlit run ./mainStreamlit.py
```
即可启动UI服务

config.yaml为配置文件，可配置查询条件等参数