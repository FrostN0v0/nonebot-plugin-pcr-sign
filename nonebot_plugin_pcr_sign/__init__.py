import random
from datetime import date

from nonebot import logger, require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_uninfo")
require("nonebot_plugin_alconna")
require("nonebot_plugin_argot")
require("nonebot_plugin_orm")
require("nonebot_plugin_htmlrender")
from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_argot import add_argot
from nonebot_plugin_alconna.uniseg import At
from nonebot_plugin_orm import async_scoped_session
from nonebot_plugin_alconna import (
    Args,
    Match,
    Alconna,
    UniMessage,
    CommandMeta,
    on_alconna,
)

from .config import config
from .models import Sign, User, Album
from .render import render_sign, render_album
from .db_handler import get_group_rank, get_collected_stamps
from .utils import (
    img_list,
    todo_list,
    image_cache,
    get_hitokoto,
    get_message_id,
    image_to_base64,
    get_background_image,
)

__plugin_meta__ = PluginMetadata(
    name="PCR签到重制版",
    description=(
        "对“从 hoshino 搬来的 pcr 签到”插件"
        "nonebot_plugin_hoshino_sign 的搬运重制（我搬两遍"
    ),
    usage=("发送 sign/签到/盖章/妈 进行签到\n发送 收集册/排行榜/图鉴 显示自己的收集册"),
    type="application",
    homepage="https://github.com/FrostN0v0/nonebot-plugin-pcr-sign",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna", "nonebot_plugin_uninfo"
    ),
    extra={
        "author": "FrostN0v0 <1614591760@qq.com>",
        "version": "0.2.0",
    },
)

sign = on_alconna(
    Alconna(
        "sign",
        meta=CommandMeta(
            description=__plugin_meta__.description,
            usage=__plugin_meta__.usage,
            example="签到",
        ),
    ),
    block=True,
    use_cmd_start=True,
    aliases=("盖章", "签到", "妈!"),
)

stamp_album = on_alconna(
    Alconna(
        "album",
        Args["target?#目标", At | int],
        meta=CommandMeta(
            description=__plugin_meta__.description,
            usage=__plugin_meta__.usage,
            example="收集册",
        ),
    ),
    block=True,
    use_cmd_start=True,
    aliases=("收集册", "排行榜", "图鉴"),
)


@sign.handle()
async def _(user_session: Uninfo, session: async_scoped_session):
    user_name = user_session.user.name if user_session.user.name is not None else "None"
    user_id = user_session.user.id
    group_id = user_session.scene.id
    todo = random.choice(todo_list)
    affection = random.randint(1, 10)
    stamp_id = random.choice(img_list).stem
    stamp_img = image_to_base64(image_cache[stamp_id])
    background_image = await get_background_image()
    hitokoto = await get_hitokoto()
    is_new: bool = False
    if user := await session.get(User, (group_id, user_id)):
        if user.last_sign == date.today():
            await UniMessage(f"{user_name}，今天已经签到过啦，明天再来叭~").finish(
                reply_to=True
            )
        else:
            rank = await get_group_rank(user_id, group_id, session)
            user.last_sign = date.today()
            user.affection += affection
            raw_msg = (
                f"欢迎回来，主人~！\n"
                f"好感+{affection}！当前好感：{user.affection}\n"
                f"主人今天要{todo}吗？\n\n今日一言：{hitokoto}"
            )
            if record := await session.get(Album, (group_id, user_id, stamp_id)):
                is_new = False
                record.collected = True
            else:
                is_new = True
                session.add(
                    Album(gid=group_id, stamp_id=stamp_id, uid=user_id, collected=True)
                )
            result = Sign(
                user_name=user_name,
                affection=affection,
                affection_total=user.affection,
                stamp=stamp_img,
                background_image=str(background_image),
                hitokoto=hitokoto,
                rank=rank,
                todo=todo,
                is_new=is_new,
            )
            await session.commit()
            image = await render_sign(result)
            msg = await UniMessage.image(raw=image).send(
                at_sender=True,
                argot={
                    "name": "background",
                    "command": "background",
                    "content": str(background_image),
                    "expire": config.sign_argot_expire_time,
                },
            )
            msg_id = await get_message_id(msg.msg_ids)
            await add_argot(
                name="stamp",
                message_id=str(msg_id),
                content=str(stamp_img),
                command="stamp",
                expire_time=config.sign_argot_expire_time,
            )
            await add_argot(
                name="raw",
                message_id=str(msg_id),
                content=raw_msg,
                command="raw",
                expire_time=config.sign_argot_expire_time,
            )
            logger.debug(
                f"群{group_id} | {user_name}({user_id})签到成功,"
                f"印章ID:{stamp_id}, 新获得：{is_new}"
            )
            await sign.finish()
    else:
        session.add(
            User(gid=group_id, uid=user_id, affection=affection, last_sign=date.today())
        )
        raw_msg = (
            f"欢迎回来，主人~！\n"
            f"好感+{affection}！当前好感：{affection}\n"
            f"主人今天要{todo}吗？\n\n今日一言：{hitokoto}"
        )
        result = Sign(
            user_name=user_name,
            affection=affection,
            affection_total=affection,
            stamp=stamp_img,
            background_image=str(background_image),
            hitokoto=hitokoto,
            rank=await get_group_rank(user_id, group_id, session),
            todo=todo,
            is_new=True,
        )
        session.add(Album(gid=group_id, stamp_id=stamp_id, uid=user_id, collected=True))
        image = await render_sign(result)
        await session.commit()
        msg = await UniMessage.image(raw=image).send(
            at_sender=True,
            argot={
                "name": "background",
                "command": "background",
                "content": str(background_image),
                "expire": config.sign_argot_expire_time,
            },
        )
        msg_id = await get_message_id(msg.msg_ids)
        await add_argot(
            name="stamp",
            message_id=str(msg_id),
            content=str(stamp_img),
            command="stamp",
            expire_time=config.sign_argot_expire_time,
        )
        await add_argot(
            name="raw",
            message_id=str(msg_id),
            content=raw_msg,
            command="raw",
            expire_time=config.sign_argot_expire_time,
        )
        logger.debug(
            f"群{group_id} | {user_name}({user_id})签到成功,"
            f"印章ID:{stamp_id}, 新获得：{is_new}"
        )
        await sign.finish()


@stamp_album.handle()
async def _(
    user_session: Uninfo,
    session: async_scoped_session,
    target: Match[At | int],
):
    if target.available:
        if isinstance(target.result, At):
            user_id = target.result.target
        else:
            user_id = target.result
    else:
        user_id = user_session.user.id
    group_id = user_session.scene.id
    group_rank = await get_group_rank(str(user_id), group_id, session)
    collected_stamps = await get_collected_stamps(group_id, str(user_id), session)
    image = await render_album(collected_stamps)
    msg = UniMessage.image(raw=image)
    msg += UniMessage.text(f"图鉴完成度：{len(collected_stamps)}/{len(img_list)}\n")
    msg += UniMessage.text(f"当前群排名：{group_rank}")
    await msg.send(reply_to=True)
