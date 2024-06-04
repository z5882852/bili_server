import os
import sys
import qianfan
from utils import config
from log import logger


QIANFAN_CONFIG = config.get("qianfan", {})
if not QIANFAN_CONFIG.get("access_key") or not QIANFAN_CONFIG.get("secret_key"):
    logger.error("access_key和secret_key未设置!")
    sys.exit(0)
os.environ["QIANFAN_ACCESS_KEY"] = QIANFAN_CONFIG.get("access_key", "")
os.environ["QIANFAN_SECRET_KEY"] = QIANFAN_CONFIG.get("secret_key", "")

chat_comp = qianfan.ChatCompletion()


def get_chat_comp(message):
    resp = chat_comp.do(
        model=QIANFAN_CONFIG.get("model", "ERNIE-4.0-8K-0104"),
        system=QIANFAN_CONFIG.get("prompt", "给定一则视频的多条弹幕内容 [weight] [content]，请根据弹幕内容，为该视频作者提出视频的优化建议。请直接给出优化建议和理由，不需要其他内容。"),
        temperature=QIANFAN_CONFIG.get("temperature", 0.6),
        top_p=QIANFAN_CONFIG.get("top_p", 0.8),
        messages=[{
            "role": "user",
            "content": message
        }],
        stream=True)
    return resp
