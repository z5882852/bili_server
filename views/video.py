from fastapi import APIRouter, Query, Depends
from starlette.responses import StreamingResponse
from log import logger
from bili.dm import get_danmu
from bili.info import get_info, get_user_info
from controllers import video as video_controller
from views.user import get_current_user
import schemas.user as schemas

router = APIRouter()


@router.get("/video/info")
async def video_info(
        url: str = Query(
            None,
            title="视频url地址",
            description="视频的url地址，要求是bv类型的url",
            min_length=1,
            max_length=100,
            regex="^https://www.bilibili.com/video/BV.*"
        ), bv: str = Query(
            None,
            title="视频bv号",
            description="视频的bv号, 例如：BV1Zy4y1C7Jw",
            min_length=1,
            max_length=100,
            regex="^BV.*"
        ), current_user: schemas.UserResponse = Depends(get_current_user)):
    """获取视频信息"""
    if not url and not bv:
        return {"code": 400, "msg": "参数为空"}
    if url:
        # 去除url中的参数
        url = url.split("?")[0]
        bv = url.split("/")[-1]
    try:
        logger.debug(f"获取视频信息，bv: {bv}")
        info = get_info(bv)
        return {"code": 200, "msg": "success", "data": info}
    except Exception as e:
        logger.error(f"获取视频信息失败，错误信息：{e}")
        return {"code": 500, "msg": "获取视频信息失败"}


@router.get("/video/user/info")
async def video_info(
        mid: str = Query(
            None,
            title="mid",
            description="目标用户mid",
            min_length=1,
            max_length=20,
            regex="^\d+$"
        ), current_user: schemas.UserResponse = Depends(get_current_user)):
    """获取获取作者信息"""
    if not mid:
        return {"code": 400, "msg": "参数为空"}
    try:
        logger.debug(f"获取用户信息，mid: {mid}")
        info = get_user_info(mid)
        return {"code": 200, "msg": "success", "data": info}
    except Exception as e:
        logger.error(f"获取用户信息失败，错误信息：{e}")
        return {"code": 500, "msg": "获取用户信息失败"}


@router.get("/video/dm")
async def video_dm(
        cid: str = Query(
            None,
            title="视频cid",
            description="视频的cid号",
            regex="^\d+$"
        ),
        aid: str = Query(
            None,
            title="视频aid",
            description="视频的aid号",
            regex="^\d+$"
        ), current_user: schemas.UserResponse = Depends(get_current_user)):
    """获取视频弹幕"""
    try:
        logger.debug(f"获取视频弹幕，cid: {cid}, aid: {aid}")
        info = get_danmu(cid, aid)
        return {"code": 200, "msg": "success", "data": info}
    except Exception as e:
        logger.error(f"获取视频弹幕失败，错误信息：{e}")
        return {"code": 500, "msg": "获取视频弹幕失败"}


@router.get("/video/dm/analyse")
async def video_dm_processed(
        cid: str = Query(
            None,
            title="视频cid",
            description="视频的cid号",
            regex="^\d+$"
        ),
        aid: str = Query(
            None,
            title="视频aid",
            description="视频的aid号",
            regex="^\d+$"
        ), current_user: schemas.UserResponse = Depends(get_current_user)):
    """获取处理后的弹幕信息"""
    try:
        data = video_controller.handle_danmu(cid, aid)
        return {"code": 200, "msg": "success", "data": data}
    except Exception as e:
        logger.error(f"分析视频弹幕失败，错误信息：{e}")
        return {"code": 500, "msg": "分析视频弹幕失败"}


@router.get("/video/comments")
async def video_comments():
    return {"code": 200, "msg": "success"}


# 视频优化方案
@router.get("/video/optimization")
async def video_optimization(
        cid: str = Query(
            None,
            title="视频cid",
            description="视频的cid号",
            regex="^\d+$"
        ),
        aid: str = Query(
            None,
            title="视频aid",
            description="视频的aid号",
            regex="^\d+$"
        ), current_user: schemas.UserResponse = Depends(get_current_user)):
    """获取优化建议"""
    # 流式响应，格式为json
    return StreamingResponse(content=video_controller.handle_optimization(cid=cid, aid=aid),
                             media_type="text/event-stream")
