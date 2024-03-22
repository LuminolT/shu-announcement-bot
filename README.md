# SHU 通知公告转发工具

## 关于

本项目是一个 QQ 频道机器人的实现，用于将[上海大学教务部](https://jwb.shu.edu.cn/)的通知转发到 QQ 频道，便于获取一手消息。

~~这是关于一个一直忘记报名六级的智障儿童的悲惨故事~~

虽说是 SHUSHU 工具，但是你只需要修改 SHUCrawler 类就可以轻松实现对其他网站通知的支持。当然，也可以通过 SHUCrawler 的 method 实现自动发邮件等功能。

## 使用说明

本项目依赖 [QQ Bot Python SDK](https://github.com/tencent-connect/botpy)，你需要通过 [RTF QQ Bot Manual](https://bot.q.qq.com/wiki/) 的方式获得相关配置参数。

同时，你需要在 [QQ Bot 管理端](https://q.qq.com/qqbot)中设置两条指令 `/start` 和 `/stop` 用于调用。


安装依赖：

```bash
pip install -r requirements.txt
```

为了安全性考虑，你需要设置以下环境变量：

```sh
export SHU_BOT_APPID=your_own_qq_bot_appid
export SHU_BOT_SECRET=your_own_qq_bot_secret
```

在启动脚本后，可以通过 `/start` 和 `/stop` 控制机器人。

