import logging
import os
import asyncio
from pyrogram import Client, __version__, enums
from database.users_chats_db import db
from info import *
from utils import temp
from Script import script
from aiohttp import web

# Lightweight health server to satisfy PaaS port binding (Koyeb/Render)
async def health_check(request):
    return web.Response(text="Bot is running smoothly!", status=200)

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
        # Display logo from script.py
        if hasattr(script, 'LOGO'):
            print(script.LOGO)

        # Start the minimal web server
        app = web.Application()
        app.router.add_get('/', health_check)
        app.router.add_get('/health', health_check)
        
        runner = web.AppRunner(app)
        await runner.setup()
        bind_address = "0.0.0.0"
        port = int(os.environ.get("PORT", 8080))
        await web.TCPSite(runner, bind_address, port).start()
        logging.info(f"Health server started on port {port}")

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
