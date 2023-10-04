import sqlite3 as sq
import datetime

class DB:
    def __init__(self):
        self.conn = sq.connect("app\db\cards.sqlite")
        self.cur = self.conn.cursor()
    
    async def getPlayersList(self, events:list, ratings: list, card: str):
        if len(events) > 1:
            return self.cur.execute("SELECT team, name, rating, card, nation, avatar FROM ratings WHERE event IN {0} AND rating >= {1} AND rating <= {2} AND card = '{3}'".format(tuple(events),ratings[0],ratings[1],card)).fetchall()
        else:
            return self.cur.execute("SELECT team, name, rating, card, nation, avatar FROM ratings WHERE event = '{0}' AND rating >= {1} AND rating <= {2} AND card = '{3}'".format(events[0],ratings[0],ratings[1],card)).fetchall()
        
db = DB()