from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
from database.mysql import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    gender = Column(Enum("male", "female", "unknown", name="gender_enum"))
    registration_date = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))  # 支持IPv6



