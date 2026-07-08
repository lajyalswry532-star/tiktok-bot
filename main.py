import logging
from aiogram import Bot, Dispatcher, types, executor
import yt_dlp
import os

API_TOKEN = os.environ.get('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("أهلاً بك! أرسل لي رابط تيك توك وسأقوم بتحميل الفيديو لك.")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text
    if "tiktok.com" in url:
        await message.reply("جاري التحميل... انتظر قليلاً.")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video.mp4', 'rb') as video:
                await bot.send_video(message.chat.id, video)
            os.remove('video.mp4')
        except Exception as e:
            await message.reply(f"حدث خطأ: {e}")
    else:
        await message.reply("الرجاء إرسال رابط تيك توك صحيح.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
  
