from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import users


class SET_ATT(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return users[message.from_user.id]['set_attempts'] == 'NotSet'


class BOT_WIN(BaseFilter):
    async def __call__(self, message: Message):
        if users[message.from_user.id]['bot_win']:
            return True
        return False


class CHEMPION(BaseFilter):
    async def __call__(self, message: Message):
        if users[message.from_user.id]['chemp']['status']:
            return True
        return False
