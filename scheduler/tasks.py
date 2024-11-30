from abc import ABC, abstractmethod
from datetime import datetime

from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ChatMemberStatus
from db.sql.models import Users
from db.sql.service import run_sql, AllUsers


class Task(ABC):
    @abstractmethod
    async def task(self):
        raise NotImplementedError


class MonitorUser(Task):

    def __init__(self, bot: Bot, chat_id: int):
        self.bot = bot
        self.chat_id = chat_id

    async def check_expired(self, user: Users):
        if user.expired_date < datetime.now():
            member = await self.bot.get_chat_member(chat_id=self.chat_id, user_id=user.tg_id)
            if member and not (
                    member.status in [ChatMemberStatus.KICKED, ChatMemberStatus.LEFT, ChatMemberStatus.CREATOR]):
                await self.bot.ban_chat_member(self.chat_id, user.tg_id)
                buttons = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text="Buy 10 $ on 1 moth"), KeyboardButton(text="Buy 20 $ on 2 moth")],
                    [KeyboardButton(text="Buy 30 $ on 3 moth")],
                ], resize_keyboard=True, one_time_keyboard=True)
                await self.bot.send_message(user.tg_id, "You banned in our chanel pleas: ",
                                            reply_markup=buttons)
            else:
                print("You are not banned in our chanel pleas")

    async def task(self):
        users: list[Users] = await run_sql(AllUsers())
        print("Users: ", len(users))
        for user in users:
            await self.check_expired(user)
