from aiogram.filters import BaseFilter
from aiogram.types import Message
users={}
class SET_ATT(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return users[message.from_user.id]['set_attempts'] == 'NotSet'

class BOT_WIN(BaseFilter):
    async def __call__(self, message:Message):
        return users[message.from_user.id]['bot_win']==True