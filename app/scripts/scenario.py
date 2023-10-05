from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
import app.aiogram.keyboards as kb
from app.scripts.graphics import getCardPick, getCardPng
from app.db.cards_db import db
from random import randint

# {'status': True, 
# 'emoji': 1, 
# 'name': 'TEST PACK', 
# 'icon': '', 
# 'price': 0, 

# 'events': ['default', 'special'], 
# 'ratings': {'min': 0, 'max': 99}, 
# 'guarantee': {'rating': {}, 'event': {}}, 
# 'chances': {'random_numbers': 1000, "borders": {"bronze": [0,350],"bronze rare": [351,500],"silver": [501,700],"silver rare": [701,850],"gold": [851,940],"gold rare": [941,985],"special": [986,1000]}, 
# 'items': 5}


async def openPack(pack: dict, call : CallbackQuery):
    drop = []
    for i in range(pack['items']):
        num = randint(0, pack['chances']['random_numbers'])
        for g in pack['chances']["borders"].items():
            if num > int(g[1][0]) and num <= int(g[1][1]):
                card = g[0]
                break
        players_list = await db.getPlayersList(pack['events'], pack['ratings'], card)
        if len(players_list) > 1:
            player = players_list[randint(0, len(players_list)-1)]
        else:
            player = players_list[0]
        drop.append(list(player))
    drop.sort(key = lambda x: x[2])
    drop.reverse()
    card_file = getCardPng(team=drop[0][0], name=drop[0][1],rating=drop[0][2],card=drop[0][3],nation=drop[0][4], avatar=drop[0][5])
    for k in range(len(drop)):
        if "\r\n" in drop[k-1][1]:
            drop[k-1][1]= drop[k-1][1].replace("\r\n", "")
    file = getCardPick(card_file)
    drop_str = "\n".join((f"{x[1]} | {x[2]}" for x in drop[1:]))
    print("="*20)
    print(f"Open {pack['name']}\n@{call.from_user.username} ({call.from_user.id}):\n{drop[0][1]} | {drop[0][2]}\n{drop_str}")
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile(file),has_spoiler=True, caption=f"⬆️Вам выпал⬆️\n\nОстальной дроп:\n{drop_str}"),reply_markup=kb.pack_menu)