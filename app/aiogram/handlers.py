from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command
from app.aiogram.texts import TEXT

router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(text=TEXT["welcome"])