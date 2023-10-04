from aiogram.types import CallbackQuery
from app.db.cards_db import db
from random import randint
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика для logger
packs_handler = logging.FileHandler(f"logs/{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
packs_handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(packs_handler)

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
    try:
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
            drop.append(player)
        drop_str = ""
        for j in drop:
            drop_str += f"{j[1]} | {j[2]}\n"
        await call.answer(text="Вам выпали:\n"+drop_str+"\nЭто тестовый вариант выпадения игроков!\nВ финальной версии игроки будут отображаться в виде фотографии карточки:3",show_alert=True)
        logger.info(f"\n@{call.from_user.username} ({call.from_user.id})\n{'='*10}\n{drop_str}Pack: {pack['name']}")
    except:
        logger.error("Error", exc_info=True)
    