from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdatePassword
from utils import get_password_hash, verify_password


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate, ip_address: str = ""):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        gender=user.gender,
        ip_address=ip_address,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(db: Session, username, user: UserUpdatePassword):
    db_user = get_user_by_username(db, user.username)
    if db_user and verify_password(user.old_password, db_user.hashed_password):
        db_user.hashed_password = get_password_hash(user.new_password)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
