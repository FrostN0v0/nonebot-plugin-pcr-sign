from datetime import date
from typing_extensions import TypedDict

from nonebot_plugin_orm import Model
from sqlalchemy.orm import Mapped, mapped_column


class User(Model):
    __tablename__ = "sign_users"

    gid: Mapped[int] = mapped_column(primary_key=True)
    """Group ID"""
    uid: Mapped[int] = mapped_column(primary_key=True)
    """User ID"""
    affection: Mapped[int] = mapped_column(default=0)
    """User's Affection"""
    last_sign: Mapped[date]
    """Last Sign Date"""


class Album(Model):
    __tablename__ = "sign_albums"

    gid: Mapped[int] = mapped_column(primary_key=True)
    """Group ID"""
    uid: Mapped[int] = mapped_column(primary_key=True)
    """User ID"""
    stamp_id: Mapped[int] = mapped_column(primary_key=True)
    """Stamp ID"""
    collected: Mapped[bool] = mapped_column(default=False)
    """Whether the stamp is collected"""


class Sign(TypedDict):
    user_name: str
    affection: int
    affection_total: int
    stamp: str
    background_image: str
    rank: int
    todo: str
    hitokoto: str
