import random
from pathlib import Path
from typing import Any, Literal

from nonebot import logger
from pydantic import BaseModel
from pydantic import AnyUrl as Url
from nonebot.compat import PYDANTIC_V2
from nonebot.plugin import get_plugin_config
import nonebot_plugin_localstore as localstore

RES_DIR: Path = Path(__file__).parent / "resources"
TEMPLATES_DIR: Path = RES_DIR / "templates"
ALBUM_BG_DIR: Path = RES_DIR / "images" / "album_background"
SIGN_BG_DIR: Path = RES_DIR / "images" / "sign_background"


class CustomSource(BaseModel):
    uri: Url | Path

    def to_uri(self) -> Any:
        if isinstance(self.uri, Path):
            uri = self.uri
            if not uri.is_absolute():
                uri = Path(localstore.get_plugin_data_dir() / uri)

            if uri.is_dir():
                # random pick a file
                files = [f for f in uri.iterdir() if f.is_file()]
                logger.debug(
                    f"CustomSource: {uri} is a directory, random pick a file: {files}"
                )
                if PYDANTIC_V2:
                    return Url((uri / random.choice(files)).as_posix())
                else:
                    return Url((uri / random.choice(files)).as_posix(), scheme="file")  # type: ignore

            if not uri.exists():
                raise FileNotFoundError(f"CustomSource: {uri} not exists")
            if PYDANTIC_V2:
                return Url(uri.as_posix())
            else:
                return Url(uri.as_posix(), scheme="file")  # type: ignore

        return self.uri


class Config(BaseModel):
    sign_argot_expire_time: int = 300
    """ 暗语过期时间（单位：秒） """
    stamp_path: Path = RES_DIR / "stamps"
    """ 印章图片路径 """
    sign_background_source: (
        Literal["default", "LoliAPI", "Lolicon", "random"] | CustomSource
    ) = "default"
    """ 背景图片来源 """
    album_background_source: (
        Literal["default", "kraft", "pcr", "prev", "random"] | CustomSource
    ) = "default"
    """ 收集册背景图片来源 """


config = get_plugin_config(Config)
