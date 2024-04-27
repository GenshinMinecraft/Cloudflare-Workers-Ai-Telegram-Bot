import requests
import telebot

bot = telebot.TeleBot("[Telegram Bot Token]")

ACCOUNT_ID = "[Cloudflare Account ID]"
AUTH_TOKEN = "[Cloudflare API TOKEN]"
MODEL = "@cf/qwen/qwen1.5-14b-chat-awq"

def GPT(prompt):
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
            "max_tokens": 1024,
            "messages": [
            {"role": "system", "content": "你是一个人工智能助手，用什么语言提问就用什么语言回答"},
            {"role": "user", "content": prompt}
            ]
        }
    )
    result = response.json()
    answer = result.get("result").get("response")
    return answer

@bot.message_handler(func=lambda _: True)
def handle_message(message):
    replytxt = GPT(message.text)
    bot.send_message(chat_id=message.from_user.id, text=replytxt)

bot.polling()
