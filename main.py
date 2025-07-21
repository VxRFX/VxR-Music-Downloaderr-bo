import telebot
import yt_dlp
import os

BOT_TOKEN = '7590984094:AAGuVH13k26Iynyz-BATElSTMiyT3Y7LtB8'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Отправь ссылку на YouTube-видео, и я скачаю тебе музыку 🎵")

@bot.message_handler(func=lambda m: True)
def download_audio(message):
    url = message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        bot.reply_to(message, "Это не ссылка на YouTube 😔")
        return

    bot.reply_to(message, "⏳ Скачиваю музыку...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio_file = 'downloaded.mp3'
        with open(audio_file, 'rb') as f:
            bot.send_audio(message.chat.id, f)

        os.remove(audio_file)

    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

bot.polling()
