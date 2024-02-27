import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from Token import token_bot
from lexicon import  upper_tily_list, lower_tily_list, attempts_dict, att_choice
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

def get_attempts_user(number:str)->int:
    if number in ('abcdefgehij'):
        return attempts_dict[number]
    else:
        return 5

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Согласны ? \n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help')
    # Если пользователь только запустил бота и его нет в словаре 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': 5,
            'total_games': 0,
            'wins': 0,
            'total': 5,
            'game_list':[]}

    # Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    if message.from_user.id in users.keys():
        await message.answer(
            f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
            f'а вам нужно его угадать\nУ вас есть заданное Вами количество попыток '
            f'попыток\n\nДоступные команды:\n/help - правила '
            f'игры и список команд\n/cancel - выйти из игры\n'
            f'/stat - посмотреть статистику\n\nСо скольки попыток Вы угадаете число ?'
            f'\n(Не больше 10 ! по умолчанию 5)'
            f'\n/att - количество попыток с которых Вы хотите угадать число'
            f'\n\nНачинаем игру ?')
    else:
        await message.answer('Для начала работы с ботом введите /start')

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
            users[message.from_user.id]['game_list'] = []
            await message.answer(
                'Вы вышли из игры. Если захотите сыграть '
                'снова - напишите об этом')
            await message.answer_sticker('CAACAgIAAxkBAAEDsZll2HU40blXBxl0fJfM1gxprSiB-AACZwADr8ZRGsmQice9AYoCNAQ')
        else:
            await message.answer('А мы итак с вами не играем.\nМожет, сыграем разок?')
    else:
        await message.answer('Для начала работы с ботом введите /start')
#  Этот хэндлер срабатывает тогда, когда пользователь уже согласился сыграть, просто уточняется количество попыток.

@dp.message(Command(commands='att'))
async def get_attempt_number(message: Message):
    if message.from_user.id in users.keys():
        if not users[message.from_user.id]['in_game']:
            await message.answer(att_choice)
        else:
            await message.answer(f'У вас {users[message.from_user.id]["attempts"]} попыток')
    else:
        await message.answer('Для начала работы с ботом введите /start')

@dp.message(F.text.lower().in_ ("abcdefghij"))
async def user_attempt(message:Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['attempts'] = get_attempts_user(message.text)
        users[message.from_user.id]['total'] = get_attempts_user(message.text)
        await message.answer(f'Количество ваших попыток {users[message.from_user.id]["attempts"]}\nНачинаем игру ?')
    else:
        await message.answer(f'Количество оставшихся попыток - {users[message.from_user.id]["attempts"]}')

# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра','yes', 'es','нуы',
                                'играть', 'хочу играть', 'OK', 'ok','хочу','lfdfq',
                                'хорошо', 'ну', 'ладно','lf','la','da','jr','[jxe']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game'] :
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        await message.answer(
                'Ура!\n\nЯ загадал число от 1 до 100, '
                f'попробуй угадать c {users[message.from_user.id]["attempts"]} попыток !')
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
            'Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом')
        await message.answer_sticker('CAACAgMAAxkBAAEDsZVl2HTCLn_lM0nM94erqfXnriAPpQAC5wQAAr-MkARY4Gt1LYVUxTQE')
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            users[message.from_user.id]['game_list'] = []
            users[message.from_user.id]['attempts'] = users[message.from_user.id]['total']
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?')
            await message.answer_sticker('CAACAgIAAxkBAAEDsZNl2HSDGiWepbBz9sB7qIBAXGRAEAACYQADr8ZRGq70R9934jY7NAQ')

        elif int(message.text) > users[message.from_user.id]['secret_number']:
            if int(message.text) not in users[message.from_user.id]['game_list']:
                users[message.from_user.id]['attempts'] -= 1
                users[message.from_user.id]['game_list'].append(int(message.text))
                await message.answer('Мое число меньше')
                random.shuffle(lower_tily_list)
                await message.answer_sticker(random.choice(lower_tily_list))
            else:
                await message.answer('Вы же знаете, что я не это число загадал)))')

        elif int(message.text) < users[message.from_user.id]['secret_number']:
            if int(message.text) not in users[message.from_user.id]['game_list']:
                users[message.from_user.id]['attempts'] -= 1
                users[message.from_user.id]['game_list'].append(int(message.text))
                await message.answer('Мое число больше')
                await message.answer_sticker(random.choice(upper_tily_list))
            else:
                await message.answer('Вы же знаете, что я не это число загадал)))')


        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['attempts'] = users[message.from_user.id]['total']
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['game_list']= []
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}\n')
            time.sleep(1)
            await message.answer_sticker('CAACAgIAAxkBAAEDsY9l2HPkZZUsr8Ms1jKbIC2NpvA-cQACtAIAAjZ2IA4zoo2zbPUj6zQE')
            time.sleep(1)
            await message.answer('\nДавайте сыграем еще?')
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?\n'
                             f'Угадайте число с {users[message.from_user.id]["attempts"]} попыток !')

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