try:
    from clilte import CommandLine
except ImportError as e:
    raise ImportError(
        "请使用 `pip install nonebot-plugin-pcr-sign[cli]` 安装所需依赖"
    ) from e
from arclet.alconna import Argv, set_default_argv_type

from .plugins.migrate import Migrate

set_default_argv_type(Argv)
pcr = CommandLine(
    "NB CLI plugin for nonebot-plugin-pcr-sign",
    "0.3.0",
    rich=True,
    _name="nb pcr",
    load_preset=True,
)
pcr.add(Migrate)
