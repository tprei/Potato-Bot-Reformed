import aiosqlite
import asyncio
import os.path

class GoldDatabaseHandler:
    def __init__(self, name):
        self.database_name = name
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.startup())

    async def startup(self):
        if not os.path.isfile(self.database_name):
            with open(self.database_name, 'w'): pass
            async with aiosqlite.connect(self.database_name) as db:
                await db.execute("""CREATE TABLE Gold (
                        original_id INTEGER NOT NULL,
                        embed_id INTEGER NOT NULL,
                        CONSTRAINT Gold_PK PRIMARY KEY (original_id));""")
                await db.commit()


    async def lookup(self, msg_id):
        async with aiosqlite.connect(self.database_name) as db:
            params = (msg_id,)
            async with db.execute("""
                        SELECT *
                        FROM Gold 
                        WHERE original_id=?""", params) as cursor:
                row = await cursor.fetchone()

                if row is not None:
                    return row[1]
                
                return row
    
    async def insert(self, msg_id, msg_embed):
        async with aiosqlite.connect(self.database_name) as db:
            await db.execute("INSERT INTO Gold VALUES (?, ?)", (msg_id, msg_embed))
            await db.commit()
    
    async def insert_many(self, bindings):
        async with aiosqlite.connect(self.database_name) as db:
            await db.executemany("INSERT INTO Gold VALUES (?, ?)", bindings)
            await db.commit()
