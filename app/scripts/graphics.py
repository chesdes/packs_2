# ---------------- Imports ---------------- #
from PIL import Image, ImageDraw, ImageFont
import json

# ---------------- Funcs ---------------- #
# {'status': True, 
# 'emoji': 1, 
# 'name': 'TEST PACK', 
# 'icon': 'icon', 
# 'price': 0, 
# 'events': ['default', 'special'], 
# 'ratings': {'min': 0, 'max': 99}, 
# 'guarantee': {'rating': {}, 'event': {}}, 
# 'chances': {'random_numbers': 1000, "borders": {"bronze": [0,350],"bronze rare": [351,500],"silver": [501,700],"silver rare": [701,850],"gold": [851,940],"gold rare": [941,985],"special": [986,1000]}, 
# 'items': 5}

def getCardPick(card: str, user_id):
    with Image.open('img/backgrounds/main.png') as im:
        cardPng = Image.open(card)
        cardPng = cardPng.resize((int(cardPng.width/1.4),int(cardPng.height/1.4)))
        im.paste(cardPng, (int(im.width/2)-int(cardPng.width/2), int(im.height/2)-int(cardPng.height/2)), cardPng)
        im.save(f"temp/{user_id}.png", "PNG")
        return f"temp/{user_id}.png"


def getCardPng(rating, nation, team, name, card, user_id, avatar = "default"):
    with open('app/jsons/cards.json') as f:
        cards = json.load(f)
    with Image.open(cards[card]["file"]) as im:
        #init draw
        draw = ImageDraw.Draw(im)
        
        #fonts
        name_font = ImageFont.truetype("fonts/CruyffSans-Bold.otf", size=107)
        rating_font = ImageFont.truetype("fonts/CruyffSansCondensed-Bold.otf", size=229)
        
        #get nation and team png's 
        flag = Image.open(f"img/flags/{nation}.png")
        logo = Image.open(f"img/logo/{team}.png").resize((160,160))
        
        if avatar == "default": 
            i = cards[card]["avatar"]
            ava = Image.open(f"img/avatars/{avatar}_{i}.png").resize((800,800))
            im.paste(ava, (330, 295), ava)
        else: 
            ava = Image.open(f"img/avatars/{avatar}").resize((650,800))
            try:
                im.paste(ava, (440, 295), ava)
            except ValueError:
                im.paste(ava, (440, 295))
        
        #draw
        draw.text(
            (im.width/2, 1195),
            f'{name}',
            align="center",
            spacing=15,
            anchor="ms",
            fill=(cards[card]["color"]),
            font=name_font
        )
        draw.text(
            (283, 511),
            f'{rating}',
            align="center",
            anchor="ms",
            fill=(cards[card]["color"]),
            font=rating_font
        )
        im.paste(flag, (207, 560))
        im.paste(logo, (207, 700), logo)
        
        #save
        im.save(f"temp/{user_id}.png", "PNG")
        return f"temp/{user_id}.png"
