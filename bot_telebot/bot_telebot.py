import telebot
from telebot import types
import logging
from googlesearch import search
from simple_image_download import simple_image_download as simp
import glob
import os
import datetime
from datetime import datetime
import wikipedia, re
wikipedia.set_lang("ru")
from database import insert_dataset



group_chat_id = -1001435928850
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot_commands = ("/start", "/help", "/button")  # Список команд
bot_token = os.environ.get('BOT_TOKEN')  # ENV токена
bot = telebot.TeleBot(bot_token)
immages = simp.simple_image_download
tb = telebot.TeleBot(bot_token)
download_count = 9  # Надо вывести в следующей версии в инпут пользователя



def porn_searth(message):
    text = message.text
    text_search = text.replace(' ', '+')
    bot.send_message(message.chat.id, f"https://www.xvideos.com/?k={text_search}")


def handle_text(message):
    log(message)
    id = message.from_user.id
    chat_id = message.chat.id
    user_text = message.text
    name = message.from_user.first_name
    insert_dataset(id, chat_id, user_text, name)


def log(message):
    print("<!------!>")
    print(datetime.now())
    print("Сообщение от {0} {1} (id = {2}) \n {3}".format(message.from_user.first_name,
                                                          message.from_user.last_name,
                                                          str(message.from_user.id), message.text))


def getwiki(message):
    s = message.text
    handle_text(message)
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем
                    # утерянные при разделении строк точки на место
                if len((x.strip()))>3:
                   wikitext2= wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        bot.send_message(message.chat.id, wikitext2)
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        bot.send_message(message.chat.id, 'В энциклопедии нет информации об этом')


def message_reply(message):
    log(message)
    images_to_push = message.text
    bot.send_message(message.chat.id, f'Начался поиск картинок по запросу "{images_to_push}"')
    query_replace = images_to_push.replace(' ', '_')  # Замена пробелов на символ "_" с которым работает библиотека
    handle_text(message)
    my_results_list = []

    for image_result in search(query_replace,  # The query you want to run
                               tld='com',  # The top level domain
                               lang='en',  # The language
                               num=3,  # Number of results per page
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
    log(message_search)
    handle_text(message_search)
    text = message_search.text
    bot.send_message(message_search.chat.id, f'Начался поиск ссылок по запросу "{text}"')
    query = text
    links = []
    for j in search(query, tld="co.in", num=5, stop=1, pause=0):
        links_send = ''.join(j)
        links.append(links_send)
    bot.send_message(message_search.chat.id, links)


@bot.message_handler(commands=["start"])
def start(start_bot):
    log(start_bot)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    google_search = types.KeyboardButton('/search')
    markup.add(google_search)
    photo_search = types.KeyboardButton("/photos")
    markup.add(photo_search)
    wiki_search = types.KeyboardButton("/wiki")
    markup.add(wiki_search)
    # porn = types.KeyboardButton("/porn")
    # markup.add(porn)
    bot.send_message(start_bot.chat.id, 'Выберете что будем делать', reply_markup=markup)


# @bot.message_handler(commands=["porn"])
# def stop(message):
#     log(message)
#     handle_text(message)
#     if "/porn" in message.text:
#         bot.register_next_step_handler(message, porn_searth)


@bot.message_handler(commands=["stop"])
def stop(message):
    log(message)
    handle_text(message)
    if "/stop" in message.text:
        bot.send_message(message.chat.id, "Меня не остановить!")


@bot.message_handler(commands=["wiki"])
def wiki(message):
    log(message)
    handle_text(message)
    if "/wiki" in message.text:
        bot.register_next_step_handler(message, getwiki)


@bot.message_handler(commands=["search"])
def wiki(message_search):
    log(message_search)
    handle_text(message_search)
    if "/search" in message_search.text:
        bot.register_next_step_handler(message_search, getgoogle)


@bot.message_handler(commands=["photos"])
def photos(message):
    log(message)
    handle_text(message)
    if "/photos" in message.text:
        bot.register_next_step_handler(message, message_reply)


bot.infinity_polling()

# ПОПРОБОВАТЬ ЗАЮЗАТЬ SHELL SH ДЛЯ УДАЛЕНИЯ СРАНЫХ КАРТИНОК
