import random, time
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ContentType
from Token import token_bot
from lexicon import *
from UserFilter import BOT_WIN, SET_ATT, CHEMPION, RESTART
from External_function import verify_number, choosing_number, time_counter, reset_user_dict_after_finish
from config import users, user_belongnes
#  from pprint import pprint  #  Раскомментировать для вывода логов

BOT_TOKEN = token_bot
# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart(), RESTART())
async def process_start_command(message: Message):
    # print(message) log
    # print(message.chat.first_name) log
    user_name = message.chat.first_name
    start_time = time.monotonic()
    await message.answer(
        f'Привет, {message.chat.first_name} !\n {start_greeding}')
    # Если пользователь только запустил бота и его нет в словаре 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = user_belongnes.copy()#{
        users[message.from_user.id]['user_name']= user_name
        users[message.from_user.id]['start_time']= start_time
    time.sleep(1)
    await message.answer('Если хотите установить количество попыток введите число от 1 до 10\n'
                         'По умолчанию у вас 5 попыток')
    #print('Only print, when new User start bot') log
    #pprint(users) # log


@dp.message(F.content_type != ContentType.TEXT)
async def process_notTEXT_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(language_dict['wrong sent data'][users[message.from_user.id]['language']])
    else:
        await message.answer(
            users[message.from_user.id]['user_name'] + language_dict['wrong content type'][users[message.from_user.id]['language']])


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
        await message.answer(language_dict['start chat'][users[message.from_user.id]['language']])


@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    if message.from_user.id in users.keys():
        await message.answer(language_dict['game rules'][users[message.from_user.id]['language']] + \
                             users[message.from_user.id]['user_name'] + \
                             language_dict['start ?'][users[message.from_user.id]['language']])
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
                language_dict['exit from game'][users[message.from_user.id]['language']])
            await message.answer_sticker(sticker_dict['process_cancel_command'])
        else:
            await message.answer(language_dict['user not in game now'][users[message.from_user.id]['language']])
    else:
        await message.answer(language_dict['if not start'][users[message.from_user.id]['language']])


@dp.message(Command(commands='att'))
async def get_attempt_number(message: Message):
    if message.from_user.id in users.keys():
        if not users[message.from_user.id]['in_game']:
            await message.answer(language_dict['set attempts number'][users[message.from_user.id]['language']])
            users[message.from_user.id]['set_attempts'] = 'NotSet'
        else:
            await message.answer(language_dict['attempts number is'][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]['attempts']))
    else:
        await message.answer(language_dict['if not start'][users[message.from_user.id]['language']])


@dp.message(Command(commands='schet'))
async def uznatb_schet(message: Message):
    if message.from_user.id in users.keys():
        minut, secund = time_counter(users[message.from_user.id]["start_time"])
        await message.answer(f"{users[message.from_user.id]['user_name']} : {users[message.from_user.id]['wins']}\n"
                             f'BOT : {users[message.from_user.id]["bot_pobeda"]}\n'
                             f'Total Game : {users[message.from_user.id]["total_games"]}'
                             f'\nGameTiming : {minut} min, {secund} sec.')
        time.sleep(1)
        await  message.answer(language_dict['had a look at scores ?'][users[message.from_user.id]['language']])
    else:
        await message.answer(language_dict['if not start'][users[message.from_user.id]['language']])


@dp.message(Command(commands='chemp'))
async def set_new_chempionat(message: Message):
    users[message.from_user.id]['chemp']['status'] = True
    await message.answer(language_dict['start chemp'][users[message.from_user.id]['language']])
    await message.answer(language_dict['give 1-100'][users[message.from_user.id]['language']])

@dp.message(CHEMPION(), lambda message: users[message.from_user.id]['chemp_result'] == 5)
async def chempionat(message: Message):
    await message.answer(
        f"{users[message.from_user.id]['user_name']} : {users[message.from_user.id]['chemp']['count_user_win']}, "
        f"BOT : {users[message.from_user.id]['chemp']['count_bot_win']}")
    users[message.from_user.id]['chemp']['status'] = False
    if users[message.from_user.id]['chemp']['count_user_win'] > users[message.from_user.id]['chemp']['count_bot_win']:
        await message.answer(f'{users[message.from_user.id]["user_name"]} WINS !\n Go on ?')
    elif users[message.from_user.id]['chemp']['count_user_win'] < users[message.from_user.id]['chemp']['count_bot_win']:
        await message.answer(f'BOT  WINS !\n Go on ?')
    else:
        await message.answer('NO WINERS\n Go on ?')
    users[message.from_user.id]['chemp']['count_user_win'] = users[message.from_user.id]['chemp']['count_bot_win'] = 0
    users[message.from_user.id]['chemp_result'] = 0


@dp.message(SET_ATT())
async def user_attempt(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['user_number'] = 'setting_data'
        users[message.from_user.id]['set_attempts'] = "SET"
        if message.text.isdigit() and int(message.text) < 11:
            users[message.from_user.id]['attempts'] = int(message.text)
            users[message.from_user.id]['total'] = int(message.text)
            await message.answer(language_dict['attempts number is'][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]["attempts"]) + " \n" +
                                 language_dict['give 1-100'][users[message.from_user.id]['language']])
        else:
            users[message.from_user.id]['attempts'] = 5
            users[message.from_user.id]['total'] = 5
            await message.answer(language_dict['number your attempts'][users[message.from_user.id]['language']])
        #  pprint(users) log
    else:
        await message.answer(
            language_dict['last att'][users[message.from_user.id]['language']] + str({users[message.from_user.id]["attempts"]}))


@dp.message(BOT_WIN())
async def bot_win(message: Message):
    await message.answer(
        language_dict['bot guessed'][users[message.from_user.id]['language']] + str(users[message.from_user.id]["bot_list"][-1]))
    await message.answer_sticker(sticker_dict['win'])
    await message.answer(language_dict['My namber was'][users[message.from_user.id]['language']] +
                         str(users[message.from_user.id]['secret_number']))
    await message.answer(language_dict['render new att'][users[message.from_user.id]['language']])
    users[message.from_user.id]['set_attempts'] = 'NotSet'
    users[message.from_user.id]['bot_pobeda'] += 1
    userID = message.from_user.id
    reset_user_dict_after_finish(users, userID)

    if users[message.from_user.id]['chemp_result'] == 5:
        await message.answer('Chemp finish'),
        await chempionat(message)


@dp.message(lambda message: users[message.from_user.id]['user_number'] == 'setting_data' and message.text.isdigit())
async def set_user_number(message: Message):
    if message.text.isdigit() and int(message.text) < 100:
        users[message.from_user.id]['user_number'] = int(message.text)
        # print('stats = ', users[message.from_user.id]['chemp']['status']) log

        if users[message.from_user.id]['chemp']['status']:
            await message.answer('Вы загадали Число, я тоже !\n Начинайте угадывать моё число !')
            userID = message.from_user.id
            choosing_number(users, userID)
            #print(users)  #log
        else:
            await message.answer(language_dict['taily is guessed'][users[message.from_user.id]['language']])
    else:
        await message.answer(language_dict['1-100'][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(positiv_answer))
@dp.message(lambda message: users[message.from_user.id]['set_attempts'] == 'SET' and not message.text.isdigit())
async def process_positive_answer(message: Message):
    if users[message.from_user.id]['user_number'] == 'setting_data':
        # print("********JJJ*****", users[message.from_user.id]['user_number']) log
        await message.answer(language_dict['new number'][users[message.from_user.id]['language']])
    else:
        if not users[message.from_user.id]['in_game']:
            userID = message.from_user.id
            choosing_number(users, userID)
            # pprint(users) log

            # print('bot taily = ', users[message.from_user.id]['bot_taily']) log
            if not users[message.from_user.id]['chemp']['status']:
                await message.answer(language_dict['Bot guessed'][users[message.from_user.id]['language']] +
                                     str(users[message.from_user.id]["attempts"]) +
                                     language_dict['Bot guessed part2'][users[message.from_user.id]['language']])
                await message.answer_sticker(sticker_dict['start game sticker'])
            await message.answer('Какое у меня число ?')
        else:
            await message.answer(language_dict['not digit sent in game'][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(negative_answer))
async def process_negative_answer(message: Message):

    if not users[message.from_user.id]['in_game']:
        await message.answer(language_dict['pity'][users[message.from_user.id]['language']])
        await message.answer_sticker(sticker_dict['negative answer'])
    else:
        await message.answer(language_dict['wrong sent data'][users[message.from_user.id]['language']])


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
        if users[message.from_user.id]['chemp']['status']:
            users[message.from_user.id]['chemp_result'] += 1
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['user_number'] = False
            users[message.from_user.id]['wins'] += 1
            userID = message.from_user.id
            reset_user_dict_after_finish(users, userID)


            await message.answer(language_dict['wow'][users[message.from_user.id]['language']] +
                                    users[message.from_user.id]['user_name'] +
                                    language_dict['user guessed'][users[message.from_user.id]['language']] +
                                    str(users[message.from_user.id]["secret_number"]))
            await message.answer_sticker(sticker_dict['win'])
            await message.answer(language_dict['play new game after user wins'][users[message.from_user.id]['language']])
            if users[message.from_user.id]['chemp_result'] == 5:
                await message.answer('Chemp finish'),
                await chempionat(message)

        elif int(message.text) > users[message.from_user.id]['secret_number']:
            print(users[message.from_user.id]['game_list'])
            if int(message.text) not in users[message.from_user.id]['game_list']:
                users[message.from_user.id]['attempts'] -= 1
                users[message.from_user.id]['game_list'].append(int(message.text))
                await message.answer(language_dict['less'][users[message.from_user.id]['language']])
                random.shuffle(lower_tily_list)
                await message.answer_sticker(random.choice(lower_tily_list))
                await message.answer(language_dict['bot says number'][users[message.from_user.id]['language']] + str(
                    users[message.from_user.id]['bot_list'][-2]))
            else:
                await message.answer(language_dict['dont repeat your number'][users[message.from_user.id]['language']])


        elif int(message.text) < users[message.from_user.id]['secret_number']:
            if int(message.text) not in users[message.from_user.id]['game_list']:
                users[message.from_user.id]['attempts'] -= 1
                users[message.from_user.id]['game_list'].append(int(message.text))
                await message.answer(language_dict['more'][users[message.from_user.id]['language']])
                await message.answer_sticker(random.choice(upper_tily_list))
                await message.answer(language_dict['bot says number'][users[message.from_user.id]['language']] + str(
                    users[message.from_user.id]['bot_list'][-2]))
            else:
                await message.answer(language_dict['dont repeat your number'][users[message.from_user.id]['language']])

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['user_number'] = 'setting_data'
            userID = message.from_user.id
            reset_user_dict_after_finish(users, userID)
            users[message.from_user.id]['attempts'] = users[message.from_user.id]['total']
            await message.answer(language_dict['unf'][users[message.from_user.id]['language']] +
                                 users[message.from_user.id]["user_name"] +
                                 language_dict['no att lost'][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]["secret_number"]))
            time.sleep(1)
            await message.answer_sticker(sticker_dict['no att'])
            time.sleep(1)
            if not users[message.from_user.id]['chemp']['status']:
                await message.answer(language_dict['again'][users[message.from_user.id]['language']])
            else:
                if users[message.from_user.id]['chemp_result'] == 5:
                    await message.answer('-*- CHEMPIONAT FINISHED -*-'),
                    await chempionat(message)
                else:
                    await message.answer("Продолжаем Чемпионат ! Загадывайте следующее число !")

    else:
        await message.answer(language_dict['in game false'][users[message.from_user.id]['language']] +
                             str(users[message.from_user.id]["attempts"]) +
                             language_dict['mal'][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    if not message.from_user.id in users:
        await message.answer(language_dict['start chat'][users[message.from_user.id]['language']])
    if users[message.from_user.id]['in_game']:
        await message.answer(language_dict['wrong sent data'][users[message.from_user.id]['language']])
    else:
        if message.text ==('/start'):
            await message.answer(language_dict['restart'][users[message.from_user.id]['language']])
        else:
            await message.answer(language_dict['silly bot'][users[message.from_user.id]['language']])
            await message.answer_sticker(sticker_dict['silly bot'])


if __name__ == '__main__':
    dp.run_polling(bot)
