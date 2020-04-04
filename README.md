# 知乎广告屏蔽
使用mitm技术进行知乎app广告定向屏蔽
# 原理
本项目基于[mitmproxy](https://github.com/mitmproxy/mitmproxy)，使用中间人攻击的方法对https请求进行修改，以达到精准过滤广告的效果。  
目前仅支持知乎IOS客户端，使用时需要在wifi中设置http代理并信任证书  
您可以在block_zhihu_ad.py中设定是否屏蔽推荐栏中的视频卡片
```python
disable_ads=True
#过滤广告
disable_videos=False
#过滤视频卡片
disable_answers_with_video=False
#过滤带有视频的回答卡片
```
# 使用方法
# 一、安装
您可以使用三种不同的方法安装服务
```bash
git clone https://github.com/LiuChangFreeman/block_zhihu_ad.git
cd block_zhihu_ad
```
## 1、从Dockerfile制作镜像
```bash
docker build -t block_zhihu_ad .
docker run -it --name block_zhihu_ad -p 9999:8889  --restart=always -d block_zhihu_ad
```
您可以将9999修改为任何可用的端口号
## 2、使用systemd创建linux服务
需自行安装安装python3与mitmproxy,并将block_zhihu_ad.py放置到
**/home/block_zhihu_ad/block_zhihu_ad.py**
```bash
cp block_zhihu_ad.service /etc/systemd/system/block_zhihu_ad.service
systemctl daemon-reload
systemctl enable block_zhihu_ad
systemctl start block_zhihu_ad
```
您可以在block_zhihu_ad.service中修改端口号
```bash
[Unit]
Description=mitmdump
After=syslog.target

[Service]
ExecStart=/usr/local/bin/mitmdump -s /home/block_zhihu_ad/block_zhihu_ad.py -p 8889 -q
Restart=always
Type=simple
StartLimitInterval=1sec

[Install]
WantedBy=multi-user.target
```
## 3、使用winsw创建windows服务
需自行安装windows版mitmproxy到  
**C:/Program Files (x86)/mitmproxy/**
```cmd
BlockZhihuAd install 
BlockZhihuAd start
```
您可以在BlockZhihuAd.xml中修改端口号
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<service>
  <id>BlockZhihuAd</id>
  <name>BlockZhihuAd</name>
  <description>BlockZhihuAd</description>
  <executable>C:/Program Files (x86)/mitmproxy/bin/mitmdump.exe</executable>
  <startargument>-s</startargument>
  <startargument>%BASE%\block_zhihu_ad.py</startargument>
  <startargument>-q</startargument>
  <startargument>-p</startargument>
  <startargument>8889</startargument>
  <logpath>%BASE%\logs</logpath>
  <logmode>roll</logmode>  
</service>
```
# 二、使用
## 1、在wifi的http代理中连接到您的服务器
![](http://static.aikatsucn.cn/images/block-zhihu-ad/1.png)
## 2、访问http://mitm.it，安装证书
![](http://static.aikatsucn.cn/images/block-zhihu-ad/2.png)
## 3、在**设置->通用->描述文件**中安装已下载的mitmproxy描述文件
![](http://static.aikatsucn.cn/images/block-zhihu-ad/3.png)
## 4、在**设置->通用->关于本机->证书信任设置**中勾选完全信任mitmproxy的证书
![](http://static.aikatsucn.cn/images/block-zhihu-ad/4.png)