import json
import asyncio
from pathlib import Path
from datetime import datetime

import aiosqlite
from nonebot.log import logger
from clilte import BasePlugin, PluginMetadata
from arclet.alconna.tools import RichConsoleFormatter
from nonebot_plugin_orm import get_scoped_session, async_scoped_session
from arclet.alconna import (
    Args,
    Option,
    Alconna,
    Arparma,
    CommandMeta,
)

from ...models import User, Album


class Migrate(BasePlugin):
    def init(self) -> Alconna | str:
        return Alconna(
            "migrate",
            Option(
                "-d|--data-path",
                Args["db_path", str, "./data/nonebot_plugin_hoshino_sign/"],
                help_text="指定原数据路径",
            ),
            meta=CommandMeta("pcr 迁移相关指令"),
            formatter_type=RichConsoleFormatter,
        )

    def meta(self) -> PluginMetadata:
        return PluginMetadata(
            "Migrate", "0.3.0", "pcr 迁移相关指令", ["migrate"], ["FrostN0v0"]
        )

    def dispatch(self, result: Arparma) -> bool | None:
        session = get_scoped_session()
        base_path = result.db_path
        if not base_path.endswith("/"):
            base_path += "/"
        json_path = base_path + "json/goodwill.json"
        db_path = Path(base_path + "db/pcr_stamp.db")

        new_user_count = 0
        updated_user_count = 0
        original_json_count = 0
        logger.info("开始迁移数据，请不要关闭进程……")
        try:
            with open(json_path, encoding="utf-8") as f:
                json_data = json.load(f)
        except FileNotFoundError as e:
            logger.error(f"未找到数据文件，请检查路径是否正确: {e}")
            return

        original_json_count = sum(len(users) for users in json_data.values())

        logger.info(f"读取到原 JSON 数据条数 {original_json_count} 条")
        for gid, users in json_data.items():
            for uid, data in users.items():
                affection = data[0]
                last_sign_date = datetime.strptime(data[1], "%Y年%m月%d日").date()
                if user := asyncio.run(session.get(User, (int(gid), int(uid)))):
                    user.affection += affection
                    updated_user_count += 1
                else:
                    user = User(
                        gid=int(gid),
                        uid=int(uid),
                        affection=affection,
                        last_sign=last_sign_date,
                    )
                    new_user_count += 1
                session.add(user)
        logger.success(
            f"json数据迁移完成，共计新增用户数据 {new_user_count} 个,"
            f"更新现有用户好感度 {updated_user_count} 个"
        )
        asyncio.run(migrate_album(db_path, session))
        if result.find("migrate"):
            return
        return True

    @classmethod
    def supply_options(cls) -> list[Option] | None:
        return


async def migrate_album(db_path: Path, session: async_scoped_session):
    album_migrated_count = 0
    original_album_count = 0
    async with aiosqlite.connect(db_path) as db:
        logger.info("开始迁移数据库数据，请不要关闭进程……")
        async with db.execute("SELECT gid, uid, cid, num FROM card_record") as cursor:
            rows = await cursor.fetchall()
            original_album_count = len(list(rows))
            logger.info(f"数据库读取成功，原数据读取条数 {original_album_count} 条")
            for row in rows:
                gid, uid, cid, num = row
                if record := await session.get(Album, (gid, uid, cid)):
                    record.collected = True
                else:
                    session.add(Album(gid=gid, uid=uid, stamp_id=cid, collected=num))
                    album_migrated_count += 1
            await session.commit()
            logger.success(f"数据库迁移成功，迁移收集册数据 {album_migrated_count} 条")
