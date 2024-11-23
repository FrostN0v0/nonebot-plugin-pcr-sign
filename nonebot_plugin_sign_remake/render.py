from nonebot_plugin_htmlrender import template_to_pic

from .models import Sign
from .config import TEMPLATES_DIR


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
        },
        pages={
            "viewport": {"width": 360, "height": 10},
            "base_url": f"file://{TEMPLATES_DIR}",
        },
    )
