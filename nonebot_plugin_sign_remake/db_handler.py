from sqlalchemy import func, select
from nonebot_plugin_orm import async_scoped_session

from .models import Album


async def get_group_rank(
    user_id: str, group_id: str, session: async_scoped_session
) -> int:
    rank_orign = await session.execute(
        select(Album.uid, func.count())
        .where(Album.gid == group_id, Album.collected == 1)
        .group_by(Album.uid)
        .order_by(func.count().desc())
    )
    users = rank_orign.all()
    rank = next((i + 1 for i, u in enumerate(users) if str(u[0]) == user_id), None)
    return rank or 0


async def get_collected_stamps(
    group_id: str, user_id: str, session: async_scoped_session
) -> list[int]:
    stamps = await session.execute(
        select(Album.stamp_id).where(
            Album.gid == group_id, Album.uid == user_id, Album.collected == 1
        )
    )
    return list(stamps.scalars().all())
