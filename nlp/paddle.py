from log import logger
from paddlenlp import Taskflow
from utils import config

PADDLE_CONFIG = config.get("paddle", {})

# 初始化情感分析模型
senta = Taskflow(PADDLE_CONFIG.get("model", "sentiment_analysis"), home_path=PADDLE_CONFIG.get("model_path", "./data"))
logger.debug("情感分析模型 sentiment_analysis 初始化成功!")


def get_sentiment_count(text_list):
    output = senta(text_list)
    result = {
        "positive": 0,
        "negative": 0
    }
    for item in output:
        result[item.get("label")] += 1
    return result






