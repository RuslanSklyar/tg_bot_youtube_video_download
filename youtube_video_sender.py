import telebot
from pytube import YouTube

bot = telebot.TeleBot('token')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введите URL адрес видео которое хотите скачать с YouTube")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if "www.youtube.com/watch" in message.text:
        yt = YouTube(message.text)  # текст ссылки
        stream = yt.streams.get_by_itag(22)  # выбираем по тегу, в каком формате будем скачивать.
        download(message, stream)


def download(message, stream):
    stream.download(filename="video.mp4")  # загружаем видео.
    send_v(message)  # вызываем ф-цию отправки видео


@bot.message_handler()
def send_v(message):
    try:
        video = open('video.mp4', 'rb')
        bot.send_video(message.chat.id, video)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(message.chat.id, "Видео больше 50МБ, его не удалось отправить.")


bot.polling(none_stop=True)
