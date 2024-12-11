from nonebot_plugin_htmlrender import template_to_pic

from .models import Sign
from .config import TEMPLATES_DIR
from .utils import img_list, image_cache, get_album_background


async def render_sign(data: Sign) -> bytes:
    return await template_to_pic(
        template_path=str(TEMPLATES_DIR),
        template_name="sign_card.html.jinja2",
        templates={
            "background_image": data["background_image"],
            "user_name": data["user_name"],
            "stamp": data["stamp"],
            "todo": data["todo"],
            "hitokoto": data["hitokoto"],
            "affection": data["affection"],
            "affection_total": data["affection_total"],
            "rank": data["rank"],
            "is_new": data["is_new"],
        },
        pages={
            "viewport": {"width": 360, "height": 10},
            "base_url": f"file://{TEMPLATES_DIR}",
        },
    )


async def render_album(collected_stamps: list[int]) -> bytes:
    return await template_to_pic(
        template_path=str(TEMPLATES_DIR),
        template_name="album.html.jinja2",
        templates={
            "stamp_list": img_list,
            "image_cache": image_cache,
            "collected_list": collected_stamps,
            "background_image": await get_album_background(),
        },
        pages={
            "viewport": {"width": 1440, "height": 10},
            "base_url": f"file://{TEMPLATES_DIR}",
        },
        device_scale_factor=1,
    )
