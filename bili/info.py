from bili.session import BiliSession
from bili.sign import get_w_rid
from utils import download_images


def get_info(bv: str = None):
    session = BiliSession().session
    url = "https://api.bilibili.com/x/web-interface/view"
    params = {
        "bvid": bv
    }
    response = session.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"请求失败，状态码：{response.status_code}")
    data = response.json()
    if data["code"] != 0:
        raise Exception(f"请求失败，错误信息：{data.get('message', '未知错误')}")
    data = data.get("data", {})

    data["pic_base64"] = download_images(data.get("pic"))
    return data


def get_user_info(mid: str):
    if not mid:
        raise Exception("请求失败，mid为空!")
    session = BiliSession().session
    cookies = {
        "buvid3": "463EB650-1CCE-D872-00E4-174A876E651F98864infoc",
        "buvid4": "FA699B04-2917-D65D-E727-C7F574481E0A00417-024060300-QE0lHqgVYDSXapUrnc9V4Q%3D%3D",
        "buvid_fp": "4cfdabe303d0e866ffecaf3d643cbddc",
    }
    session.cookies.update(cookies)
    session.headers.update({"referer": "https://space.bilibili.com/{mid}"})
    url = "https://api.bilibili.com/x/space/wbi/acc/info"
    params = {
        "mid": mid
    }
    w_rid, wts = get_w_rid(params)

    params.update({
        "w_rid": w_rid,
        "wts": wts
    })
    response = session.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"请求失败，状态码：{response.status_code}")
    data = response.json()
    if data["code"] != 0:
        raise Exception(f"请求失败，错误信息：{data.get('message', '未知错误')}")
    data = data.get("data", {})
    data["face_base64"] = download_images(data.get("face"))
    return data
