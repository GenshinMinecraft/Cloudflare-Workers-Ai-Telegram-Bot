# Cloudflare-Workers-Ai-Telegram-Bot
一个很简单很简单的 Telegram AI Bot，基于 Python + Cloudflare Workers AI API

没有技术含量，可在 [这里](https://developers.cloudflare.com/workers-ai/models/)查看支持的模型

需要配置项: 
- ACCOUNT_ID = Cloudflare 的 Account ID，最简单的获取方式就是打开 Cloudflare Dash，URL 中的那串就是，比如 `41810b51b9f7521da5fea96d12xxxxxx`
- AUTH_TOKEN = [这里](https://dash.cloudflare.com/profile/api-tokens)获取，最好不要使用 Global API
- Chat_MODEL = 对话使用的大模型，默认是阿里云的通义千问，可以在[这里](https://developers.cloudflare.com/workers-ai/models/)查看支持的模型，更改即可，非必要无需更改
- Image_MODEL = 绘图使用的大模型，非必要无需更改
- Audio2Text_MODEL = 语音识别使用的大模型，非必要无需更改 (该功能尚未完工)
- Telegram_Bot_Token = Telegram 的 Bot Token
- ADMIN_ID = Telegram 管理员 ID

PS: 目前所用模型都是 Beta，Beta 模型限时免费，所以你可以随便用而不用担心付费

使用方法: 通过 `/start` 查看
请勿在使用命令时使用 `/start@xxxbot` 这种类型，目前尚未适配，请直接使用 `/start`

Demo Bot: <https://t.me/cloudflareworkersaibot>

TO DO LIST:
- 添加上下文支持
- 适配 `/start@xxxbot` 命令
