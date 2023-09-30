# ---------------- Imports ---------------- #
from PIL import Image, ImageDraw, ImageFont
import json
import datetime

# ---------------- Funcs ---------------- #
def getCardPng(rating, nation, team, name, card, avatar = "default"):
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
        date = "-".join(str(datetime.datetime.now()).split('.')[0].split(':'))
        im.save(f"temp/{date}.png", "PNG")
        return f"temp/{date}.png"
