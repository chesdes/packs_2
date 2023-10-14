from aiogram.types import InlineKeyboardButton as InBt, InlineKeyboardMarkup as InMp, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.aiogram.lexicon import EMOJI_PACKS
from app.scripts.utils import getPacks, getPack
from app.db.main_db import main_db
import json

start_menu = InMp(inline_keyboard=[
    [InBt(text="💬Канал разработчика", url="https://t.me/chesdesq")],
    [InBt(text="🧿Дискорд сервер", url="https://discord.gg/RTX9ZAVh7S")],
    [InBt(text="🗂Меню",callback_data="menu")]
])

main_menu = InMp(inline_keyboard=[
    [InBt(text="⬅️Назад", callback_data="start_menu")],
    [InBt(text="🗄Инвентарь", callback_data="inventory"),
    InBt(text="📦Магазин паков",callback_data="shop_packs")]
])

inventory_menu = InMp(inline_keyboard=[
    [InBt(text="⬅️Назад", callback_data="menu")],
    [InBt(text="🎰Паки", callback_data="inventory_packs"),
    InBt(text="🏋🏻‍♂️Игроки", callback_data="inventory_players")]
])

def player_inventory(num: int):
    return  InMp(inline_keyboard=[
        [InBt(text="⬅️Назад", callback_data="inventory_players")],
        [InBt(text="Пнг карты", callback_data=f"get_png_{num}")]
    ])

async def inventory_players_menu(call: CallbackQuery, page: int):
    user = await main_db.getUser(call.from_user.id)
    if len(user[4]) != 0:
        builder = InlineKeyboardBuilder()
        row = []
        builder.button(text="⬅️Назад", callback_data="inventory")
        row.append(1)
        for g in range(page*10+1, page*10+len(user[4][page*10:page*10+10])+1):
            builder.button(text=f"{g}", callback_data=f"pl_{g}")
            if g % 5 == 0:
                row.append(5)
            elif g == page*10+len(user[4][page*10:page*10+10]):
                row.append(g-5-page*10)
        if page == 0 and len(user[4]) > 10:
            builder.button(text=f"Вперёд", callback_data=f"page_{page+1}")
            row.append(1)
        elif len(user[4]) <= 10:
            pass
        elif page * 10 + 10 < len(user[4]): 
            builder.button(text=f"Назад", callback_data=f"page_{page-1}")
            builder.button(text=f"Вперёд", callback_data=f"page_{page+1}")
            row.append(2)
        else:
            builder.button(text=f"Назад", callback_data=f"page_{page-1}")
            row.append(1)
        builder.button(text=f"Продать всех", callback_data=f"sell_all")
        row.append(1)
        builder.adjust(*row)
        return builder.as_markup()
    else:
        return InMp(inline_keyboard=[
            [InBt(text="⬅️Назад", callback_data="inventory")]
        ])

async def inventory_packs_menu(call: CallbackQuery):
    user = await main_db.getUser(call.from_user.id)
    builder = InlineKeyboardBuilder()
    row = []
    builder.button(text="⬅️Назад", callback_data="inventory")
    row.append(1)
    for g in user[5]:
        pack = getPack(g)
        builder.button(text=f"{EMOJI_PACKS[pack['emoji']]}{pack['name']}", callback_data=f"{pack['name']}")
    row.append(2)
    builder.adjust(*row)
    return builder.as_markup()

def shop_packs_menu():
    packs = getPacks()
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️Назад", callback_data="menu")
    for g in packs:
        builder.button(text=f"{EMOJI_PACKS[g['emoji']]}{g['name']}", callback_data=f"{g['name']}")
    builder.adjust(1)
    return builder.as_markup()

inventory_pack_menu = InMp(inline_keyboard=[
    [InBt(text="⬅️Назад", callback_data="inventory_packs")],
    [InBt(text="📤Открыть", callback_data="open")]
])

shop_buy_confirm = InMp(inline_keyboard=[
    [InBt(text="⛔️Отмена", callback_data="shop_packs")],
    [InBt(text="✅Подтвердить", callback_data="buy_confirm")]
])

pack_get_drop = InMp(inline_keyboard=[
    [InBt(text="⬅️Паки", callback_data="inventory_packs")]
])

inventory_players = InMp(inline_keyboard=[
    [InBt(text="⬅️Назад", callback_data="inventory")],
    [InBt(text="Продать всех", callback_data="buy_all_players")]
])

shop_pack_menu = InMp(inline_keyboard=[
    [InBt(text="⬅️Назад", callback_data="shop_packs")],
    [InBt(text="💸Купить", callback_data="buy")]
])