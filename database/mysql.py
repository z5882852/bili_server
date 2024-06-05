from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from log import logger
from utils import config

MYSQL_CONFIG = config.get("mysql", {})

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    MYSQL_CONFIG.get("username", "root"),
    MYSQL_CONFIG.get("password", ""),
    MYSQL_CONFIG.get("host", "localhost"),
    str(MYSQL_CONFIG.get("port", 3306)),
    MYSQL_CONFIG.get("database", "bili"),
)

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 声明基类
Base = declarative_base()

# 测试数据库连接
try:
    engine.connect()
    logger.debug("MySQL数据库连接成功!")
except Exception as e:
    logger.error(e)
    logger.error('数据库连接失败! 请检查配置文件和数据库是否正确!')
    import sys
    sys.exit(0)




