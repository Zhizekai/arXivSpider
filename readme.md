

![img.png](img.png)
# arXivSpider

## 介绍

本项目是arXiv论文网站的爬虫监控系统

🕸️ 爬取下载指定条件的论文到本地

🕷️ 订阅最新论文，发送论文到指定的邮箱



## 启动
本项目有两个UI版本，用户可以选择启动一个进行启动
### 启动GradioUI
```
gradio .\mainGradio.py
```

### 启动StreamlitUI
```
streamlit run ./mainStreamlit.py
```

config.yaml为配置文件，可配置查询条件等参数
## 技术
beautifulsoup4==4.11.1 

PyYAML==6.0

PyYAML==6.0.1

Requests==2.31.0

streamlit==1.26.0

