import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ContentType
from Token import token_bot
from lexicon import upper_tily_list, lower_tily_list, positiv_answer, negative_answer, language_dict, start_greeding
import time
from UserFilter import BOT_WIN, SET_ATT, users
from External_function import verify_number, get_random_number

BOT_TOKEN = token_bot
# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    # print(message) log
    # print(message.chat.first_name) log
    user_name = message.chat.first_name
    start_time = time.monotonic()
    await message.answer(
        f'Привет, {message.chat.first_name} !\n {start_greeding}')
    # Если пользователь только запустил бота и его нет в словаре 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'user_name': user_name,
            'in_game': False,
            'secret_number': None,
            'attempts': 5,
            'total_games': 0,
            'wins': 0,
            'total': 5,
            'game_list': [],
            'bot_list': [],
            'set_attempts': 'NotSet',
            'user_number': False,
            'bot_taily': 'empty',
            'bot_win': False,
            'bot_pobeda': 0,
            'language': 0,
            'start_time':start_time,
            'end_time':None}
    time.sleep(1)
    print('***********', users[message.from_user.id]["user_name"])
    await message.answer('Если хотите установить количество попыток введите число от 1 до 10\n'
                         'По умолчанию у вас 5 попыток')


@dp.message(F.content_type != ContentType.TEXT)
async def process_notTEXT_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(language_dict[20][users[message.from_user.id]['language']])
    else:
        await message.answer(users[message.from_user.id]['user_name'] + language_dict[36][users[message.from_user.id]['language']] )


@dp.message(F.text.lower().in_(('rus', 'eng', 'de')))
async def set_language(message: Message):
    if message.from_user.id in users.keys():
        if message.text == 'rus' or message.text == 'кгы':
            users[message.from_user.id]['language'] = 0
            await message.answer('Игра продолжится на русском языке')
        elif message.text == 'eng' or message.text == 'утп':
            users[message.from_user.id]['language'] = 1
            await message.answer('The Game is carry on in English')
        elif message.text == 'de' or message.text == 'ву':
            users[message.from_user.id]['language'] = 2
            await message.answer('Das Spiel wird auf Deutsch fortgesetzt')
    else:
        await message.answer(language_dict[33][users[message.from_user.id]['language']])


@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    if message.from_user.id in users.keys():
        await message.answer(language_dict[1][users[message.from_user.id]['language']] + \
                             users[message.from_user.id]['user_name'] + \
                             language_dict[2][users[message.from_user.id]['language']])
    else:
        await message.answer('Для начала работы с ботом введите /start')


@dp.message(F.text.lower().in_(('rus', 'eng', 'de')))
async def set_language(message: Message):
    if message.from_user.id in users.keys():
        if message.text == 'rus' or message.text == 'кгы':
            users[message.from_user.id]['language'] = 0
            await message.answer('Игра продолжится на русском языке')
        elif message.text == 'eng' or message.text == 'утп':
            users[message.from_user.id]['language'] = 1
            await message.answer('The Game is going on in English')
        elif message.text == 'de' or message.text == 'ву':
            users[message.from_user.id]['language'] = 2
            await message.answer('Das Spiel wird auf Deutsch fortgesetzt')
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
                language_dict[3][users[message.from_user.id]['language']])
            await message.answer_sticker('CAACAgIAAxkBAAEDsZll2HU40blXBxl0fJfM1gxprSiB-AACZwADr8ZRGsmQice9AYoCNAQ')
        else:
            await message.answer(language_dict[4][users[message.from_user.id]['language']])
    else:
        await message.answer(language_dict[0][users[message.from_user.id]['language']])


@dp.message(Command(commands='att'))
async def get_attempt_number(message: Message):
    if message.from_user.id in users.keys():
        if not users[message.from_user.id]['in_game']:
            await message.answer(language_dict[5][users[message.from_user.id]['language']])
            users[message.from_user.id]['set_attempts'] = 'NotSet'
        else:
            await message.answer(language_dict[6][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]['attempts']))
    else:
        await message.answer(language_dict[0][users[message.from_user.id]['language']])


@dp.message(Command(commands='schet'))
async def uznatb_schet(message: Message):
    if message.from_user.id in users.keys():
        current_time = time.monotonic()
        secund = (current_time - users[message.from_user.id]["start_time"]) %60
        minut = (current_time - users[message.from_user.id]["start_time"]) //60
        await message.answer(f"{users[message.from_user.id]['user_name']} : {users[message.from_user.id]['wins']}\n"
                             f'BOT : {users[message.from_user.id]["bot_pobeda"]}'
                             f'\nGameTiming : {minut} min, {int(secund)} sec.')
        time.sleep(1)
        await  message.answer(language_dict[7][users[message.from_user.id]['language']])
    else:
        await message.answer(language_dict[0][users[message.from_user.id]['language']])


@dp.message(SET_ATT())
async def user_attempt(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['user_number'] = 'setting_data'
        if message.text.isdigit() and int(message.text) < 11:
            users[message.from_user.id]['attempts'] = int(message.text)
            users[message.from_user.id]['total'] = int(message.text)
            users[message.from_user.id]['set_attempts'] = "SET"
            await message.answer(language_dict[6][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]["attempts"]) + " \n" +
                                 language_dict[8][users[message.from_user.id]['language']])
        else:
            users[message.from_user.id]['attempts'] = 5
            users[message.from_user.id]['total'] = 5
            users[message.from_user.id]['set_attempts'] = "SET"
            await message.answer(language_dict[9][users[message.from_user.id]['language']])
    else:
        await message.answer(
            language_dict[10][users[message.from_user.id]['language']] + str({users[message.from_user.id]["attempts"]}))


@dp.message(BOT_WIN())
async def bot_win(message: Message):
    await message.answer(
        language_dict[11][users[message.from_user.id]['language']] + str(users[message.from_user.id]["bot_list"][-1]))
    await message.answer_sticker('CAACAgIAAxkBAAEDsZNl2HSDGiWepbBz9sB7qIBAXGRAEAACYQADr8ZRGq70R9934jY7NAQ')
    await message.answer(language_dict[35][users[message.from_user.id]['language']]+
                         str(users[message.from_user.id]['secret_number']))
    await message.answer(language_dict[12][users[message.from_user.id]['language']])
    users[message.from_user.id]['in_game'] = False
    users[message.from_user.id]['set_attempts'] = 'NotSet'
    users[message.from_user.id]['bot_win'] = False
    users[message.from_user.id]['bot_list'] = []
    users[message.from_user.id]['game_list'] = []
    users[message.from_user.id]['bot_pobeda'] += 1


@dp.message(lambda message: users[message.from_user.id]['user_number'] == 'setting_data' and message.text.isdigit())
async def set_user_number(message: Message):
    if message.text.isdigit() and int(message.text) < 100:
        users[message.from_user.id]['user_number'] = int(message.text)
        await message.answer(language_dict[13][users[message.from_user.id]['language']])
    else:
        await message.answer(language_dict[14][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(positiv_answer))
@dp.message(lambda message: users[message.from_user.id]['set_attempts'] == 'SET' and not message.text.isdigit)
async def process_positive_answer(message: Message):
    if users[message.from_user.id]['user_number'] == 'setting_data':
        # print("********JJJ*****", users[message.from_user.id]['user_number']) log
        await message.answer(language_dict[15][users[message.from_user.id]['language']])
    else:
        if not users[message.from_user.id]['in_game']:
            users[message.from_user.id]['in_game'] = True
            users[message.from_user.id]['secret_number'] = get_random_number()
            users[message.from_user.id]['set_attempts'] = 'reSET'
            users[message.from_user.id]['bot_taily'] = get_random_number()
            users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])
            print('bot taily = ', users[message.from_user.id]['bot_taily'])
            await message.answer(language_dict[16][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]["attempts"]) +
                                 language_dict[17][users[message.from_user.id]['language']])
            await message.answer_sticker('CAACAgMAAxkBAAEDsZdl2HTxxM_Ex5LbFgXh5kXTu60FJQACzAUAAr-MkAQdi6X60cRhBTQE')
        else:
            await message.answer(language_dict[18][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(negative_answer))
async def process_negative_answer(message: Message):
    print('&&&&&&&&&&&&&&negative works') # log
    if not users[message.from_user.id]['in_game']:
        await message.answer(language_dict[19][users[message.from_user.id]['language']])
        await message.answer_sticker('CAACAgMAAxkBAAEDsZVl2HTCLn_lM0nM94erqfXnriAPpQAC5wQAAr-MkARY4Gt1LYVUxTQE')
    else:
        await message.answer(language_dict[20][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100, ~F.BOT_WIN())
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:

        ############################################## BOT PART #############################################

        if users[message.from_user.id]['bot_taily'] > users[message.from_user.id]['user_number']:
            if len(users[message.from_user.id]['bot_list']) == 1:
                users[message.from_user.id]['bot_taily'] = users[message.from_user.id]['bot_taily'] // 2
                users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])
                if users[message.from_user.id]['bot_list'][0] == users[message.from_user.id]['user_number']:
                    users[message.from_user.id]['bot_win'] = True
            else:
                if users[message.from_user.id]['bot_list'][-1] < users[message.from_user.id]['bot_list'][-2]:
                    # print('list1=  ', users[message.from_user.id]['bot_list'])Здесь должен быть log
                    users[message.from_user.id]['bot_taily'] = (users[message.from_user.id]['bot_taily'] -
                                                                (users[message.from_user.id]['bot_list'][-2] -
                                                                 users[message.from_user.id]['bot_list'][-1]) // 2)
                    users[message.from_user.id]['bot_list'].append(
                        verify_number(users[message.from_user.id]['bot_taily'],
                                      users[message.from_user.id]['bot_list']))
                    if users[message.from_user.id]['bot_taily'] == users[message.from_user.id]['user_number']:
                        users[message.from_user.id]['bot_win'] = True
                else:
                    # print('list2=  ', users[message.from_user.id]['bot_list']) Здесь должен быть log
                    users[message.from_user.id]['bot_taily'] = (users[message.from_user.id]['bot_taily'] -
                                                                (users[message.from_user.id]['bot_list'][-1] -
                                                                 users[message.from_user.id]['bot_list'][-2]) // 2)
                    users[message.from_user.id]['bot_list'].append(
                        verify_number(users[message.from_user.id]['bot_taily'],
                                      users[message.from_user.id]['bot_list']))

                    if users[message.from_user.id]['bot_taily'] == users[message.from_user.id]['user_number']:
                        users[message.from_user.id]['bot_win'] = True

        else:  # Если число меньше загаданного пользователем
            if len(users[message.from_user.id]['bot_list']) == 1:
                # print('list3=  ', users[message.from_user.id]['bot_list']) Здесь должен быть log
                users[message.from_user.id]['bot_taily'] = 1 + (100 - users[message.from_user.id]['bot_taily']) // 2 + \
                                                           users[message.from_user.id]['bot_taily']
                users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])

                if users[message.from_user.id]['bot_list'][0] == users[message.from_user.id]['user_number']:
                    users[message.from_user.id]['bot_win'] = True
            else:  # число меньше загаданного пользователем
                if users[message.from_user.id]['bot_list'][-1] < users[message.from_user.id]['bot_list'][-2]:
                    # print('list4=  ', users[message.from_user.id]['bot_list']) Здесь должен быть log
                    users[message.from_user.id]['bot_taily'] = (1 + users[message.from_user.id]['bot_taily'] +
                                                                ((users[message.from_user.id]['bot_list'][-2] -
                                                                  users[message.from_user.id]['bot_list'][-1]) // 2))

                    if users[message.from_user.id]['bot_taily'] == users[message.from_user.id]['user_number']:
                        users[message.from_user.id]['bot_win'] = True
                    users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])
                else:  # Здесь последнее число больше предпоследнего и меньше заганного
                    users[message.from_user.id]['bot_taily'] = (1 + users[message.from_user.id]['bot_taily'] +
                                                                (users[message.from_user.id]['bot_list'][-1] -
                                                                 users[message.from_user.id]['bot_list'][-2]) // 2)

                    if users[message.from_user.id]['bot_taily'] == users[message.from_user.id]['user_number']:
                        users[message.from_user.id]['bot_win'] = True
                    # print('list5=  ', users[message.from_user.id]['bot_list'])Здесь должен быть log
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
            await message.answer(
                language_dict[21][users[message.from_user.id]['language']] +
                users[message.from_user.id]['user_name'] +
                language_dict[22][users[message.from_user.id]['language']] +
                str(users[message.from_user.id]["secret_number"]))
            await message.answer_sticker('CAACAgIAAxkBAAEDsZNl2HSDGiWepbBz9sB7qIBAXGRAEAACYQADr8ZRGq70R9934jY7NAQ')

        elif int(message.text) > users[message.from_user.id]['secret_number']:
            print(users[message.from_user.id]['game_list'])
            if int(message.text) not in users[message.from_user.id]['game_list']:
                users[message.from_user.id]['attempts'] -= 1
                users[message.from_user.id]['game_list'].append(int(message.text))
                await message.answer(language_dict[24][users[message.from_user.id]['language']])
                random.shuffle(lower_tily_list)
                await message.answer_sticker(random.choice(lower_tily_list))
                await message.answer(language_dict[25][users[message.from_user.id]['language']] + str(
                    users[message.from_user.id]['bot_list'][-2]))
            else:
                await message.answer(language_dict[26][users[message.from_user.id]['language']])


        elif int(message.text) < users[message.from_user.id]['secret_number']:
            if int(message.text) not in users[message.from_user.id]['game_list']:
                users[message.from_user.id]['attempts'] -= 1
                users[message.from_user.id]['game_list'].append(int(message.text))
                await message.answer(language_dict[27][users[message.from_user.id]['language']])
                await message.answer_sticker(random.choice(upper_tily_list))
                await message.answer(language_dict[25][users[message.from_user.id]['language']] + str(
                    users[message.from_user.id]['bot_list'][-2]))
            else:
                await message.answer(language_dict[26][users[message.from_user.id]['language']])

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['attempts'] = users[message.from_user.id]['total']
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['game_list'] = []
            users[message.from_user.id]['user_number'] = 'setting_data' # users[message.from_user.id]['user_number'] == 'setting_data'
            users[message.from_user.id]['bot_list'] = []
            users[message.from_user.id]['bot_win'] = False
            await message.answer(language_dict[28][users[message.from_user.id]['language']] +
                                 users[message.from_user.id]["user_name"] +
                                 language_dict[29][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]["secret_number"]))
            time.sleep(1)
            await message.answer_sticker('CAACAgIAAxkBAAEDsY9l2HPkZZUsr8Ms1jKbIC2NpvA-cQACtAIAAjZ2IA4zoo2zbPUj6zQE')
            time.sleep(1)
            await message.answer(language_dict[30][users[message.from_user.id]['language']])
    else:
        await message.answer(language_dict[31][users[message.from_user.id]['language']] +
                             str(users[message.from_user.id]["attempts"]) +
                             language_dict[32][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    if not message.from_user.id in users:
        await message.answer(language_dict[33][users[message.from_user.id]['language']])
    if users[message.from_user.id]['in_game']:
        await message.answer(language_dict[20][users[message.from_user.id]['language']])
    else:
        await message.answer(language_dict[34][users[message.from_user.id]['language']])
        await message.answer_sticker('CAACAgIAAxkBAAEDsatl2HWZwDhJpwvwho9h62MeKsWQIgACXw4AAqgILwiHbCuoW3ksfDQE')


if __name__ == '__main__':
    dp.run_polling(bot)