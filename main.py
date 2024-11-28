import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8185175071:AAFCjW-WvT1cZ8wBlJ5IYcr8QuBieW3xC2A")

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@dp.message()
async def echo_handler(message) -> None:

    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())