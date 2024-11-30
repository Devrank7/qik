from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo
from aiogram.utils.deep_linking import create_start_link

from api.stripe.conector import stripe_session, check_stripe_session
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())
data_pay = {}


@router.message(Command("stripe"))
async def stripe_pay(message: Message):
    link_success = await create_start_link(message.bot, "success", encode=True)
    link_cancel = await create_start_link(message.bot, "cancel", encode=True)
    ses_is, url = stripe_session(1000, link_success, link_cancel)
    pay_id = ses_is[-15:]
    data_pay[pay_id] = ses_is
    print("sesid = ", ses_is)
    print(f"stripe, {url}")
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить", url=url),
         InlineKeyboardButton(text="Проверить оплату", callback_data=f"ch_{pay_id}")],
    ])
    await message.answer("Перейдите по ссылке для оплаты", reply_markup=button)


@router.callback_query(F.data.startswith("ch_"))
async def stripe_callback_query(query: CallbackQuery):
    pay_id = query.data.split("_")[1]
    ses_id = data_pay[pay_id]
    print("sesid = ", ses_id)
    if check_stripe_session(ses_id):
        data_pay.pop(pay_id)
        print("Successfully paid to stripe")
        await query.answer("Successfully paid to stripe", show_alert=True)
        await query.message.answer("Successfully paid to stripe")
    else:
        await query.answer("Failed to paid to stripe", show_alert=True)
