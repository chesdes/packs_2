from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Filter, Command, CommandStart
from app.aiogram.lexicon import TEXTS, EMOJI_PACKS
import app.aiogram.keyboards as kb 
from app.scripts.utils import getPacks, getPack

router = Router()

class ItsPack(Filter):
    async def __call__(self, call: CallbackQuery):
        packs = getPacks()
        for i in packs:
            if call.data == i['name']:
                return True
        return False

@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer_photo(caption=TEXTS["welcome"], reply_markup=kb.start_menu, photo=FSInputFile("img\other\packs logo.png"))

@router.callback_query(F.data == "start_menu")
async def start_menu_call_handler(call: CallbackQuery):
    await call.message.edit_caption(caption=TEXTS["welcome"],reply_markup=kb.start_menu)

@router.callback_query(F.data == "menu")
async def menu_call_handler(call: CallbackQuery):
    await call.message.edit_caption(caption=TEXTS["menu"],reply_markup=kb.main_menu)
    
@router.callback_query(F.data == "packs")
async def packs_menu_call_handler(call: CallbackQuery):
    await call.message.edit_caption(caption=TEXTS["packs"],reply_markup=kb.packs_menu())

@router.callback_query(ItsPack())
async def pack_menu(call: CallbackQuery):
    pack = getPack(call.data)
    await call.message.edit_caption(caption=f"Пак: {EMOJI_PACKS[pack['emoji']]}{pack['name']}\nЦена: {pack['price']}\n\nВыберите действие из списка:",
                                    reply_markup=kb.pack_menu
                                    )

#other
@router.callback_query()
async def other_calls_handler(call: CallbackQuery):
    await call.answer(text="Скоро...", show_alert=True)

@router.message()
async def other_handler(msg: Message):
    await msg.delete()