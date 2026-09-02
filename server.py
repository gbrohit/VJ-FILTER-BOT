import asyncio
import logging
import os
import aiohttp
from aiohttp import web

# Default to 8080 if PORT isn't set in Koyeb
PORT = int(os.environ.get("PORT", 8080))
# URL to ping. Use Koyeb's public URL if provided, otherwise ping localhost
PING_URL = os.environ.get("URL", f"http://0.0.0.0:{PORT}")

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({"status": "Bot is running perfectly!"})

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def ping_server():
    """Background task to ping the web server every 5 minutes."""
    await asyncio.sleep(10)
    while True:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(PING_URL) as resp:
                    logging.info(f"Keep-Alive Ping Successful: {resp.status}")
        except Exception as e:
            logging.error(f"Keep-Alive Ping Failed: {e}")
        # Wait 5 minutes before pinging again
        await asyncio.sleep(300)