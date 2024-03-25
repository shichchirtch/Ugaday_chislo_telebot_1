from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import users


class SET_ATT(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if users[message.from_user.id]['set_attempts'] == 'NotSet':
            return True
        return False


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

class RESTART(BaseFilter):
    async def __call__(self, message:Message):
        if message.from_user.id in users:
            return False
        return True

class DATA_IS_NOT_DIGIT(BaseFilter):
    async  def __call__(self, message:Message):
        if not message.text.isdigit():
            return True
        return False

class DATA_IS_DIGIT(BaseFilter):
    async def __call__(self, message:Message):
        if message.text.isdigit():
            return True
        return False

class USER_NUMBER(BaseFilter):
    async def __call__(self, message: Message):
        if users[message.from_user.id]['user_number']=='setting_data' :
            return True
        return False

class BOT_NUMBER(BaseFilter):
    async def __call__(self, message:Message):
        if users[message.from_user.id]['bot_taily'] == 'empty':
            return True
        return False