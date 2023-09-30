# ---------------- Imports ---------------- #
from PIL import Image, ImageDraw, ImageFont
import json
import datetime

# ---------------- Funcs ---------------- #
with open('app/jsons/cards.json') as f:
    CARDS = json.load(f)

def getCard(rating, nation, team, name, card, avatar = "default"):
    with Image.open(CARDS[card]["file"]) as im:
        #init draw
        draw = ImageDraw.Draw(im)
        
        #fonts
        name_font = ImageFont.truetype("app/fonts/CruyffSans-Bold.otf", size=107)
        rating_font = ImageFont.truetype("app/fonts/CruyffSansCondensed-Bold.otf", size=229)
        
        #get nation and team png's 
        flag = Image.open(f"app/img/flags/{nation}.png")
        logo = Image.open(f"app/img/logo/{team}.png").resize((160,160))
        
        if avatar == "default": 
            i = CARDS[card]["avatar"]
            ava = Image.open(f"app/img/avatars/{avatar}_{i}.png").resize((800,800))
            im.paste(ava, (330, 295), ava)
        else: 
            ava = Image.open(f"app/img/avatars/{avatar}").resize((650,800))
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
            fill=(CARDS[card]["color"]),
            font=name_font
        )
        draw.text(
            (283, 511),
            f'{rating}',
            align="center",
            anchor="ms",
            fill=(CARDS[card]["color"]),
            font=rating_font
        )
        im.paste(flag, (207, 560))
        im.paste(logo, (207, 700), logo)
        
        #save
        date = "-".join(str(datetime.datetime.now()).split('.')[0].split(':'))
        im.save(f"temp/{date}.png", "PNG")
        return f"temp/{date}.png"
   
getCard(99, "ru", "Tester","yowai","special") # Test