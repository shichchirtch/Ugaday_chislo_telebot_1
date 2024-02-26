import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, BaseFilter
from aiogram.types import Message
from Token import token_bot
from lexicon import  upper_tily_list, lower_tily_list
import time

BOT_TOKEN = token_bot
# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
users = {}

def verify_game_status(data:dict)->bool:
    return users[data.from_user.id]['in_game']
def get_random_number() -> int:
    return random.randint(1, 100)

class OpytClass(BaseFilter):
    async def __call__(self, message):
        return not users[message.from_user.id]['in_game']
# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help')
    # Если пользователь только запустил бота и его нет в словаре 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': False,
            'total_games': 0,
            'wins': 0}

    # Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть заданное Вами количество попыток '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nСо скольки попыток Вы угадаете число ?'
        f'\n(Не больше 10 !)')

# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    if message.from_user.id in users.keys():
        await message.answer(
            f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
            f'Игр выиграно: {users[message.from_user.id]["wins"]}')
        await message.answer('Сыграем ?')
    else:
        await message.answer('Пока что Вы не сыграли ни одной игры !')

# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if message.from_user.id in users.keys():
        if users[message.from_user.id]['in_game']:
            users[message.from_user.id]['in_game'] = False
            await message.answer(
                'Вы вышли из игры. Если захотите сыграть '
                'снова - напишите об этом')
            await message.answer_sticker('CAACAgIAAxkBAAEDsZll2HU40blXBxl0fJfM1gxprSiB-AACZwADr8ZRGsmQice9AYoCNAQ')
        else:
            await message.answer(
                'А мы итак с вами не играем. '
                'Может, сыграем разок?')
    else:
        await message.answer('Для начала работы с ботом введите /start')
#  Этот хэндлер срабатывает тогда, когда пользователь уже согласился сыграть, просто уточняется количество попыток.
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 10, OpytClass())
async def get_attempt_number(message: Message):
    if not users[message.from_user.id]['attempts'] and not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['attempts']=int(message.text)
        time.sleep(1)
        await message.answer('Сыграем ?')

# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть', 'OK', 'ok','хочу',
                                'хорошо', 'ну', 'ладно','lf','la','da']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        # users[message.from_user.id]['attempts'] = 5
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!')
        await message.answer_sticker('CAACAgMAAxkBAAEDsZdl2HTxxM_Ex5LbFgXh5kXTu60FJQACzAUAAr-MkAQdi6X60cRhBTQE')

    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat')

# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду','no', 'net', 'yen','ytn']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом')
        await message.answer_sticker('CAACAgMAAxkBAAEDsZVl2HTCLn_lM0nM94erqfXnriAPpQAC5wQAAr-MkARY4Gt1LYVUxTQE')
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?')
            await message.answer_sticker('CAACAgIAAxkBAAEDsZNl2HSDGiWepbBz9sB7qIBAXGRAEAACYQADr8ZRGq70R9934jY7NAQ')

        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
            random.shuffle(lower_tily_list)
            await message.answer_sticker(random.choice(lower_tily_list))

        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')
            await message.answer_sticker(random.choice(upper_tily_list))

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}\n')
            time.sleep(1)
            await message.answer_sticker('CAACAgIAAxkBAAEDsY9l2HPkZZUsr8Ms1jKbIC2NpvA-cQACtAIAAjZ2IA4zoo2zbPUj6zQE')
            time.sleep(1)
            await message.answer('\nДавайте сыграем еще?')
    else:
        users[message.from_user.id]['attempts']=5
        await message.answer('Мы еще не играем. Хотите сыграть?\n'
                             'Угадайте число с 5 попыток !')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?')
        await message.answer_sticker('CAACAgIAAxkBAAEDsatl2HWZwDhJpwvwho9h62MeKsWQIgACXw4AAqgILwiHbCuoW3ksfDQE')


if __name__ == '__main__':
    dp.run_polling(bot)