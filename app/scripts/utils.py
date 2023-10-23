import json
from aiogram.types import CallbackQuery
from app.db.main_db import main_db
from app.aiogram.lexicon import TEXTS

def getPacks():
    with open("app/jsons/packs.json") as i:
        data = json.load(i)
    packs = []
    for j in data.values():
        if j["status"] == True:
            packs.append(j)
    return packs

def getPack(pack: str):
    try:
        with open("app/jsons/packs.json") as i:
            data = json.load(i)
        return data[f"{pack.lower()}"]
    except KeyError:
        return None

async def getInventoryPlayersStr(call: CallbackQuery, page: int):
    user = await main_db.getUser(call.from_user.id)
    user[4].sort(key = lambda x: x[2])
    user[4].reverse()
    players = user[4][page*10:page*10+10]
    for k in range(len(players)):
            if "\r\n" in players[k-1][1]:
                players[k-1][1]= players[k-1][1].replace("\r\n", "")
    result_str = "\n".join((f"{page*10+x+1}) <b>{players[x][1]}</b> [{players[x][2]}] ({players[x][3]}) - <b>{players[x][6]}$</b>" for x in range(len(players[0:]))))
    if len(user[4]) == 0:
        return f"{TEXTS['inventory_players']}\n\nПусто"
    elif len(user[4]) >= 100:
        return f"{TEXTS['inventory_players']}\n\nСтраница {page+1}/{int(str(len(user[4]))[:2])}\n\n{result_str}"
    elif len(user[4]) > 10 and len(user[4]) % 10 == 0:
        return f"{TEXTS['inventory_players']}\n\nСтраница {page+1}/{int(str(len(user[4]))[0])}\n\n{result_str}"
    elif len(user[4]) > 10:
        return f"{TEXTS['inventory_players']}\n\nСтраница {page+1}/{int(str(len(user[4]))[0])+1}\n\n{result_str}"
    else:
        return f"{TEXTS['inventory_players']}\n\nСтраница {page+1}/{page+1}\n\n{result_str}"
    
def getProfileStr(call: CallbackQuery, user: list):
    return f"👤<b>Профиль @{call.from_user.username} :</b>\n\n📍<b>id's:</b> {user[0]} / {call.from_user.id} (bot_id / tg_id)\n👤<b>имя:</b> {call.from_user.full_name}\n💳<b>баланс:</b> {user[2]}💸\n📊<b>паков открыто:</b> {user[3]}\n🗂<b>Размеры инвентаря:</b> {user[7]} / {user[8]} (паки/игроки)"
