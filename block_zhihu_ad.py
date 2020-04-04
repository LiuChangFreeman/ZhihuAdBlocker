from mitmproxy import http
from mitmproxy.proxy.protocol import TlsLayer, RawTCPLayer
import json
import logging
import datetime
    
disable_ads=True
#过滤广告
disable_videos=False
#过滤视频卡片
disable_answers_with_video=False
#过滤带有视频的回答卡片

server_address_watch=["client-api.itunes.apple.com","api.zhihu.com"]
#过滤host的黑名单，除此之外的域名或者ip一律放行

date=datetime.datetime.now().strftime('%Y-%m-%d')
logger = logging.getLogger('{}'.format(date))
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter(fmt="%(asctime)s   %(message)s", datefmt='%H:%M:%S')
terminal_handler = logging.StreamHandler()
terminal_handler.setLevel(logging.DEBUG)
terminal_handler.setFormatter(fmt)
file_handler = logging.FileHandler('{}.log'.format(date), mode="a", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(fmt)
logger.addHandler(terminal_handler)
logger.addHandler(file_handler)

def next_layer(next_layer):
    if isinstance(next_layer, TlsLayer) and next_layer._client_tls:
        server_address = next_layer.server_conn.address
        host=server_address[0]
        if not host in server_address_watch:
            next_layer_replacement = RawTCPLayer(next_layer.ctx, ignore=True)
            next_layer.reply.send(next_layer_replacement)

def request(flow: http.HTTPFlow) -> None:
    if flow.request.url.startswith("https://client-api.itunes.apple.com/WebObjects/MZStorePlatform.woa/wa/lookup"):
        logger.info("itunes广告请求")
        return

def response(flow: http.HTTPFlow) -> None:
    if flow.request.url.startswith("https://api.zhihu.com/moments/recommend"):
        data= json.loads(flow.response.text)
        cards=[]
        for item in data["data"]:
            if "ad" in item:
                if disable_ads:
                    logger.info("推荐广告:{}".format(item["ad"]["brand"]["name"]))
            elif item["type"]=="market_card":
                if disable_ads:
                    logger.info("卡片广告:{}".format(item["fields"]["body"]["title"]))
            else:
                cards.append(item)
        data["data"]=cards
        flow.response.text=json.dumps(data)
    if flow.request.url.startswith("https://api.zhihu.com/topstory/recommend"):
        data= json.loads(flow.response.text)
        cards=[]
        for item in data["data"]:
            if "ad" in item:
                if disable_ads:
                    logger.info("推荐广告:{}".format(item["ad"]["brand"]["name"]))
            elif item["type"]=="market_card":
                if disable_ads:
                    logger.info("卡片广告:{}".format(item["fields"]["body"]["title"]))
            else:
                if item["extra"]["type"]=="zvideo":
                    if disable_videos:
                        logger.info("视频:{}".format(item["common_card"]["feed_content"]["title"]["panel_text"]))
                elif item["common_card"]["style"]=="BIG_IMAGE":
                    if disable_answers_with_video:
                        logger.info("视频回答:{}".format(item["common_card"]["feed_content"]["title"]["panel_text"]))
                else:
                    cards.append(item)
        data["data"]=cards
        flow.response.text=json.dumps(data)
    if flow.request.url.startswith("https://api.zhihu.com/v4/questions"):
        data= json.loads(flow.response.text)
        if "ad_info" in data:
            if disable_ads:
                logger.info("问题广告:{}".format(data["ad_info"]["ad"]["brand"]["name"]))
                del data["ad_info"]
        flow.response.text=json.dumps(data)