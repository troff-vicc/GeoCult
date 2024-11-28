import asyncio
import logging
import json
import sqlite3
import random
import math
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.types import CallbackQuery, Message
import yandex_map

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8185175071:AAFCjW-WvT1cZ8wBlJ5IYcr8QuBieW3xC2A")
dp = Dispatcher()

connection = sqlite3.connect('SiteGeoCult/SiteGeoCult/dataPlace.db')
cursor = connection.cursor()

user_data = {}


def coordinate_place(id_place: int):
    dataPlace:str = cursor.execute(f'SELECT coordinate FROM place WHERE id={id_place}').fetchone()[0]
    dataPlace.find(',')
    place_y = dataPlace[:dataPlace.find(',')]
    place_x = dataPlace[dataPlace.find(',')+1:]
    return place_x, place_y


def get_place_SQL(listId: list):
    listPlace = []
    
    for idPlace in listId:
        dataPlace = cursor.execute(f'SELECT * FROM place WHERE id={idPlace}').fetchone()
        listPlace.append(dataPlace)
    
    return listPlace


@dp.callback_query(F.data == 'random_place')
async def send_random_person(call: CallbackQuery):
    count = cursor.execute(f'SELECT Count(id) FROM place').fetchone()
    idPlace = random.randint(0, int(count[0])-1)
    place = get_place_SQL([idPlace])[0]
    #await call.message.answer_photo(place[3])
    idChat = str(call.message.chat.id)
    user_data[idChat] = idPlace
    await call.message.answer(f"{place[1]}\n{place[2]}")


# Получить место
@dp.callback_query(F.data == 'get_place')
async def my_place(call: CallbackQuery):
    with open('SiteGeoCult/SiteGeoCult/data.json', 'r') as json_file:
        data = json.load(json_file)
        idChat = str(call.message.chat.id)
    if idChat in data:
        listPlace = list(data[idChat]['place'])
        if not listPlace:
            listPlace = "Пока ничего нет..."
        else:
            listPlace = get_place_SQL(listPlace)
            print()
    else:
        with open('SiteGeoCult/SiteGeoCult/data.json', 'w') as json_file:
            listPlace = "Пока ничего нет..."
            data[idChat] = {'balance': '500', 'place': []}
            json.dump(data, json_file)
    
    if isinstance(listPlace, str):
        await call.message.answer(listPlace)
    else:
        for place in listPlace:
            #await call.message.answer_photo(place[3])
            await call.message.answer(f"{place[1]}\n{place[2]}")


# Баланс
@dp.callback_query(F.data == 'balance')
async def get_balance(call: CallbackQuery):
    with open('SiteGeoCult/SiteGeoCult/data.json', 'r') as json_file:
        data = json.load(json_file)
        idChat = str(call.message.chat.id)
    if idChat in data:
        balance = data[idChat]['balance']
    else:
        with open('SiteGeoCult/SiteGeoCult/data.json', 'w') as json_file:
            balance = '500'
            data[idChat] = {'balance': '500', 'place': []}
            json.dump(data, json_file)
    await call.message.answer(balance)


def main_kb():
    kb_list = [
        [InlineKeyboardButton(text="Твои места", callback_data='get_place'),
         InlineKeyboardButton(text="Узнать баланс", callback_data='balance')],
        [InlineKeyboardButton(text="Отправится в путешествие", callback_data='random_place'),
         InlineKeyboardButton(text="Узнать баланс", web_app=WebAppInfo(url='https://mass.net.ru'))]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Этот бог поможет \n1. Спланировать путешествие по воронежу "
                         "\n2. Изучить литературные места воронежа "
                         "\n3. Посоревноваться с друзьями в знании литературного Воронежа",
                         reply_markup=main_kb())


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        f = user_data[str(message.chat.id)]
        coordinate = await yandex_map.geocodeAddress(message.text)
        place_x1, place_y1 = coordinate_place(user_data[str(message.chat.id)])
        place_x2, place_y2 = coordinate[:coordinate.find(" ")], coordinate[coordinate.find(" ")+1:]
        dist = math.hypot(float(place_x2) - float(place_x1), float(place_y2) - float(place_y1))
        del user_data[str(message.chat.id)]
        reward = int(1/dist*30)
        with open('SiteGeoCult/SiteGeoCult/data.json', 'r') as json_file:
            data = json.load(json_file)
            data[str(message.chat.id)]['balance'] = str(int(data[str(message.chat.id)]['balance']) + reward)
        with open('SiteGeoCult/SiteGeoCult/data.json', 'w') as json_file:
            json.dump(data, json_file)
        await message.answer(f'Вы получили {reward}')
    except KeyError:
        await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
