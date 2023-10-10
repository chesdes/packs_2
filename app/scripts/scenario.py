from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
import app.aiogram.keyboards as kb
from app.scripts.graphics import getCardPick, getCardPng
from app.db.cards_db import cards_db
from app.db.main_db import main_db
from random import randint
from app.aiogram.lexicon import *
import datetime
import colorama

colorama.init(autoreset=True)

async def inventoryPackMenu(num: str, call: CallbackQuery):
    num = int(num)
    user = await main_db.getUser(call.from_user.id)
    user[4].sort(key = lambda x: x[2])
    user[4].reverse()
    card = user[4][num-1]
    png_file = await getCardPng(user_id=call.from_user.id,team=card[0], name=card[1],rating=card[2],card=card[3],nation=card[4], avatar=card[5])
    file = await getCardPick(png_file, call.from_user.id)
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile(file)),reply_markup=kb.player_inventory(num))
    

async def buyPack(pack: dict, call: CallbackQuery):
    user = await main_db.getUser(call.from_user.id)
    if user[2] >= pack['price'] and len(user[5]) < 25:
        await main_db.setBalance(call.from_user.id, user[2]-pack['price'])
        user[5].append(pack)
        await main_db.setPacks(call.from_user.id, user[5])
        print("="*20)
        print(f"\033[33m{datetime.datetime.now()}")
        print(f"\033[32mBuy {pack['name']}\n\033[35m{call.from_user.full_name} - @{call.from_user.username} ({call.from_user.id}):\n\033[36mBalance: {user[2]} -> {user[2]-pack['price']}\nPacks: {len(user[5])}")
        await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile("img/backgrounds/main.png"),caption=TEXTS["shop_packs"], parse_mode='html'),reply_markup=kb.shop_packs_menu())
    elif user[2] < pack['price']:
        await call.answer(text=f"Вам не хватает {pack['price'] - user[2]} монет чтобы купить пак",show_alert=True)
    else:
        await call.answer(text=f"У вас максимальное кол-во паков в инвентаре",show_alert=True)

async def openPack(pack: dict, call : CallbackQuery):
    user = await main_db.getUser(call.from_user.id)
    if len(user[4])+pack["items"] <= 200:
        await main_db.openPack(call.from_user.id)
        user[5].remove(pack)
        await main_db.setPacks(call.from_user.id, user[5])
        drop = []
        for i in range(pack['items']):
            num = randint(0, pack['chances']['random_numbers'])
            for g in pack['chances']["borders"].items():
                if num > int(g[1][0]) and num <= int(g[1][1]):
                    card = g[0]
                    break
            players_list = await cards_db.getPlayersList(pack['events'], pack['ratings'], card)
            if len(players_list) > 1:
                player = players_list[randint(0, len(players_list)-1)]
            else:
                player = players_list[0]
            drop.append(list(player))
        drop.sort(key = lambda x: x[2])
        drop.reverse()
        for j in drop:  
            user[4].append(j)
        await main_db.setInventory(call.from_user.id,user[4])
        card_file = await getCardPng(user_id=call.from_user.id,team=drop[0][0], name=drop[0][1],rating=drop[0][2],card=drop[0][3],nation=drop[0][4], avatar=drop[0][5])
        for k in range(len(drop)):
            if "\r\n" in drop[k-1][1]:
                drop[k-1][1]= drop[k-1][1].replace("\r\n", "")
        file = await getCardPick(card=card_file, user_id=call.from_user.id)
        logs_drop_str = "\n".join((f"{x[1]} [{x[2]}] ({x[3]})" for x in drop[1:]))
        drop_str = "\n".join((f"<b>{x[1]}</b> [{x[2]}] ({x[3]})" for x in drop[1:]))
        print("="*20)
        print(f"\033[33m{datetime.datetime.now()}")
        print(f"\033[32mOpen {pack['name']}\n\033[35m{call.from_user.full_name} - @{call.from_user.username} ({call.from_user.id}):\n\033[36m{drop[0][1]} [{drop[0][2]}] ({drop[0][3]})\n{logs_drop_str}\nPlayers: {len(user[4])}")
        await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile(file),
                                                            has_spoiler=True, 
                                                            caption=f"⬆️<b>Вам выпал</b>⬆️\n\nОстальной дроп:\n{drop_str}", 
                                                            parse_mode='html'),
                                      reply_markup=kb.pack_get_drop)
    else:
        await call.answer(text="Вам не хватает места для игроков в инвентаре", show_alert=True)