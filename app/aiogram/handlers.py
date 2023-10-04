from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Filter, Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.aiogram.lexicon import TEXTS, EMOJI_PACKS
import app.aiogram.keyboards as kb
from app.scripts.utils import getPacks, getPack
from app.scripts.scenario import openPack
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# настройка обработчика и форматировщика для logger
log_handler = logging.FileHandler(f"logs/{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
log_handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(log_handler)

router = Router()

class Wait(StatesGroup):
    pack_menu = State()

class ItsPack(Filter):
    async def __call__(self, call: CallbackQuery):
        packs = getPacks()
        for i in packs:
            if call.data == i['name']:
                return True
        return False

@router.message(CommandStart())
async def start_handler(msg: Message):
    logger.debug(f"/start command: {msg.from_user.username} ({msg.from_user.id})")
    await msg.answer_photo(caption=TEXTS["welcome"], reply_markup=kb.start_menu, photo=FSInputFile("img\other\packs logo.png"))

@router.callback_query(F.data == "start_menu")
async def start_menu_call_handler(call: CallbackQuery):
    logger.debug(f"Start menu: {call.from_user.username} ({call.from_user.id})")
    await call.message.edit_caption(caption=TEXTS["welcome"],reply_markup=kb.start_menu)

@router.callback_query(F.data == "menu")
async def menu_call_handler(call: CallbackQuery):
    logger.debug(f"Main menu: {call.from_user.username} ({call.from_user.id})")
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile("img\other\packs logo.png"),caption=TEXTS["menu"]),reply_markup=kb.main_menu)
    
@router.callback_query(F.data == "packs")
async def packs_menu_call_handler(call: CallbackQuery, state: FSMContext):
    logger.debug(f"Packs menu: {call.from_user.username} ({call.from_user.id})")
    await state.clear()
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile("img/backgrounds/main.png"),caption=TEXTS["packs"]),reply_markup=kb.packs_menu())

@router.callback_query(F.data == "open")
async def open_pack(call: CallbackQuery, state: FSMContext):
    logger.debug(f"Open pack: {call.from_user.username} ({call.from_user.id})")
    data = await state.get_data()
    try:
        await openPack(data['pack'], call=call)
    except KeyError: 
        await call.answer(text="Ошибка!\n\nВернитесь в меню паков и попробуйте снова!", show_alert=True)
        
@router.callback_query(ItsPack())
async def pack_menu(call: CallbackQuery, state: FSMContext):
    logger.debug(f"Pack menu: {call.from_user.username} ({call.from_user.id})")
    pack = getPack(call.data)
    pack_pic = f"{pack['prev']}"
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pack_pic),
                                                        caption=f"Пак: {EMOJI_PACKS[pack['emoji']]}{pack['name']}\nЦена: {pack['price']}\n\nВыберите действие из списка:"),
                                  reply_markup=kb.pack_menu)
    await state.set_state(Wait.pack_menu)
    await state.update_data(pack=pack)

#other
@router.callback_query()
async def other_calls_handler(call: CallbackQuery):
    await call.answer(text="Скоро...", show_alert=True)

@router.message()
async def other_handler(msg: Message):
    logger.debug(f"Other Messages\n{msg.from_user.username} ({msg.from_user.id}) : {msg.text}")
    await msg.delete()