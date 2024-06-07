import os
import requests
import base64
import yaml
import jieba
import logging
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas.user import TokenData

jieba.setLogLevel(logging.INFO)


def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


# 加载配置文件
config = load_config("config.yml")
SECRET_CONFIG = config.get("secret", {})
SECRET_KEY = SECRET_CONFIG.get("secret_key", "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6")
ALGORITHM = SECRET_CONFIG.get("algorithm", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = SECRET_CONFIG.get("expire_time", 1440)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_word_count(text_list: list) -> list[dict]:
    """分词统计"""
    word_dict = {}
    for text in text_list:
        words = jieba.cut(text)
        for word in words:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    # 去除停用词
    with open("data/cn_stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = f.read().split("\n")
    stopwords += ["\n", "‘", "’", " "]
    for word in stopwords:
        if word in word_dict:
            word_dict.pop(word)
    # 按照词频排序
    word_dict = dict(sorted(word_dict.items(), key=lambda x: x[1], reverse=True))
    # 取前30个，不足30个则全部返回
    word_dict = dict(list(word_dict.items())[:30])
    word_count = []
    for k, v in word_dict.items():
        word_count.append({
            "name": str(k),
            "value": v
        })
    return word_count


def download_images(image_url: str) -> str:
    res = requests.get(image_url, timeout=3)
    if res.status_code != 200:
        return ""
    return base64.b64encode(res.content).decode("utf-8")
