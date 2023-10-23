from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, UserProfilePhotos, InputFile
from aiogram.filters import Filter, Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.aiogram.lexicon import TEXTS, EMOJI_PACKS, PACKS_DESC
import app.aiogram.keyboards as kb
from app.scripts.utils import *
from app.scripts.scenario import *
from app.db.main_db import main_db
import colorama
import datetime

colorama.init(autoreset=True)

router = Router()

class Wait(StatesGroup):
    shop_pack_menu = State()
    inventory_pack_menu = State()
    inventory_players_menu = State()
    inventory_gifts_menu = State()
    
class ItsPage(Filter):
    async def __call__(self, call: CallbackQuery):
        if call.data[:5] == "page_":
            return True
        return False
    
class ItsPlayerNumber(Filter):
    async def __call__(self, call: CallbackQuery):
        if call.data[:3] == "pl_":
            return True
        return False
    
class ItsGiftNumber(Filter):
    async def __call__(self, call: CallbackQuery):
        if call.data[:3] == "gf_":
            return True
        return False

class ItsGetPng(Filter):
    async def __call__(self, call: CallbackQuery):
        if call.data[:8] == "get_png_":
            return True
        return False

class ItsPack(Filter):
    async def __call__(self, call: CallbackQuery):
        packs = getPacks()
        for i in packs:
            if call.data == i['name']:
                return True
        return False

class InDB(Filter):
    async def __call__(self, call: CallbackQuery):
        if await main_db.getUser(call.from_user.id) != None:
            return True
        else:
            return False

class ItsAdmin(Filter):
    async def __call__(self, call: CallbackQuery):
        user = await main_db.getUser(call.from_user.id)
        if user[-1] == 1:
            return True
        else:
            return False

@router.message(InDB(), CommandStart())
async def start_handler(msg: Message):
    await msg.answer_photo(caption=TEXTS["welcome"], parse_mode='html', reply_markup=kb.start_menu, photo=FSInputFile("img\other\packs logo.png"))

@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer_photo(caption=TEXTS["welcome"], parse_mode='html', reply_markup=kb.start_menu, photo=FSInputFile("img\other\packs logo.png"))
    await main_db.addUser(msg.from_user.id)

@router.message(InDB(), ItsAdmin(), Command("gift"))
async def gift_command(msg: Message):
    msgArray = msg.text.split(" ")[1:]
    try:
        if msgArray[0] == "all":
            list = await main_db.getUsersAuthsList()
            for i in list:
                to_user_auth = int(i)
                to_user = await main_db.getUser(to_user_auth)
                pack = getPack(" ".join(msgArray[1:]))
                if pack != None:
                    to_user[6].append(pack['name'])
                    await main_db.setGifts(to_user_auth, to_user[6])
                else:
                    await msg.answer(text="Такого пака не существует")
                    return
            await msg.answer(text=f'Подарок "{pack["name"]}" был отправлен всем')
        else:
            to_user_auth = int(msgArray[0])
            to_user = await main_db.getUser(to_user_auth)
            if to_user != None:
                pack = getPack(" ".join(msgArray[1:]))
                if pack != None:
                    to_user[6].append(pack['name'])
                    await main_db.setGifts(to_user_auth, to_user[6])
                    await msg.answer(text=f'Подарок "{pack["name"]}" был отправлен пользователю: {to_user_auth}')
                else:
                    await msg.answer(text="Такого пака не существует")
            else:
                await msg.answer(text="Пользователя с таким айди нету")
    except IndexError:
        await msg.answer(text="Недостаток аргументов")
    
    
@router.callback_query(InDB(), F.data == "sell_all", Wait.inventory_players_menu)
async def page_players_menu(call: CallbackQuery):
    user = await main_db.getUser(call.from_user.id)
    price_sum = sum([x[6] for x in user[4]])
    await main_db.setBalance(call.from_user.id,user[2]+price_sum)
    await main_db.setInventory(call.from_user.id,[])
    user_profile_photo: UserProfilePhotos = await call.from_user.get_profile_photos()
    await call.message.edit_media(media=InputMediaPhoto(media=user_profile_photo.photos[0][0].file_id,
                                                        caption=getProfileStr(call, user),
                                                        parse_mode='html'),
                                  reply_markup=await kb.inventory_menu(call))
    await call.answer(text=f"Вы продали всех игроков!\n\nВаш баланс:\n{user[2]} ➡️ {user[2]+price_sum} (+{price_sum})", show_alert=True)
    print("="*20)
    print(f"\033[33m{datetime.datetime.now()}")
    print(f"\033[32mSell {len(user[4])} players\n\033[35m{call.from_user.full_name} - @{call.from_user.username} ({call.from_user.id}):\n\033[36mBalance: {user[2]} -> {user[2]+price_sum} (+{price_sum})")

@router.callback_query(InDB(), ItsPlayerNumber(), Wait.inventory_players_menu)
async def page_players_menu(call: CallbackQuery):
    await inventoryPackMenu(call.data[3:],call)
    
@router.callback_query(InDB(), ItsGiftNumber(), Wait.inventory_gifts_menu)
async def gift_menu(call: CallbackQuery):
    num = int(call.data[3:])
    user = await main_db.getUser(call.from_user.id)
    gift = user[6][num]
    if len(user[5]) < user[7]:
        user[5].append(gift)
        user[6].remove(gift)
        await main_db.setPacks(call.from_user.id,user[5])
        await main_db.setGifts(call.from_user.id,user[6])
        await call.answer(text=f'Подарок "{gift}" был добавлен в инвентарь', show_alert=True)
        await call.message.edit_reply_markup(reply_markup=await kb.inventory_gifts_menu(call))
    else:
        await call.answer(text=f'В инвентаре не хватает места для подарка', show_alert=True)

@router.callback_query(InDB(), ItsGetPng(), Wait.inventory_players_menu)
async def page_players_menu(call: CallbackQuery):
    user = await main_db.getUser(call.from_user.id)
    user[4].sort(key = lambda x: x[2])
    user[4].reverse()
    card = user[4][int(call.data[8:])-1]
    png = await getCardPng(user_id=call.from_user.id, team=card[0], name=card[1], rating=card[2], card=card[3], nation=card[4], avatar=card[5])
    await call.message.answer_document(document=FSInputFile(png))
    await call.answer(text="Пнг карты придёт отдельным сообщением ниже...")

@router.callback_query(InDB(), ItsPage(), Wait.inventory_players_menu)
async def page_players_menu(call: CallbackQuery):
    await call.message.edit_caption(caption=await getInventoryPlayersStr(call, int(call.data[5:])), 
                                                        parse_mode='html',
                                  reply_markup=await kb.inventory_players_menu(call, int(call.data[5:])))

@router.callback_query(InDB(), F.data == "start_menu")
async def start_menu_call_handler(call: CallbackQuery):
    await call.message.edit_caption(caption=TEXTS["welcome"], parse_mode='html', reply_markup=kb.start_menu)

@router.callback_query(InDB(), F.data == "menu")
async def menu_call_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile("img\other\packs logo.png"),caption=TEXTS["menu"], parse_mode='html'),reply_markup=kb.main_menu)
    
@router.callback_query(InDB(), F.data == "shop_packs")
async def packs_menu_call_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(Wait.shop_pack_menu)
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile("img/backgrounds/main.png"),caption=TEXTS["shop_packs"], parse_mode='html'),reply_markup=kb.shop_packs_menu())

@router.callback_query(InDB(), F.data == "inventory")
async def inventory_menu_call_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user = await main_db.getUser(call.from_user.id)
    user_profile_photo: UserProfilePhotos = await call.from_user.get_profile_photos()
    await call.message.edit_media(media=InputMediaPhoto(media=user_profile_photo.photos[0][0].file_id,
                                                        caption=getProfileStr(call, user),
                                                        parse_mode='html'),
                                  reply_markup=await kb.inventory_menu(call))

@router.callback_query(InDB(), F.data == "inventory_players")
async def inventory_players_call_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(Wait.inventory_players_menu)
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile("img/backgrounds/main.png"),caption=await getInventoryPlayersStr(call, 0), parse_mode='html'),reply_markup=await kb.inventory_players_menu(call, 0))

@router.callback_query(InDB(), F.data == "inventory_packs")
async def inventory_packs_menu_call_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(Wait.inventory_pack_menu)
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile("img/backgrounds/main.png"),caption=TEXTS["inventory_packs"], parse_mode='html'),reply_markup=await kb.inventory_packs_menu(call))

@router.callback_query(InDB(), F.data == "inventory_gifts")
async def inventory_gifts_call_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(Wait.inventory_gifts_menu)
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile("img/backgrounds/main.png"), caption=TEXTS["inventory_gifts"], parse_mode='html'), reply_markup=await kb.inventory_gifts_menu(call))

@router.callback_query(InDB(), F.data == "open", Wait.inventory_pack_menu)
async def open_pack(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        await openPack(data['pack'],call)
        await state.clear()
    except KeyError: 
        await call.answer(text="Ошибка:\n\nВернитесь в инвентарь и попробуйте снова!", show_alert=True)

@router.callback_query(InDB(), F.data == "buy", Wait.shop_pack_menu)
async def buy_pack(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        user = await main_db.getUser(call.from_user.id)
        if user[2] >= data["pack"]['price'] and len(user[5]) < user[7]:
            await call.message.edit_caption(caption=f"Подтвердите покупку:\n\n<b>{EMOJI_PACKS[data['pack']['emoji']]}{data['pack']['name']} <u>{data['items']}шт</u></b>\n\n<b>Стоимость:</b> {data['pack']['price']*data['items']}\n<b>Ваш баланс после покупки:</b> {user[2]} ➡️ {user[2]-data['pack']['price']*data['items']}",
                                            parse_mode="html",
                                            reply_markup=kb.shop_buy_confirm(data, user))
        elif user[2] < data["pack"]['price']*data["items"]:
            await call.answer(text=f"Вам не хватает {data['pack']['price'] - user[2]} монет чтобы купить пак",show_alert=True)
        else:
            await call.answer(text=f"У вас макс. кол-во паков в инвентаре",show_alert=True)
    except KeyError: 
        await call.answer(text="Ошибка:\n\nВернитесь в меню паков и попробуйте снова!", show_alert=True)

@router.callback_query(InDB(), F.data == "plus", Wait.shop_pack_menu)
async def plus_pack(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["items"] += 1
    user = await main_db.getUser(call.from_user.id)
    await call.message.edit_caption(caption=f"Подтвердите покупку:\n\n<b>{EMOJI_PACKS[data['pack']['emoji']]}{data['pack']['name']} <u>{data['items']}шт</u></b>\n\n<b>Стоимость:</b> {data['pack']['price']*data['items']}\n<b>Ваш баланс после покупки:</b> {user[2]} ➡️ {user[2]-data['pack']['price']*data['items']}",
                                            parse_mode="html",
                                            reply_markup=kb.shop_buy_confirm(data, user))
    await state.update_data(items=data["items"])

@router.callback_query(InDB(), F.data == "minus", Wait.shop_pack_menu)
async def plus_pack(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["items"] -= 1
    user = await main_db.getUser(call.from_user.id)
    await call.message.edit_caption(caption=f"Подтвердите покупку:\n\n<b>{EMOJI_PACKS[data['pack']['emoji']]}{data['pack']['name']} <u>{data['items']}шт</u></b>\n\n<b>Стоимость:</b> {data['pack']['price']*data['items']}\n<b>Ваш баланс после покупки:</b> {user[2]} ➡️ {user[2]-data['pack']['price']*data['items']}",
                                            parse_mode="html",
                                            reply_markup=kb.shop_buy_confirm(data, user))
    await state.update_data(items=data["items"])

@router.callback_query(InDB(), F.data == "buy")
async def buy_pack(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь в магазин и попробуйте снова!", show_alert=True)

@router.callback_query(InDB(), F.data == "open")
async def buy_pack(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь в инвентарь и попробуйте снова!", show_alert=True)
    
@router.callback_query(InDB(), F.data == "buy_confirm")
async def buy_confirm_pack(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        await buyPack(data['pack'], call, data['items'])
    except KeyError: 
        await call.answer(text="Ошибка:\n\nВернитесь в меню паков и попробуйте снова!", show_alert=True)

@router.callback_query(InDB(), ItsPack(), Wait.shop_pack_menu)
async def shop_packs_menu(call: CallbackQuery, state: FSMContext):
    pack = getPack(call.data)
    pack_pic = f"{pack['prev']}"
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pack_pic),
                                                        caption=f"Пак: {EMOJI_PACKS[pack['emoji']]}{pack['name']}\nЦена: {pack['price']}\n\n<b>Описание:</b>\n{PACKS_DESC[pack['emoji']]}\n\nВыберите действие из списка:", 
                                                        parse_mode='html'),
                                  reply_markup=kb.shop_pack_menu)
    await state.update_data(pack=pack)
    await state.update_data(items=1)

@router.callback_query(InDB(), ItsPack(), Wait.inventory_pack_menu)
async def shop_packs_menu(call: CallbackQuery, state: FSMContext):
    pack = getPack(call.data)
    pack_pic = f"{pack['prev']}"
    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pack_pic),
                                                        caption=f"Пак: {EMOJI_PACKS[pack['emoji']]}{pack['name']}\n\n<b>Описание:</b>\n{PACKS_DESC[pack['emoji']]}\n\nВыберите действие из списка:", 
                                                        parse_mode='html'),
                                  reply_markup=kb.inventory_pack_menu)
    await state.update_data(pack=pack)

#errors
@router.callback_query(InDB(), F.data == "sell_all")
async def ya_yzhe_nastolko_zaebalsya_nazivat_hendlers_chto_idite_nahyi_smotrite_odinakovie_nazvania(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь в инвентарь и попробуйте снова!", show_alert=True)

@router.callback_query(InDB(), F.data == "plus")
async def ya_yzhe_nastolko_zaebalsya_nazivat_hendlers_chto_idite_nahyi_smotrite_odinakovie_nazvania(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь в магазин и попробуйте снова!", show_alert=True)
    
@router.callback_query(InDB(), F.data == "minus")
async def ya_yzhe_nastolko_zaebalsya_nazivat_hendlers_chto_idite_nahyi_smotrite_odinakovie_nazvania(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь в магазин и попробуйте снова!", show_alert=True)

@router.callback_query(InDB(), ItsPack())
async def error_packs_menu(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь назад и попробуйте снова!", show_alert=True)

@router.callback_query(InDB(), ItsGetPng())
async def page_players_menu(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь в инвентарь и попробуйте снова!", show_alert=True)

@router.callback_query(InDB(), ItsPage())
async def error_packs_menu(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь в инвентарь и попробуйте снова!", show_alert=True)

@router.callback_query(InDB(), ItsGiftNumber())
async def error_gift_menu(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь в инвентарь и попробуйте снова!", show_alert=True)
    
@router.callback_query(InDB(), ItsPlayerNumber())
async def error_players_menu(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВернитесь в инвентарь и попробуйте снова!", show_alert=True)

#other
@router.callback_query(InDB())
async def other_calls_handler(call: CallbackQuery):
    await call.answer(text="Скоро...", show_alert=True)

@router.callback_query()
async def other_calls_handler(call: CallbackQuery):
    await call.answer(text="Ошибка:\n\nВас не нашли в базе данных...\nНапишите /start чтобы зарегистрироваться", show_alert=True)

@router.message()
async def other_handler(msg: Message):
    await msg.delete()