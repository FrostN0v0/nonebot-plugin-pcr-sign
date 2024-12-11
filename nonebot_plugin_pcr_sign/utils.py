import base64
from typing import Any
from pathlib import Path

import httpx
from pydantic import AnyUrl as Url

from .config import RES_DIR, SIGN_BG_DIR, ALBUM_BG_DIR, CustomSource, config


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read())
        base64_message = base64_encoded_data.decode("utf-8")
    return "data:image/png;base64," + base64_message


image_cache = {}
img_list = list(config.stamp_path.iterdir())
for image in img_list:
    img = image_to_base64(image)
    image_cache[image.stem] = img

todo_list = [
    "找伊绪老师上课",
    "给宫子买布丁",
    "和真琴寻找伤害优衣的人",
    "找镜哥探讨女装",
    "跟吉塔一起登上骑空艇",
    "和霞一起调查伤害优衣的人",
    "和佩可小姐一起吃午饭",
    "找小小甜心玩过家家",
    "帮碧寻找新朋友",
    "去真步真步王国",
    "找镜华补习数学",
    "陪胡桃排练话剧",
    "和初音一起午睡",
    "成为露娜的朋友",
    "帮铃莓打扫咲恋育幼院",
    "和静流小姐一起做巧克力",
    "去伊丽莎白农场给栞小姐送书",
    "观看慈乐之音的演出",
    "解救挂树的队友",
    "来一发十连",
    "井一发当期的限定池",
    "给妈妈买一束康乃馨",
    "购买黄金保值",
    "竞技场背刺",
    "给别的女人打钱",
    "氪一单",
    "努力工作，尽早报答妈妈的养育之恩",
    "成为魔法少女",
    "搓一把日麻",
    "和珂朵莉一起享用黄油蛋糕",
]


async def get_message_id(msg_ids: list[Any]):
    if isinstance(msg_ids[0], dict):
        return msg_ids[0].get("message_id")
    elif hasattr(msg_ids[0], "message_id"):
        return msg_ids[0].message_id
    else:
        return ""


async def get_lolicon_image() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.lolicon.app/setu/v2")
    return response.json()["data"][0]["urls"]["original"]


async def get_loliapi_image() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.loliapi.com/acg/pe/?type=url")
    return response.text


async def get_hitokoto() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://v1.hitokoto.cn/?c=f&encode=text")
        status_code = response.status_code
        if status_code == 200:
            hitokoto = response.text
        else:
            hitokoto = f"请求错误: {status_code}"
    return hitokoto


async def get_background_image() -> str | Url:
    default_background = RES_DIR / "images" / "background.png"

    match config.sign_background_source:
        case "default":
            background_image = image_to_base64(default_background)
        case "LoliAPI":
            background_image = await get_loliapi_image()
        case "Lolicon":
            background_image = await get_lolicon_image()
        case "random":
            background_image = CustomSource(uri=SIGN_BG_DIR).to_uri()
        case CustomSource() as cs:
            background_image = cs.to_uri()
        case _:
            background_image = image_to_base64(default_background)

    return background_image


async def get_album_background() -> str | Url:
    default_background = ALBUM_BG_DIR / "card.png"
    kraft_background = ALBUM_BG_DIR / "kraft_page.png"
    pcr_background = ALBUM_BG_DIR / "pcr_frame.png"
    prev_background = ALBUM_BG_DIR / "frame.png"

    match config.album_background_source:
        case "default":
            background_image = image_to_base64(default_background)
        case "kraft":
            background_image = image_to_base64(kraft_background)
        case "pcr":
            background_image = image_to_base64(pcr_background)
        case "prev":
            background_image = image_to_base64(prev_background)
        case "random":
            background_image = CustomSource(uri=ALBUM_BG_DIR).to_uri()
        case CustomSource() as cs:
            background_image = cs.to_uri()
        case _:
            background_image = image_to_base64(default_background)

    return background_image
