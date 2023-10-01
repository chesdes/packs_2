import json

def getPacks():
    with open("app/jsons/packs.json") as i:
        data = json.load(i)
    packs = []
    for j in data.values():
        if j["status"] == True:
            packs.append(j)
    return packs

def getPack(pack: str):
    with open("app/jsons/packs.json") as i:
        data = json.load(i)
    return data[pack.lower()]