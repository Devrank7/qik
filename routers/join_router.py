import os
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import ChatJoinRequest
from dotenv import load_dotenv

from db.sql.models import Users
from db.sql.service import run_sql, ReadUser

router = Router()
load_dotenv()
CHAT_ID = int(os.environ.get("CHAT_ID"))


def fit_user(user: Users) -> bool:
    return user.expired_date > (datetime.now() + timedelta(minutes=3))


@router.chat_join_request(F.chat.id == CHAT_ID)
async def join_chat_request(join_request: ChatJoinRequest):
    print("Join chat request: {}".format(join_request))
    user: Users = await run_sql(ReadUser(tg_id=join_request.from_user.id))
    if user:
        if fit_user(user):
            await join_request.approve()
            await join_request.answer("Мы одобрили вашу заявку!!")
            return
    await join_request.answer("Мы НЕ одобрили вашу заявку!!")
    await join_request.decline()
