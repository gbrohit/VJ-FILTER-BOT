# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import motor.motor_asyncio
from info import AUTH_CHANNEL, OTHER_DB_URI, DATABASE_URI

class JoinReqs:
    def __init__(self):
        uri = OTHER_DB_URI or DATABASE_URI
        if uri:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            self.db = self.client["JoinReqs"]
            self.col = self.db[str(AUTH_CHANNEL)]
        else:
            self.client = None

    def isActive(self):
        return True if self.client else not not DATABASE_URI

    async def add_user(self, user_id, first_name, username, date):
        if not self.isActive():
            return
        await self.col.update_one(
            {"user_id": user_id},
            {"$set": {"first_name": first_name, "username": username, "date": date}},
            upsert=True
        )

    async def get_user(self, user_id):
        if not self.isActive():
            return None
        return await self.col.find_one({"user_id": user_id})

    async def get_all_users_count(self):
        if not self.isActive():
            return 0
        return await self.col.count_documents({})

    async def delete_all_users(self):
        if not self.isActive():
            return
        await self.col.drop()
