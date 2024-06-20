import requests
import telebot
import os
import time

ACCOUNT_ID = ""
AUTH_TOKEN = ""
Chat_MODEL = "@cf/qwen/qwen1.5-14b-chat-awq"
Image_MODEL = "@cf/stabilityai/stable-diffusion-xl-base-1.0"
Audio2Text_MODEL = "@cf/openai/whisper"
Telegram_Bot_Token = ""
ADMIN_ID = 

bot = telebot.TeleBot(f"{Telegram_Bot_Token}")

user_sessions = {}  # 存储当前用户的历史对话
MAX_HISTORY_LENGTH = 6  # 最大对话历史长度

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        }
    return user_sessions[user_id]

def update_user_session(user_id, message):
    if user_id in user_sessions:
        user_sessions[user_id]['messages'].append({"role": "user", "content": message})
        if len(user_sessions[user_id]['messages']) > MAX_HISTORY_LENGTH:
            del user_sessions[user_id]['messages'][1]  # 删除第二个对话

def ChangeChat_MODEL(MODEL):
	global Chat_MODEL
	Chat_MODEL = MODEL

def GPT(user_id, prompt):

    session = get_user_session(user_id)
    update_user_session(user_id, prompt)
    
    
    response = requests.post(
		f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{Chat_MODEL}",
		headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
		json={
			"max_tokens": 1024,
			"messages": session['messages']
		}
	)
    result = response.json()
    answer = result.get("result").get("response")
    print(answer)
    
    session['messages'].append({"role": "assistant", "content": answer})
    
    return answer

def Image(prompt):
	response = requests.post(
		f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{Image_MODEL}",
		headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
		json={ "prompt": prompt }
	)
	return response.content

def Audio2Text(audio):
	response = requests.post(
		f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{Audio2Text_MODEL}",
		headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
		data=audio
	)
	req = response.content
	print(req)
	audiotext = req.get("result").get("text")
	return audiotext

@bot.message_handler(commands=['start', 'image', 'ai', 'changegptmodel'])
def handle_command(message):
	command = message.text.split()[0]
	print(f"用户 {message.from_user.id} 使用了 {command} 功能，命令是 {message.text}")
	if command == "/start":
		print('start')
		bot.reply_to(message, 
			"""
			Powered By GenshinMinecraft & Cloudflare
			WE LOVE OPEN-SOURCE
								
			基础命令:
			直接发送问题 (仅限私聊): 回复答案
			/ai 问题: 群组内使用
			/image 关键词: 画图
			/changegptmodel 模型: 更改模型，格式: `@xx/xxx/xxx/xx`
			""")
	
	elif command == "/image":
		imageword = (message.text[7:len(message.text)])
		if imageword == '':
			bot.reply_to(message, "绘画提示词不能为空")
			return 0
		try:
			try:
				bot.reply_to(message, "Drawing...", parse_mode='Markdown')
			except:
				bot.send_message(message.chat.id, "Drawing...", parse_mode='Markdown')
				print("为什么有人会删消息啊...")
			png = Image(imageword)
		except:
			print("获取失败")
			try:
				bot.reply_to(message, "呜呜呜~~连不上 Cloudflare 服务器呢~~", parse_mode='Markdown')
				return 1
			except:
				bot.send_message(message.chat.id, "呜呜呜~~连不上 Cloudflare 服务器呢~~", parse_mode='Markdown')
				print("为什么有人会删消息啊...")
				return 1
		bot.send_photo(message.chat.id, png, caption=imageword)
		print(f"绘制完成，提示词 {imageword}")
	
	elif command == "/ai":
		question = (message.text[4:len(message.text)])
		print(f"用户 {message.from_user.id} 使用了 Ask GPT 功能，问题是 {question}")
		try:
			try:
				bot.reply_to(message, "Thinking...", parse_mode='Markdown')
			except:
				bot.send_message(message.chat.id, "Thinking...", parse_mode='Markdown')
				print("为什么有人会删消息啊...")
			replytxt = GPT(message.from_user.id, question)
		except:
			print("获取失败")
			print(Chat_MODEL)
			try:
				bot.reply_to(message, "呜呜呜~~连不上 Cloudflare 服务器呢~~", parse_mode='Markdown')
				return 1
			except:
				bot.send_message(message.chat.id, "呜呜呜~~连不上 Cloudflare 服务器呢~~", parse_mode='Markdown')
				print("为什么有人会删消息啊...")
				return 1
		try:
			bot.reply_to(message, replytxt, parse_mode='Markdown')
		except:
			bot.send_message(message.chat.id, replytxt, parse_mode='Markdown')
			print("为什么有人会删消息啊...")
		
	elif command == "/changegptmodel":
		if message.from_user.id == ADMIN_ID:
			if (message.text[15:len(message.text)]) != '':
				ChangeChat_MODEL(message.text[16:len(message.text)])
				bot.reply_to(message, "GPT 模型已经更改为 "+Chat_MODEL, parse_mode='Markdown')
			else:
				bot.reply_to(message, "模型名不得为空", parse_mode='Markdown')
		else:
			bot.reply_to(message, "非管理员不可使用该命令", parse_mode='Markdown')

	elif command == "/getgptmodel":
		bot.reply_to(message, Chat_MODEL)

# 由于 Cloudflare API 原因，语音转文字暂不开放
#@bot.message_handler(content_types=['audio'])
#def handle_audio(message):
#	print(f"用户 {message.from_user.id} 使用了 Audio2Text 功能")
#	file_id = message.audio.file_id
#	file_info = bot.get_file(file_id)
#	file = bot.download_file(file_info.file_path)
#	print(f"用户 {message.from_user.id} 的 Audio2Text 文件已下载完成")
#	audiotext = Audio2Text(file)
#	bot.reply_to(message, "Audio2Text 结果: "+audiotext)

@bot.message_handler(func=lambda _: True)
def handle_message(message):
	if message.chat.type == "private":
		print(f"用户 {message.from_user.id} 使用了 Ask GPT 功能，问题是 {message.text}")
		try:
			try:
				bot.reply_to(message, "Thinking...", parse_mode='Markdown')
			except:
				bot.send_message(message.chat.id, "Thinking...", parse_mode='Markdown')
				print("为什么有人会删消息啊...")
			replytxt = GPT(message.from_user.id, message.text)
		except:
			print("获取失败")
			print(Chat_MODEL)
			try:
				bot.reply_to(message, "呜呜呜~~连不上 Cloudflare 服务器呢~~", parse_mode='Markdown')
				return 1
			except:
				bot.send_message(message.chat.id, "呜呜呜~~连不上 Cloudflare 服务器呢~~", parse_mode='Markdown')
				print("为什么有人会删消息啊...")
				return 1
		try:
			bot.reply_to(message, replytxt, parse_mode='Markdown')
		except:
			bot.send_message(message.chat.id, replytxt, parse_mode='Markdown')
			print("为什么有人会删消息啊...")
	else:
		return 1
	
bot.polling()
