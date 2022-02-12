import telebot
import logging
from googlesearch import search
from simple_image_download import simple_image_download as simp
import glob
import os

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot_commands = ("/start", "/help", "/button")  # Список команд
bot_token = os.environ.get('BOT_TOKEN')  # ENV токена
bot = telebot.TeleBot(bot_token)
immages = simp.simple_image_download
tb = telebot.TeleBot(bot_token)
download_count = 6  # Надо вывести в следующей версии в инпут пользователя


@bot.message_handler(content_types='text')
def message_reply(message):
    images_to_push = message.text
    query_replace = images_to_push.replace(' ', '_')  # Замена пробелов на символ "_" с которым работает библиотека

    my_results_list = []
    bot.send_message(message.chat.id, f'Начался поиск картинки с названием - "{images_to_push}"')
    for image_result in search(query_replace,  # The query you want to run
                               tld='com',  # The top level domain
                               lang='en',  # The language
                               num=1,  # Number of results per page
                               start=3,  # First result to retrieve
                               stop=1,  # Last result to retrieve
                               pause=2.0,  # Lapse between HTTP requests
                               ):

        immages().download(f'{query_replace}', download_count)
        my_results_list.append(image_result)  # Запись ссылок на картинки в массив

        bot.reply_to(message, image_result)

    # for i in range(3, download_count):
    #     photo_send_lost_2 = glob.glob(
    #         f'.\\simple_images\\{query_replace}\\{query_replace}_{i}.*'  # Путь до только что скаченного файла
    #     )
    #     photo_send = ''.join(photo_send_lost_2)
    #     print(photo_send)
    #     bot.send_photo(message.chat.id, photo=open(photo_send, 'rb'))
    photos = []
    for i in range(3, download_count):
        photo_send_lost_2 = glob.glob(
            f'.\\simple_images\\{query_replace}\\{query_replace}_{i}.*'  # Путь до только что скаченного файла
        )
        photo_send = ''.join(photo_send_lost_2)
        print(photo_send)
        # bot.send_photo(message.chat.id, photo=open(photo_send, 'rb'))
        photos.append(telebot.types.InputMediaPhoto(open(photo_send, 'rb')))
    bot.send_media_group(message.chat.id, photos)


    name = message.from_user.first_name
    if message.text == "Лохи":
        bot.send_message(message.chat.id, "От ЛОХА СЛЫШУ!!!!")
    else:
        bot.send_message(message.chat.id, f'Люблю тебя {name}')


bot.infinity_polling()
