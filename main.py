import telebot
from flask import Flask, request
import yt_dlp
import os

TOKEN = "7794349596:AAEVqwZXfRD5QD-ibSuHgU9XeKnd5Dc6HS8"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎬 Отправь ссылку на TikTok / YouTube / Instagram, и я скачаю видео без водяных знаков!")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    bot.send_message(message.chat.id, "🔁 Скачиваю...")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(filename)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")

@server.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@server.route("/")
def index():
    return "Bot is running!"

bot.remove_webhook()
bot.set_webhook(url='https://telegram-video-downloader-bot.c03681679.repl.co/' + TOKEN)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
