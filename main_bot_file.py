import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ContentType
from Token import token_bot
from lexicon import upper_tily_list, lower_tily_list, positiv_answer, negative_answer
import time
from UserFilter import BOT_WIN, SET_ATT, users
from External_function import verify_number, get_random_number, verify_game_status
BOT_TOKEN = token_bot
# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def process_start_command(message: Message):
    print(message)
    print(message.chat.first_name)
    await message.answer(
        f'Привет, {message.chat.first_name} !\nДавайте сыграем в игру "Угадай число"?\n\n'
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
            'game_list': [],
            'bot_list':[],
            'set_attempts': 'NotSet',
            'user_number': False,
            'bot_taily':'empty',
            'bot_win':False,
            'bot_pobeda': 0}
    time.sleep(1)
    await message.answer('Если хотите установить количество попыток введите число от 1 до 10\n'
                         'По умолчанию у вас 5 попыток')


@dp.message(F.content_type != ContentType.TEXT)
async def process_notTEXT_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer(
            f'{message.chat.first_name} Вы хотите сыграть в игру ?')

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

@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if message.from_user.id in users.keys():
        if users[message.from_user.id]['in_game']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['game_list'] = []
            users[message.from_user.id]['set_attempts'] = "NotSet"
            await message.answer(
                'Вы вышли из игры. Если захотите сыграть '
                'снова - напишите об этом')
            await message.answer_sticker('CAACAgIAAxkBAAEDsZll2HU40blXBxl0fJfM1gxprSiB-AACZwADr8ZRGsmQice9AYoCNAQ')
        else:
            await message.answer('А мы итак с вами не играем.\nМожет, сыграем разок?')
    else:
        await message.answer('Для начала работы с ботом введите /start')

@dp.message(Command(commands='att'))
async def get_attempt_number(message: Message):
    if message.from_user.id in users.keys():
        if not users[message.from_user.id]['in_game']:
            await message.answer('Установить количество попыток введите число от 1 до 10')
            users[message.from_user.id]['set_attempts'] = 'NotSet'
        else:
            await message.answer(f'У вас {users[message.from_user.id]["attempts"]} попыток')
    else:
        await message.answer('Для начала работы с ботом введите /start')

@dp.message(Command(commands='schet'))
async def uznatb_schet(message:Message):
    if message.from_user.id in users.keys():
        await message.answer(f'{message.chat.first_name} : {users[message.from_user.id]["wins"]}\n'
                             f'BOT : {users[message.from_user.id]["bot_pobeda"]}')
        time.sleep(1)
        await  message.answer('Посмотрел счёт ? \n А теперь сыграем ?')
    else:
        await message.answer('Для начала работы с ботом введите /start')


@dp.message(SET_ATT())
async def user_attempt(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['user_number'] = 'setting_data'
        if message.text.isdigit() and int(message.text) < 11:
            users[message.from_user.id]['attempts'] = int(message.text)
            users[message.from_user.id]['total'] = int(message.text)
            users[message.from_user.id]['set_attempts'] = "SET"
            await message.answer(f'Количество ваших попыток'
                                 f' {users[message.from_user.id]["attempts"]}\n'
                                 f'Теперь загадайте число для меня от 1 до 100 !')
        else:
            users[message.from_user.id]['attempts'] = 5
            users[message.from_user.id]['total'] = 5
            users[message.from_user.id]['set_attempts'] = "SET"
            await message.answer(f'Количество ваших попыток {5}\n'
                                 f'загадайте число для меня, пожалуйста !')
    else:
        await message.answer(f'Количество оставшихся попыток - {users[message.from_user.id]["attempts"]}')

@dp.message(BOT_WIN())
async def bot_win(message:Message):
    await message.answer(f'Бот угадал ! Ваше число было {users[message.from_user.id]["bot_list"][-1]}')
    await message.answer_sticker('CAACAgIAAxkBAAEDsZNl2HSDGiWepbBz9sB7qIBAXGRAEAACYQADr8ZRGq70R9934jY7NAQ')
    await message.answer('С какой попытки сейчас хотите угадать ? Введите цифру от 1 до 10')
    users[message.from_user.id]['in_game'] = False
    users[message.from_user.id]['set_attempts'] = 'NotSet'
    users[message.from_user.id]['bot_win'] = False
    users[message.from_user.id]['bot_list'] = []
    users[message.from_user.id]['game_list'] = []
    users[message.from_user.id]['bot_pobeda'] +=1


@dp.message(lambda message: users[message.from_user.id]['user_number'] == 'setting_data')
async def set_user_number(message:Message):
    if message.text.isdigit() and int(message.text) < 100:
        users[message.from_user.id]['user_number'] = int(message.text)
        await message.answer('Вы загадали число, я тоже !\nНачинаем игру ?')
    else:
        await message.answer('Загадайте для меня чило от 1 до 100')

# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(positiv_answer))
@dp.message(lambda message: users[message.from_user.id]['set_attempts'] == 'SET' and not message.text.isdigit)
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['user_number']:
        await message.answer('Какое число в этот раз для меня загадаете ?')

    else:
        if not users[message.from_user.id]['in_game']:
            users[message.from_user.id]['in_game'] = True
            users[message.from_user.id]['secret_number'] = get_random_number()
            users[message.from_user.id]['set_attempts'] = 'reSET'
            users[message.from_user.id]['bot_taily']=get_random_number()
            users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])
            print('bot taily = ', users[message.from_user.id]['bot_taily'])
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
@dp.message(F.text.lower().in_(negative_answer))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом')
        await message.answer_sticker('CAACAgMAAxkBAAEDsZVl2HTCLn_lM0nM94erqfXnriAPpQAC5wQAAr-MkARY4Gt1LYVUxTQE')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100, ~F.BOT_WIN())
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:

        ############################################## BOT PART #############################################

        if users[message.from_user.id]['bot_taily'] > users[message.from_user.id]['user_number']:
            if len(users[message.from_user.id]['bot_list']) == 1:
                print('list=  ',users[message.from_user.id]['bot_list'])
                users[message.from_user.id]['bot_taily']= users[message.from_user.id]['bot_taily']//2
                users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])
                if users[message.from_user.id]['bot_list'][0] == users[message.from_user.id]['user_number']:
                    users[message.from_user.id]['bot_win'] = True
            else:
                if users[message.from_user.id]['bot_list'][-1] < users[message.from_user.id]['bot_list'][-2]:
                    print('list1=  ', users[message.from_user.id]['bot_list'])
                    users[message.from_user.id]['bot_taily'] =(users[message.from_user.id]['bot_taily'] -
                                                               (users[message.from_user.id]['bot_list'][-2] -
                                                                users[message.from_user.id]['bot_list'][-1])//2)
                    users[message.from_user.id]['bot_list'].append(
                        verify_number(users[message.from_user.id]['bot_taily'],
                                      users[message.from_user.id]['bot_list']))
                    if users[message.from_user.id]['bot_taily'] == users[message.from_user.id]['user_number']:
                        users[message.from_user.id]['bot_win'] = True
                else:
                    print('list2=  ', users[message.from_user.id]['bot_list'])
                    users[message.from_user.id]['bot_taily'] = (users[message.from_user.id]['bot_taily'] -
                                                                (users[message.from_user.id]['bot_list'][-1] -
                                                                 users[message.from_user.id]['bot_list'][-2]) // 2)
                    users[message.from_user.id]['bot_list'].append(verify_number(users[message.from_user.id]['bot_taily'],
                                                                                     users[message.from_user.id]['bot_list']))

                    if users[message.from_user.id]['bot_taily'] == users[message.from_user.id]['user_number']:
                        users[message.from_user.id]['bot_win'] = True

        else: # Если число меньше загаданного пользователем
            if len(users[message.from_user.id]['bot_list']) == 1:
                print('list3=  ', users[message.from_user.id]['bot_list'])
                users[message.from_user.id]['bot_taily'] =1 + (100 - users[message.from_user.id]['bot_taily'])//2 + users[message.from_user.id]['bot_taily']
                users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])

                if users[message.from_user.id]['bot_list'][0] == users[message.from_user.id]['user_number']:
                    users[message.from_user.id]['bot_win'] = True
            else: # число меньше загаданного пользователем
                if users[message.from_user.id]['bot_list'][-1] < users[message.from_user.id]['bot_list'][-2]:
                    print('list4=  ', users[message.from_user.id]['bot_list'])
                    users[message.from_user.id]['bot_taily'] = 1 + users[message.from_user.id]['bot_taily'] + ((users[message.from_user.id]['bot_list'][-2] - users[message.from_user.id]['bot_list'][-1])//2)
                    if users[message.from_user.id]['bot_taily'] == users[message.from_user.id]['user_number']:
                        users[message.from_user.id]['bot_win'] = True
                    users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])
                else: # Здесь последнее число больше предпоследнего и меньше заганного
                    users[message.from_user.id]['bot_taily'] = 1 + users[message.from_user.id]['bot_taily'] + (users[message.from_user.id]['bot_list'][-1]-users[message.from_user.id]['bot_list'][-2])//2
                    if users[message.from_user.id]['bot_taily'] == users[message.from_user.id]['user_number']:
                        users[message.from_user.id]['bot_win'] = True
                    print('list5=  ', users[message.from_user.id]['bot_list'])
                    if users[message.from_user.id]['bot_taily'] > 100:
                        users[message.from_user.id]['bot_taily'] = 100
                    users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])

#########################################  USER PART  ###################################################

        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            users[message.from_user.id]['game_list'] = []
            users[message.from_user.id]['attempts'] = users[message.from_user.id]['total']
            users[message.from_user.id]['user_number'] = False
            users[message.from_user.id]['bot_win'] = False
            users[message.from_user.id]['bot_list'] = []
            users[message.from_user.id]['user_number'] = False
            await message.answer(
                f'Ура!!! {message.chat.first_name} Вы угадали Моё число {users[message.from_user.id]["secret_number"]} !\n\n'
                'Может, сыграем еще?')
            await message.answer_sticker('CAACAgIAAxkBAAEDsZNl2HSDGiWepbBz9sB7qIBAXGRAEAACYQADr8ZRGq70R9934jY7NAQ')

        elif int(message.text) > users[message.from_user.id]['secret_number']:
            if int(message.text) not in users[message.from_user.id]['game_list']:
                users[message.from_user.id]['attempts'] -= 1
                users[message.from_user.id]['game_list'].append(int(message.text))
                await message.answer('Мое число меньше')
                random.shuffle(lower_tily_list)
                await message.answer_sticker(random.choice(lower_tily_list))
                await message.answer(f"Я назову число {users[message.from_user.id]['bot_list'][-2]}")
            else:
                await message.answer('Вы же знаете, что я не это число загадал)))')


        elif int(message.text) < users[message.from_user.id]['secret_number']:
            if int(message.text) not in users[message.from_user.id]['game_list']:
                users[message.from_user.id]['attempts'] -= 1
                users[message.from_user.id]['game_list'].append(int(message.text))
                await message.answer('Мое число больше')
                await message.answer_sticker(random.choice(upper_tily_list))
                await message.answer(f"Я нозову число {users[message.from_user.id]['bot_list'][-2]}")
            else:
                await message.answer('Вы же знаете, что я не это число загадал)))')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['attempts'] = users[message.from_user.id]['total']
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['game_list'] = []
            users[message.from_user.id]['user_number'] = False
            users[message.from_user.id]['bot_list'] = []
            users[message.from_user.id]['bot_win'] = False
            await message.answer(
                f'К сожалению {message.chat.first_name}, у нас больше не осталось '
                f'попыток. Никто не выиграл :(\n\nМое число '
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
    if not message.from_user.id in users:
        await message.answer('Для начала работы с ботом введите /start')
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