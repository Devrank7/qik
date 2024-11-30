import os
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, PreCheckoutQuery, \
    ReplyKeyboardRemove
from dotenv import load_dotenv
from aiogram.exceptions import TelegramBadRequest
from db.sql.models import Users
from db.sql.service import run_sql, UpdateUser, ReadUser
from middlewares.middleware import AuthMiddleware

load_dotenv()
router = Router()
router.message.middleware(AuthMiddleware())
PAYMENT_TOKEN = os.environ.get("PAYMENT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))


@router.message(Command("id"))
async def send_payment_message(message: Message):
    await message.answer(
        f"Chat id: {message.reply_to_message.forward_from_chat.id}, {message.reply_to_message.forward_from_chat.description}")


@router.message(Command("pay"))
async def pay_command(message: Message):
    buttons = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Buy 10 $ on 1 moth"), KeyboardButton(text="Buy 20 $ on 2 moth")],
        [KeyboardButton(text="Buy 30 $ on 3 moth")],
    ], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Choose action:", reply_markup=buttons)


@router.message(F.text.startswith("Buy"))
async def buy_command(message: Message):
    price = int(message.text.split()[1])
    price_liable = [LabeledPrice(label="Подписка на 1 месяц", amount=10 * 100)]
    if price == 20:
        price_liable = [LabeledPrice(label="Подписка на 2 месяц", amount=20 * 100)]
    elif price == 30:
        price_liable = [LabeledPrice(label="Подписка на 3 месяц", amount=30 * 100)]
    await message.answer_invoice("Tg chanel",
                                 "Tg chanel",
                                 "subscription_payment",
                                 "USD",
                                 provider_token=PAYMENT_TOKEN,
                                 prices=price_liable)


@router.pre_checkout_query(lambda query: True)
async def checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def pay_success_payment(message: Message):
    await message.answer("Successfully paid!")
    invite_link = await message.bot.create_chat_invite_link(CHAT_ID, creates_join_request=True)
    member = await message.bot.get_chat_member(chat_id=CHAT_ID, user_id=message.from_user.id)
    if member:
        try:
            await message.bot.unban_chat_member(chat_id=CHAT_ID, user_id=message.from_user.id)
        except TelegramBadRequest as e:
            await message.answer(f"Err: {str(e)}")
    print(invite_link)
    match message.successful_payment.total_amount:
        case 1000:
            ex_data = datetime.now() + timedelta(hours=1)
        case 2000:
            ex_data = datetime.now() + timedelta(hours=2)
        case 3000:
            ex_data = datetime.now() + timedelta(hours=3)
        case _:
            ex_data = datetime.now()
    await run_sql(UpdateUser(tg_id=message.from_user.id, date_time=ex_data))
    await message.answer(f"Chat link: {invite_link}", reply_markup=ReplyKeyboardRemove())
