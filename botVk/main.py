#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, '../')

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import vk_api
from datetime import datetime
import random
import data
from datetime import datetime, timedelta

# login, password='login','password'
# vk_session = vk_api.VkApi(login, password)
# vk_session.auth()

vk_session = vk_api.VkApi(token=data.token_group())

# session_api = vk_session.get_api()
vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)


# def send_message(peer_id, message=None, attachment=None, keyboard=None, payload=None):
#     session_api.messages.send(peer_id=peer_id, message=message, random_id=random.randint(-2147483648, +2147483648),
#                               attachment=attachment, keyboard=keyboard, payload=payload)

dict_status = {}
dict_status_buy = {}
status_buy = True


def create_keyboard(response):
    keyboard = VkKeyboard(one_time=False)
    if response == "/help" or response == "!начать" or response == "!старт" or response == "старт" or response == "начать" or response == "назад" or response == "/start" or response == "start" or response == "!start":
        keyboard.add_button('Купить', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Продать', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Пруфы', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()

        keyboard.add_button('Отключить бота', color=VkKeyboardColor.NEGATIVE)
    elif response == 'купить':
        keyboard.add_button('100к', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('500к', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('1кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('5кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Другое', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)

    elif response == 'продать':
        keyboard.add_button('До 1кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('1кк-5кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('5кк-15кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('От 15кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)

    elif response == 'отключить бота':
        print('Отключаю')
        return keyboard.get_empty_keyboard()


    keyboard = keyboard.get_keyboard()
    return keyboard

# def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
#     vk_session.method('messages.send',
#                       {id_type: id, 'message': message,
#                        'random_id': random.randint(-2147483648, +2147483648),
#                        "attachment": attachment,
#                        'keyboard': keyboard})

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            tomorrow = datetime.strftime(datetime.now() + timedelta(days=1), "%d%m%Y")

            if vk.messages.search(peer_id=event.user_id, date=tomorrow, count=1)['count'] == 1:
                vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                 message='Здравствуй! Мы рады видеть тебя здесь. Скорее пиши "Старт", чтобы активировать бота.')
            else:
                if dict_status.get(event.user_id) == None:
                    dict_status[event.user_id] = True
                print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                print('Текст сообщения: ' + str(event.text))
                print(event.user_id)
                response = event.text.lower()
                keyboard = create_keyboard(response)

                if event.from_user and not event.from_me:
                    if response == "/help" or response == "!начать" or response == "!старт" or response == "старт" or response == "начать" or response == "/start" or response == "start" or response == "!start":
                        dict_status[event.user_id] = True
                        dict_status_buy[event.user_id] = False
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='Другие доступные команды: \n/купить - Данная команда вызывает инструкцию для покукпки VKCs.\n/продать - Данныя подсказка вызывает инструкцию, которая помагает вам продать нам коины.\n/пруфы - Данная команда предоставит вам доказательство, что мы не мошенники.',
                                     keyboard=keyboard)

                    elif response == "купить" and dict_status.get(event.user_id) == True:
                        dict_status_buy[event.user_id] = True
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message='Выберите товар из списка и нажмите "Написать продавцу" .\nКаталог товаров - https://vk.com/market-151512230', keyboard=keyboard)

                    elif response == "продать" and dict_status.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message='Выберите сумму, которую хотите продать. Обязательно приложите скрин баланса, доказывающий наличии указанной суммы', keyboard=keyboard)

                    elif response == 'пруфы' and dict_status.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message='Все пруфы можно найти в обсуждениях группы. Обсуждения - https://vk.com/board151512230')

                    elif response == 'отключить бота' and dict_status.get(event.user_id) == True:
                        dict_status[event.user_id] = False
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message='Если вы хотите снова включить бота, напишите "Старт"', keyboard=keyboard)

                    elif response == 'включить бота' and dict_status.get(event.user_id) == False:
                        dict_status[event.user_id] = True
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message='Включить бота', keyboard=keyboard)
                    elif response == 'назад'  and dict_status.get(event.user_id) == True:
                        dict_status_buy[event.user_id] = False
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='Выберите действие.', keyboard=keyboard)

                if event.from_user and not event.from_me:
                    if response == '100к' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='https://vk.com/market-151512230?w=product-151512230_2423932')
                    elif response == '500к' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='https://vk.com/market-151512230?w=product-151512230_2423937%2Fquery')
                    elif response == '1кк' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='https://vk.com/market-151512230?w=product-151512230_2423940%2Fquery')
                    elif response == '5кк' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='https://vk.com/market-151512230?w=product-151512230_2428516%2Fquery')
                    elif response == 'другое' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='Отправьте сообщение с суммой которую хотите приобрести.\nОбразец - #купить 50кк\nПисать сюда - https://vk.com/chyika2015')

                if event.from_user and not event.from_me:
                    if status_buy == True:
                        msg = 'Ожидайте ответа, я позвал администратора.'
                    else:
                        msg = 'Простите, но в данный момент скупка приостановленна.'
                    if response == 'до 1кк':
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message=msg)
                    elif response == '1кк-5кк':
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message=msg)
                    elif response == '5кк-15кк':
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message=msg)
                    elif response == 'от 15кк':
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message=msg)

                print('-' * 30)
                print(dict_status.get(269593957))

