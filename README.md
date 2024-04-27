# Cloudflare-Workers-Ai-Telegram-Bot
一个很简单很简单的 Telegram AI Bot，基于 Python + Cloudflare Workers AI API

没有技术含量，可在 [这里](https://developers.cloudflare.com/workers-ai/models/)查看支持的模型

由于只有 30 行，所以也太可能有什么高科技玩意，只是简单的发送信息并回复

需要配置项: 
- `[Telegram Bot Token]`: Telegram 的 Bot Token
- `[Cloudflare Account ID]`: Cloudflare 的 Account ID，最简单的获取方式就是打开 Cloudflare Dash，URL 中的那串就是，比如 `41810b51b9f7521da5fea96d12xxxxxx`
- `[Cloudflare API TOKEN]` [这里](https://dash.cloudflare.com/profile/api-tokens)获取，最好不要使用 Global API
- `MODEL`: 默认是阿里云的通义千问，可以在[这里](https://developers.cloudflare.com/workers-ai/models/)查看支持的模型，更改即可

就这样吧，Workers 刚出，每天免费 1w tokens 貌似
