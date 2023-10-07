from aiogram.types import InlineKeyboardButton as InBt, InlineKeyboardMarkup as InMp
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.aiogram.lexicon import EMOJI_PACKS
from app.scripts.utils import getPacks

start_menu = InMp(inline_keyboard=[
    [InBt(text="💬Канал разработчика", url="https://t.me/chesdesq")],
    [InBt(text="🧿Дискорд сервер", url="https://discord.gg/RTX9ZAVh7S")],
    [InBt(text="🗂Меню",callback_data="menu")]
])

main_menu = InMp(inline_keyboard=[
    [InBt(text="⬅️Назад", callback_data="start_menu")],
    [InBt(text="📦Паки",callback_data="packs")]
])

def packs_menu():
    packs = getPacks()
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️Назад", callback_data="menu")
    for g in packs:
        builder.button(text=f"{EMOJI_PACKS[g['emoji']]}{g['name']}", callback_data=f"{g['name']}")
    builder.adjust(1)
    return builder.as_markup()

pack_menu = InMp(inline_keyboard=[
    [InBt(text="⬅️Назад", callback_data="packs")],
    [InBt(text="Открыть", callback_data="open")]
])