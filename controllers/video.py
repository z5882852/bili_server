import json
import qianfan.errors
from loguru import logger
from bili.dm import get_danmu
from nlp.chat import get_chat_comp
from nlp.paddle import get_sentiment_count
from database.redis import redis, EXPIRE_TIME
from utils import get_word_count


def handle_danmu(cid, aid: str = None):
    """处理弹幕"""
    # 先从redis中获取，如果没有再去请求
    dm_list = redis.get(f"dm_{cid}")
    if not dm_list or True:
        logger.debug(f"弹幕未命中缓存，cid: {cid}")
        dm_list = get_danmu(cid, aid)
        redis.set(f"dm_{cid}", json.dumps(dm_list), ex=EXPIRE_TIME)
    else:
        dm_list = json.loads(dm_list)
    dm_content_list = []

    # 权重
    weights = []

    # 统计时间分布
    dm_time_count = {}
    for dm in dm_list:
        dm_content_list.append(dm.get("content"))
        weights.append(dm.get("weight"))
        if dm.get("progress"):
            k = dm.get("progress") // 1000 // 60
            if k not in dm_time_count:
                dm_time_count[k] = 0
            dm_time_count[k] += 1
    sorted_dm_time_count = {k: dm_time_count[k] for k in sorted(dm_time_count.keys())}
    time_count = []
    for k, v in sorted_dm_time_count.items():
        time_count.append({
            "name": str(k),
            "value": v
        })

    # 进行分词统计
    word_count = get_word_count(dm_content_list)

    # 情感分析统计
    sentiment_count = get_sentiment_count(dm_content_list)

    data = dict(
        dm_list=dm_list,
        time_count=time_count,
        word_count=word_count,
        sentiment_count=sentiment_count,
        avg_weight=sum(weights) / len(weights)
    )
    return data


def handle_optimization(cid, aid: str = None):
    """视频优化"""
    # 先从redis中获取，如果没有再去请求
    dm_list = redis.get(f"dm_{cid}")
    if not dm_list:
        logger.debug(f"弹幕未命中缓存，cid: {cid}")
        dm_list = get_danmu(cid, aid)  # 获取弹幕
        redis.set(f"dm_{cid}", json.dumps(dm_list), ex=EXPIRE_TIME)  # 缓存弹幕
    else:
        dm_list = json.loads(dm_list)
    # 获取弹幕内容 [weight] [content]
    dm = [f'{dm["weight"]} {dm["content"]}' for dm in dm_list]
    # 去重
    dm = list(set(dm))[:200]
    dm_text = "\n".join(dm)
    logger.debug("弹幕长度: {}", len(dm_text))
    # 调用模型, 输入弹幕内容，返回优化建议
    try:
        response = get_chat_comp(dm_text)
    except qianfan.errors.APIError as e:
        data = {
            "error": 1,
            "message": str(e)
        }
        logger.error(e)
        yield json.dumps(data, ensure_ascii=False)
        return
    for resp in response:
        # 流式响应结果
        yield json.dumps(resp.body, ensure_ascii=False)
        # yield resp["result"]
