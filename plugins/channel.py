# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram import Client, filters
from info import REQ_CHANNEL
from database.join_reqs import JoinReqs

join_db = JoinReqs()

@Client.on_chat_join_request(filters.chat(REQ_CHANNEL) if REQ_CHANNEL else None)
async def req_channel_handler(client, message):
    if not join_db.isActive():
        return
    await join_db.add_user(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        username=message.from_user.username,
        date=message.date
    )
