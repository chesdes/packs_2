# ------------ Imports ------------ #
import asyncio
from aiogram import Bot, Dispatcher
from app.aiogram.handlers import router
import json

# ------------ Get Config ------------ #
with open("config.json") as i:
    TOKEN = json.load(i)['TOKEN']


# ------------ Start ------------ #
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print('Start')
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Goodbye!")