import asyncio
import logging
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram import Bot, Dispatcher, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8185175071:AAFCjW-WvT1cZ8wBlJ5IYcr8QuBieW3xC2A")
dp = Dispatcher()


def main_kb():
    kb_list = [
        [
            InlineKeyboardButton(text="Узнать баланс",
                                 web_app=WebAppInfo(url='https://mass.net.ru')
                                 )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Этот бог поможет \n1. Спланировать путешествие по воронежу "
                         "\n2. Изучить литературные места воронежа "
                         "\n3. Посоревноваться с друзьями в знании литературного Воронежа",
                         reply_markup=main_kb())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
