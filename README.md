# 知乎广告屏蔽器
使用mitm技术进行知乎app广告定向屏蔽
# 原理
本项目基于mitmdump，使用中间人攻击的方法对http请求进行修改，以达到过滤广告的效果，目前仅支持最新版IOS知乎客户端，使用时需要在wifi中设置http代理并信任证书
# 使用方法
# 安装
## 1、从Dockerfile制作镜像
```bash
docker build -t block_zhihu_ad .
docker run -it --name block_zhihu_ad -p 9999:8889  --restart=always -d block_zhihu_ad
```
## 2、使用systemd创建linux服务
需自行安装安装python3与mitmproxy,并将block_zhihu_ad.py放置到
**/home/block_zhihu_ad/block_zhihu_ad.py**
```bash
cp block_zhihu_ad.service /etc/systemd/system/block_zhihu_ad.service
systemctl daemon-reload
systemctl enable block_zhihu_ad
systemctl start block_zhihu_ad
```
## 3、使用winsw创建windows服务
需自行安装windows版mitmproxy到
**C:/Program Files (x86)/mitmproxy/**
```cmd
BlockZhihuAd install 
BlockZhihuAd start
```
# 使用
https://jingyan.baidu.com/article/03b2f78cdb52105ea237aeeb.html