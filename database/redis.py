import sys
import redis
from log import logger
from utils import config

REDIS_CONFIG = config.get("redis", {})

# 初始化redis连接
pool = redis.ConnectionPool(
    host=REDIS_CONFIG.get("host", "localhost"),
    port=REDIS_CONFIG.get("port", 6379),
    db=REDIS_CONFIG.get("database", 0),
    decode_responses=True,
    password=REDIS_CONFIG.get("password", None),
    socket_timeout=REDIS_CONFIG.get("timeout", 5),
)

redis = redis.Redis(connection_pool=pool)

try:
    if redis.get("test") == "test":
        logger.debug("redis连接成功!")
except Exception as e:
    logger.error(e)
    logger.error("redis连接失败！请检查redis服务是否开启或者配置文件是否正确")
    sys.exit(0)


# 过期时间
EXPIRE_TIME = REDIS_CONFIG.get("expire", 3600)
