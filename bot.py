# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import datetime
import logging
import sys
import os
import asyncio
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.users_chats_db import db
from info import *
from utils import temp
from aiohttp import web
from server import web_server, ping_server

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="TechVJBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        # Start the web server
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        port = int(os.environ.get("PORT", 8080))
        await web.TCPSite(app, bind_address, port).start()
        
        # Start the continuous ping loop
        asyncio.create_task(ping_server())

        await super().start()
        self.set_parse_mode(enums.ParseMode.HTML)
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = "@" + me.username
        
        logging.info(f"{me.first_name} with Pyrogram v{__version__} Started successfully!")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")

app = Bot()
app.run()
