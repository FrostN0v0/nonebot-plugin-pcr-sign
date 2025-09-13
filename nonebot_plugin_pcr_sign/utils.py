import httpx
from pydantic import AnyUrl as Url
from nonebot import logger

from .config import RES_DIR, SIGN_BG_DIR, ALBUM_BG_DIR, CustomSource, config

image_cache = {}
img_list = list(config.stamp_path.iterdir())
for image in img_list:
    image_cache[image.stem] = image

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


async def get_lolicon_image() -> str:
    async with httpx.AsyncClient(proxy=config.sign_proxy) as client:
        response = await client.get("https://api.lolicon.app/setu/v2")
    return response.json()["data"][0]["urls"]["original"]


async def get_loliapi_image() -> str:
    async with httpx.AsyncClient(proxy=config.sign_proxy) as client:
        response = await client.get("https://api.loliapi.com/acg/pe/?type=url")
    return response.text


async def get_hitokoto() -> str:
    hitokoto_urls = [
        "https://v1.hitokoto.cn/?c=f&encode=text",
        "https://uapis.cn/api/say",
    ]
    async with httpx.AsyncClient(proxy=config.sign_proxy) as client:
        for url in hitokoto_urls:
            try:
                response = await client.get(url, timeout=5)
                if response.status_code == 200:
                    logger.debug(f"使用接口 {url} 获取成功，一言：{response.text}")
                    return response.text
            except httpx.RequestError:
                logger.warning(f"使用接口 {url} 获取一言失败")
                continue
    return ""


async def get_background_image() -> str | Url:
    default_background = RES_DIR / "images" / "background.png"

    match config.sign_background_source:
        case "default":
            background_image = default_background.as_posix()
        case "LoliAPI":
            background_image = await get_loliapi_image()
        case "Lolicon":
            background_image = await get_lolicon_image()
        case "random":
            background_image = CustomSource(uri=SIGN_BG_DIR).to_uri()
        case CustomSource() as cs:
            background_image = cs.to_uri()
        case _:
            background_image = default_background.as_posix()

    return background_image


async def get_album_background() -> str | Url:
    default_background = ALBUM_BG_DIR / "card.png"
    kraft_background = ALBUM_BG_DIR / "kraft_page.png"
    pcr_background = ALBUM_BG_DIR / "pcr_frame.png"
    prev_background = ALBUM_BG_DIR / "frame.png"

    match config.album_background_source:
        case "default":
            background_image = default_background.as_posix()
        case "kraft":
            background_image = kraft_background.as_posix()
        case "pcr":
            background_image = pcr_background.as_posix()
        case "prev":
            background_image = prev_background.as_posix()
        case "random":
            background_image = CustomSource(uri=ALBUM_BG_DIR).to_uri()
        case CustomSource() as cs:
            background_image = cs.to_uri()
        case _:
            background_image = default_background.as_posix()

    return background_image
