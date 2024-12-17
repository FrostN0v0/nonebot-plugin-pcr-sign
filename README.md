<!-- markdownlint-disable MD033 MD036 MD041 MD046 -->
<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="./docs/NoneBotPlugin.svg" width="300"  alt="NoneBotPluginLogo"></a>
  <br>
</div>

<div align="center">

# nonebot-plugin-pcr-sign

_✨ pcr签到 集印章/邮戳 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/FrostN0v0/nonebot-plugin-pcr-sign.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-pcr-sign">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-pcr-sign.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<a href="https://results.pre-commit.ci/latest/github/FrostN0v0/nonebot-plugin-pcr-sign/master">
    <img src="https://results.pre-commit.ci/badge/github/FrostN0v0/nonebot-plugin-pcr-sign/master.svg" alt="pre-commit.ci status">
</a>
<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-pcr-sign:nonebot_plugin_pcr_sign">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin%2Fnonebot-plugin-pcr-sign" alt="NoneBot Registry" />
</a>
<a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
</a>
<a href="https://github.com/astral-sh/ruff">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="ruff">
</a>
<a href="https://www.codefactor.io/repository/github/frostn0v0/nonebot-plugin-pcr-sign"><img src="https://www.codefactor.io/repository/github/frostn0v0/nonebot-plugin-pcr-sign/badge" alt="CodeFactor" />
</a>

</div>

## 📖 介绍

一个从
<code>一个从 hoshino <del>抄</del>借鉴的 nonebot2 签到插件<a href="https://github.com/zhulinyv/nonebot_plugin_hoshino_sign">nonebot-plugin-hoshino-sign</a>
</code>**~~抄~~借鉴**的 nonebot2 签到插件

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-pcr-sign

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-pcr-sign
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-pcr-sign
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-pcr-sign
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-pcr-sign
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_pcr_sign"]

</details>

## ⚙️ 配置

### 配置表

在 nonebot2 项目的`.env`文件中修改配置项

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| sign_argot_expire_time | 否 | 300 | 暗语过期时间（单位：`秒` 类型：`int`） |
| stamp_path | 否 | RES_DIR / "stamps" | 印章图片路径 |
| sign_background_source | 否 | "default" | 签到背景图来源 |
| album_background_source | 否 | "default" | 收集册背景图来源 |

### background_source

`sign_background_source` 为签到背景图来源，可选值为字面量 `default` / `LoliAPI` / `Lolicon` / `random` 或者结构 `CustomSource` 。`LoliAPI` 和  `Lolicon` 均为网络请求获取随机背景图，`random`为从[默认签到背景目录](/nonebot_plugin_pcr_sign/resources/images/sign_background/)中随机, `CustomSource` 用于自定义背景图。 默认为 `default`。

`album_background_source` 为收集册背景图来源，可选值为字面量 `default` / `kraft` / `pcr` / `prev` / `random` 或者结构 `CustomSource` 。前四者均为预设背景，`random`为从[默认收集册背景目录](/nonebot_plugin_pcr_sign/resources/images/album_background/)中随机，`CustomSource` 用于自定义背景图。 默认为 `default`。

以下是 `CustomSource` 用法

在配置文件中设置 `xxx_background_source` 为 `CustomSource`结构的字典

<details>
  <summary>CustomSource配置示例</summary>

- 网络链接

  - `uri` 可为网络图片 API，只要返回的是图片即可
  - `uri` 也可以为 base64 编码的图片，如 `data:image/png;base64,xxxxxx` ~~（一般也没人这么干）~~

```env
sign_background_source = '{"uri": "https://example.com/image.jpg"}'
```

- 本地图片

> [!TIP]
>
> - `uri` 也可以为本地图片路径，如 `imgs/image.jpg`、`/path/to/image.jpg`
> - 如果本地图片路径是相对路径，会使用 [`nonebot-plugin-localstore`](https://github.com/nonebot/plugin-localstore) 指定的 data 目录作为根目录
> - 如果本地图片路径是目录，会随机选择目录下的一张图片作为背景图

```env
sign_background_source = '{"uri": "/imgs/image.jpg"}'
```

</details>

## 🎉 使用

> [!NOTE]
> 记得使用[命令前缀](https://nonebot.dev/docs/appendices/config#command-start-%E5%92%8C-command-separator)哦

### 🪧 指令表

| 指令 | 权限 | 参数 | 说明 |
|:-----:|:----:|:----:|:----:|
| sign/签到/盖章/妈 | 所有 | 无 | 签到 |
| album/收集册 | 所有 | `无` or `@` | 查看自己（或别人）的收集册 |

### 🫣 暗语表

> [!NOTE]
> 🧭 暗语使用~~指北~~
>
> 暗语消息来自 [nonebot-plugin-argot](https://github.com/KomoriDev/nonebot-plugin-argot) 插件
>
> 对暗语对象`回复对应的暗语指令`即可获取暗语消息

| 暗语指令 | 对象 | 说明 |
|:-----:|:----:|:----:|
| `background` | [`签到图`](#-签到图) | 查看背景图 |
| `stamp` | [`签到图`](#-签到图) | 获取印章图 |
| `raw` | [`签到图`](#-签到图) | 获取原文字消息 |

> [!TIP]
> 注意暗语消息有过期时间，默认 5min 后失效，可通过[配置](#配置表)修改

### 📸 效果图

#### 🐾 签到图

![示例图1](docs/example-1.png)

#### 🎞️ 收集册

![示例图2](docs/example-2.png)

## 💖 鸣谢

- [`KomoriDev`](https://github.com/KomoriDev): 优秀的界面风格和设计理念学习
- [`nonebot-plugin-hoshino-sign`](https://github.com/zhulinyv/nonebot_plugin_hoshino_sign)：灵感来源
- [`SonderXiaoming/login_bonus`](https://github.com/SonderXiaoming/login_bonus): 灵感来源的来源
- [`GWYOG-Hoshino-plugins`](https://github.com/GWYOG/GWYOG-Hoshino-plugins#8-%E6%88%B3%E6%9C%BA%E5%99%A8%E4%BA%BA%E9%9B%86%E5%8D%A1%E5%B0%8F%E6%B8%B8%E6%88%8Fpokemanpcr): 灵感来源的来源的来源
- [`公主连结吧`](https://tieba.baidu.com/p/6769790810): 印章素材来源
- [`nonebot-plugin-argot`](https://github.com/KomoriDev/nonebot-plugin-argot): 优秀的 NoneBot2 暗语支持
- [`nonebot-plugin-htmlrender`](https://github.com/kexue-z/nonebot-plugin-htmlrender): 优秀的 NoneBot2 HTML 渲染支持
- [`nonebot-plugin-orm`](https://github.com/nonebot/plugin-orm): 优秀的 NoneBot2 数据库支持

## 📋 TODO

- [ ] 数据迁移脚本(从原hoshino_sign插件迁移数据)
- [ ] 待补充,欢迎pr
