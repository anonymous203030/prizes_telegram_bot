import logging

from telethon import Button

logging.basicConfig(format = '[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level = logging.WARNING)
import tracemalloc

tracemalloc.start()
# Bot information
BOT_TOKEN = '1673225369:AAHikNw_smgBxaEf_EhA865lEROccihr4OY'
API_ID = 1896955
API_HASH = '5851d713142f82d15774a5cfa11210e4'
SESSION_STRING_BOT = 'bot'

# Bpt buttons

PAYMENT_BUTTON = [Button.inline('Пополнить счет', b'payment')]
PAYMENT_BUTTON_1 = [Button.inline('Пополнить на 250', b'payment_250')]
PAYMENT_BUTTON_2 = [Button.inline('Пополнить на 500', b'payment_500')]
PAYMENT_BUTTON_3 = [Button.inline('Пополнить на 1000', b'payment_1000')]
PAYMENT_BUTTON_4 = [Button.inline('Пополнить на 2000', b'payment_2000')]

INFO_BUTTON = [Button.inline('Информация', b'info')]
BOXES_BUTTON = [Button.inline('Призы', b'boxes')]
HOW_TO_OPEN_BUTTON = [Button.inline('Как открыть коробку?', b'how_to_open')]
BACK_BUTTON = [Button.inline('Обратно', b'back')]
PHONE_BUTTON = [Button.request_phone('Верификация Телефона')]
INVENTORY_BUTTON = [Button.inline('Инвентарь', b'inventory')]

# Box Buttons
OPEN_BOX_1_BUTTON = [Button.inline('Открыть Коробку "Базовый Кейс"(250р)', b'open_250')]
OPEN_BOX_2_BUTTON = [Button.inline('Открыть Коробку "Базовый Кейс"(500р)', b'open_500')]
OPEN_BOX_3_BUTTON = [Button.inline('Открыть Коробку "Кейс для Вельмож"(1000р)', b'open_1000')]
OPEN_BOX_4_BUTTON = [Button.inline('Открыть Коробку "Кейс для Маценатов"(2000р)', b'open_2000')]

# Bot messages
START = ['/start', 'start', 'run', 'hi', 'hello', '/run']

START_MESSAGE = 'Вас Приветствует Призовой Бот в котором вы можете выиграть много-чего крутого!'

BOX_INSIDE = 'Базовый Кейс (250 рублей)\n' \
             '1 час игры за пк\n' \
             'Полчаса игры за PS\n' \
             'Полчаса игры за ПК\n' \
             'Кейс для бояр (500 рублей)\n' \
             'Батончик\n' \
             '1.5 часа за PC\n' \
             'Кола (0.5)\n' \
             'Пакет в зал Стандарт (ночной)\n' \
             'Кейс для Вельмож (1000 рублей)\n' \
             'Пакет в зал VIP (утренний)\n' \
             'Кола и батончик\n' \
             '3 часа за PS\n' \
             'Кейс для Меценатов (2000 рублей)\n' \
             'Абонемент на посещение клуба (на все выходные)\n' \
             'Кальян\n' \
             'Пакет в зал VIP (ночной)'

HOW_TO_OPEN = 'Как открыть коробку?' \
              'Всего три простых шага!\n\n' \
              '1️) Пополняй свой аккаунт Good Game в любом из наших киберспортивных клубов от 250 ₽ за 24 суммарно;\n' \
              '2️) Нажми на кнопку  "Открыть Коробку удачи"\n' \
              '3️) Выигрывай призы!\n' \
              'Все призы можно получить у администратора.\n' \
              'Подробнее о всех призах в разделе "🎁 Призы 🎁"'

INFO = 'О чем-бы вы хотели быть проинформированы?\n' \
       'Как открыть коробку?\n' \
       '🎁Призы🎁'

PAYMENT = 'Вы можете пополнить ваш баланс на 250р, 500р, 1000р и 2000р'

CHOICES = {250: ['1 час игры за пк', 'Полчаса игры за PS', 'Полчаса игры за ПК'],
           500: ['Батончик', '1.5 часа за PC', 'Кола (0.5)',
                 'Пакет в зал Стандарт (ночной)'],
           1000: ['Пакет в зал VIP (утренний)', 'Кола и батончик',
                  '3 часа за PS'],
           2000: ['Абонемент на посещение клуба (на все выходные)',
                  'Кальян',
                  'Пакет в зал VIP (ночной)']
           }
