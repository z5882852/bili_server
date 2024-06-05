from bili.dm import get_danmu
from bili.info import get_info

if __name__ == '__main__':
    # print(get_info("BV17m42157dx"))
    dms = get_danmu("1566091141")
    dm_text = [dm['content'] for dm in dms]
    print(dm_text)
