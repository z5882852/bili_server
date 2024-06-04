from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy import inspect
from database.mysql import engine, SessionLocal
from models.user import *
from schemas.user import *
from controllers.user import *
from log import logger
import utils

Base.metadata.create_all(bind=engine)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        inspector = inspect(db.bind)
        if not inspector.has_table("users"):
            Base.metadata.create_all(bind=engine)
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证令牌",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db), request: Request = None):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": 400, "message": "该用户已经注册"}
        )
    return create_user(db=db, user=user, ip_address=request.client.host)


@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": 401, "message": "用户名或密码错误"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"code": 200, "message": "登录成功", "access_token": access_token, "token_type": "bearer"}


@router.put("/update_password")
def update_password(user: UserUpdatePassword, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_user = update_user_password(db=db, username=current_user.username, user=user)
    if not db_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": 400, "message": "密码不正确或发生其他错误"}
        )
    return {"code": 200, "message": "密码更换成功"}


@router.get("/user/info")
def read_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user_by_username(db, username=current_user.username)
    if not db_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": 401, "message": "用户不存在"}
        )
    data = {
        "user_id": db_user.id,
        "user_name": db_user.username,
        "gender": db_user.gender,
        "ip": db_user.ip_address,
        "registration_date": db_user.registration_date,

    }
    return {"code": 200, "message": "成功", "data": data}
