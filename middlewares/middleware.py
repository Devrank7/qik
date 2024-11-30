from typing import Callable, Any, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from db.sql.service import run_sql, ReadUser, CreateUser


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        print("username = ", event.from_user.username)
        result = await run_sql(ReadUser(event.from_user.id))
        if result is None:
            result = await run_sql(CreateUser(event.from_user.id))
        data['user'] = result
        return await handler(event, data)
