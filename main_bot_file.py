from aiogram import Bot, Dispatcher
from Token import token_bot
import Game_handlers
import Comands_Handlers

# Создаем объекты бота и диспетчера
bot = Bot(token_bot)
dp = Dispatcher()
# Регистриуем роутеры в диспетчере
dp.include_router(Comands_Handlers.Comand_router)
dp.include_router(Game_handlers.Game_router)

if __name__ == '__main__':
    dp.run_polling(bot)
