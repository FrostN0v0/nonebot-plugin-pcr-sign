import random

from pathlib import Path
from typing import Literal
from nonebot import logger
from nonebot.plugin import get_plugin_config
from pydantic import BaseModel
from pydantic import AnyUrl as Url
import nonebot_plugin_localstore as localstore

RES_DIR: Path = Path(__file__).parent / "resources"
TEMPLATES_DIR: Path = RES_DIR / "templates"


class CustomSource(BaseModel):
    uri: Url | Path

    def to_uri(self) -> Url:
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
                return Url((uri / random.choice(files)).as_uri())

            if not uri.exists():
                raise FileNotFoundError(f"CustomSource: {uri} not exists")

            return Url(uri.as_uri())

        return self.uri


class Config(BaseModel):
    stamp_path: Path = RES_DIR / "stamps"
    """ 印章图片路径 """
    sign_background_source: Literal[
                                "default",
                                "LoliAPI",
                                "Lolicon"] | CustomSource = "default"
    """ 背景图片来源 """


config = get_plugin_config(Config)
