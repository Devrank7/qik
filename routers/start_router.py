from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.payload import decode_payload

from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(CommandStart(deep_link=True))
async def start_router(message: Message, command: CommandObject) -> None:
    args = command.args
    payload = decode_payload(args)
    print(payload)
    if not payload:
        await message.answer(f"Hi, {message.from_user.first_name}, to pay closed telegram chanel /pay")
    else:
        if payload in ['success']:
            await message.answer("Успех")
        elif payload in ['cancel']:
            await message.answer("Отклонение")
