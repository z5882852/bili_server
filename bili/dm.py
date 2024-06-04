import json
from google.protobuf import json_format
import bili.dm_pb2 as Danmaku
from bili.session import BiliSession
from bili.sign import get_w_rid


def get_danmu(cid, aid: str = None) -> list[dict]:
    """获取所有弹幕"""
    dm_list = []
    for i in range(1, 20):
        try:
            dm_list += get_segment_dm(cid, aid, i)
        except:
            break
    if len(dm_list) == 0:
        raise Exception("弹幕内容为空！")
    return dm_list

    

def get_segment_dm(cid, aid: str = None, idx: int = 1):
    """"""
    session = BiliSession().session
    url = "https://api.bilibili.com/x/v2/dm/wbi/web/seg.so"

    params = {
        "type": "1",
        "oid": str(cid),
        "segment_index": idx,
        "web_location": "1315873",
    }
    if aid:
        params.update({
            "pid": str(aid)
        })

    w_rid, wts = get_w_rid(params)

    params.update({
        "w_rid": w_rid,
        "wts": wts
    })

    resp = session.get(url, params=params)
    if resp.status_code != 200:
        raise Exception(f"请求失败，状态码：{resp.status_code}")
    data = resp.content
    danmaku_seg = Danmaku.DmSegMobileReply()
    danmaku_seg.ParseFromString(data)
    dm_list = []
    for element in danmaku_seg.elems:
        ele = json.loads(json_format.MessageToJson(element, ensure_ascii=False))
        if ele.get('mode', 1) == 7:
            content = json.loads(ele.get('content'))
            ele['content'] = content[4].replace("/n", '')
        dm_list.append(ele)
    return dm_list

