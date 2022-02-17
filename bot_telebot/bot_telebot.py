import telebot
from telebot import types
import logging
from googlesearch import search
from simple_image_download import simple_image_download as simp
import glob
import os
import datetime
from datetime import datetime


group_chat_id = -1001435928850
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot_commands = ("/start", "/help", "/button")  # Список команд
bot_token = os.environ.get('BOT_TOKEN')  # ENV токена
bot = telebot.TeleBot(bot_token)
immages = simp.simple_image_download
tb = telebot.TeleBot(bot_token)
download_count = 9  # Надо вывести в следующей версии в инпут пользователя


def log(message):
    print("<!------!>")
    print(datetime.now())
    print("Сообщение от {0} {1} (id = {2}) \n {3}".format(message.from_user.first_name,
                                                          message.from_user.last_name,
                                                          str(message.from_user.id), message.text))


def message_reply(message):
    # log(message)
    images_to_push = message.text
    bot.send_message(message.chat.id, f'Начался поиск картинок по запросу "{images_to_push}"')
    query_replace = images_to_push.replace(' ', '_')  # Замена пробелов на символ "_" с которым работает библиотека

    my_results_list = []

    for image_result in search(query_replace,  # The query you want to run
                               tld='com',  # The top level domain
                               lang='en',  # The language
                               num=1,  # Number of results per page
                               start=10,  # First result to retrieve
                               stop=1,  # Last result to retrieve
                               pause=0,  # Lapse between HTTP requests
                               ):
        immages().download(f'{query_replace}', download_count)
        my_results_list.append(image_result)  # Запись ссылок на картинки в массив

    photos = []
    photo_len = len(my_results_list)
    for i in range(photo_len, download_count):
        photo_send_lost_2 = glob.glob(
            f'.\\simple_images\\{query_replace}\\{query_replace}_{i}.*'  # Путь до только что скаченного файла
        )

        photo_send = ''.join(photo_send_lost_2)
        print(photo_send)
        photos.append(telebot.types.InputMediaPhoto(open(photo_send, 'rb')))
    bot.send_media_group(message.chat.id, photos)


def getgoogle(message_search):
    text = message_search.text
    bot.send_message(message_search.chat.id, f'Начался поиск ссылок по запросу "{text}"')
    query = text
    links = []
    for j in search(query, tld="co.in", num=1, stop=1, pause=0):
        links_send = ''.join(j)
        links.append(links_send)
    bot.send_message(message_search.chat.id, links)


@bot.message_handler(commands=["start"])
def start(start_bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    photo_search = types.KeyboardButton('/search')
    markup.add(photo_search)
    wiki_search = types.KeyboardButton("/photos")
    markup.add(wiki_search)
    bot.send_message(start_bot.chat.id, 'Выберете что будем делать', reply_markup=markup)


@bot.message_handler(commands=["search"])
def wiki(message_search):
    if "/search" in message_search.text:
        bot.register_next_step_handler(message_search, getgoogle)


@bot.message_handler(commands=["photos"])
def photos(message):
    user_search = message.text
    bot.register_next_step_handler(message, message_reply)

    # @bot.message_handler(content_types='text')
    # def handle_text(message):
    #     chat = message.chat.id
    #     if chat != group_chat_id:
    #         bot.forward_message(group_chat_id, message.chat.id, message.message_id)
    #         print(message.chat.id)
    #         message_reply(message)
    #     else:
    #         message_reply(message)
    # @bot.message_handler(content_types='text')
    # def wiki_text(message_wiki):
    #     bot.send_message(message_wiki.chat.id, getwiki(message_wiki.text))


# @bot.message_handler(lambda message: message.text == "WIKI")
# def wiki_selekt(message):
#     bot.send_message(message.chat.id, 'Введите запрос')

# bot.enable_save_next_step_handlers(delay=2)

bot.infinity_polling()

# ПОПРОБОВАТЬ ЗАЮЗАТЬ SHELL SH ДЛЯ УДАЛЕНИЯ СРАНЫХ КАРТИНОК
