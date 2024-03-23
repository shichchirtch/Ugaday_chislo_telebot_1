import random, time
from aiogram.types import ContentType
from aiogram import Router, F
from lexicon import *
from UserFilter import BOT_WIN, SET_ATT, CHEMPION
from External_function import verify_number, choosing_number, reset_user_dict_after_finish
from config import users
from loggers import logger, std_out_logger
from aiogram.types import Message, ReplyKeyboardRemove
from KeyBoards import keyboard_after_fail, keyboard1, keyboard_attempts

Game_router = Router()

@Game_router.message(F.content_type != ContentType.TEXT)
async def process_notTEXT_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(language_dict['wrong sent data'][users[message.from_user.id]['language']])
    else:
        await message.answer(
            users[message.from_user.id]['user_name'] + language_dict['wrong content type'][
                users[message.from_user.id]['language']])

@Game_router.message(CHEMPION(), lambda message: users[message.from_user.id]['chemp_result'] == 5)
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
        await message.answer(text='NO WINERS\n Go on ?',
                             reply_markup=keyboard1)
    users[message.from_user.id]['chemp']['count_user_win'] = users[message.from_user.id]['chemp']['count_bot_win'] = 0
    users[message.from_user.id]['chemp_result'] = 0

@Game_router.message(SET_ATT())
async def user_attempt(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['user_number'] = 'setting_data'
        users[message.from_user.id]['set_attempts'] = "SET"
        if message.text.isdigit() and int(message.text) < 11:
            users[message.from_user.id]['attempts'] = int(message.text)
            users[message.from_user.id]['total'] = int(message.text)
            await message.answer(text=language_dict['attempts number is'][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]["attempts"]) + " \n" +
                                 language_dict['give 1-100'][users[message.from_user.id]['language']],
                                  reply_markup = ReplyKeyboardRemove()
                                 )
        else:
            users[message.from_user.id]['attempts'] = 5
            users[message.from_user.id]['total'] = 5
            await message.answer(text=language_dict['number your attempts'][users[message.from_user.id]['language']])
        logger.warning(f'Изменения словаря users =  {users}')#  pprint(users) log
    else:
        await message.answer(
            language_dict['last att'][users[message.from_user.id]['language']] +
            str({users[message.from_user.id]["attempts"]}))


@Game_router.message(BOT_WIN())
async def bot_win(message: Message):
    await message.answer(
        language_dict['bot guessed'][users[message.from_user.id]['language']] + str(
            users[message.from_user.id]["bot_list"][-1]))
    await message.answer_sticker(sticker_dict['win'])
    await message.answer(language_dict['My namber was'][users[message.from_user.id]['language']] +
                         str(users[message.from_user.id]['secret_number']))
    await message.answer(text=language_dict['render new att'][users[message.from_user.id]['language']],
                        reply_markup = keyboard_attempts
                         )
    users[message.from_user.id]['set_attempts'] = 'NotSet'
    users[message.from_user.id]['bot_pobeda'] += 1
    userID = message.from_user.id
    reset_user_dict_after_finish(users, userID)

    if users[message.from_user.id]['chemp_result'] == 5:
        await message.answer('Chemp finish'),
        await chempionat(message)


@Game_router.message(lambda message: users[message.from_user.id]['user_number'] == 'setting_data' and message.text.isdigit())
async def set_user_number(message: Message):
    if message.text.isdigit() and int(message.text) < 100:
        users[message.from_user.id]['user_number'] = int(message.text)
        std_out_logger.info(f"Выводится статус чемпионата : status =   {users[message.from_user.id]['chemp']['status']}")

        if users[message.from_user.id]['chemp']['status']:
            await message.answer(text='Вы загадали Число, я тоже !\n Начинайте угадывать моё число !',
                                 reply_markup=ReplyKeyboardRemove())
            userID = message.from_user.id
            choosing_number(users, userID)
            logger.warning(f'Структура словаря users =  {users}')# print(users)  #log
            std_out_logger.warning(f"BOT's NUMBER = {users[message.from_user.id]['secret_number']}")
        else:
            await message.answer(text=language_dict['taily is guessed'][users[message.from_user.id]['language']],
                                 reply_markup=keyboard1)

    else:
        await message.answer(language_dict['1-100'][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@Game_router.message(F.text.lower().in_(positiv_answer))
@Game_router.message(lambda message: users[message.from_user.id]['set_attempts'] == 'SET' and not message.text.isdigit())
async def process_positive_answer(message: Message):

    if users[message.from_user.id]['user_number'] == 'setting_data':
        std_out_logger.info(f'Юзер {users[message.from_user.id]["user_name"]} играет {users[message.from_user.id]["total_games"]+1} игру')

        await message.answer(language_dict['new number'][users[message.from_user.id]['language']],
                             reply_markup=ReplyKeyboardRemove()
                             )
    else:
        if not users[message.from_user.id]['in_game']:
            userID = message.from_user.id
            choosing_number(users, userID)
            logger.warning(f'Структура словаря users =  {users}')
            std_out_logger.info(f'BOTs NUMBER  =  {users[message.from_user.id]["secret_number"]} ')
            std_out_logger.info(f'Юзер {users[message.from_user.id]["user_name"]} загадал число {users[message.from_user.id]["user_number"]}')

            if not users[message.from_user.id]['chemp']['status']:
                await message.answer(language_dict['Bot guessed'][users[message.from_user.id]['language']] +
                                     str(users[message.from_user.id]["attempts"]) +
                                     language_dict['Bot guessed part2'][users[message.from_user.id]['language']],
                                     reply_markup=ReplyKeyboardRemove())
                await message.answer_sticker(sticker_dict['start game sticker'])
            await message.answer(text='Какое у меня число ?',
                                 reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(language_dict['not digit sent in game'][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@Game_router.message(F.text.lower().in_(negative_answer))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(text=language_dict['pity'][users[message.from_user.id]['language']],
                             reply_markup=ReplyKeyboardRemove())
        await message.answer_sticker(sticker_dict['negative answer'],
                                     reply_markup=keyboard1)
    else:
        await message.answer(language_dict['wrong sent data'][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@Game_router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100, ~F.BOT_WIN())
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

                    std_out_logger.info(f'1 bot_list=  {users[message.from_user.id]["bot_list"]} ')
                    users[message.from_user.id]['bot_taily'] = (users[message.from_user.id]['bot_taily'] -
                                                                (users[message.from_user.id]['bot_list'][-2] -
                                                                 users[message.from_user.id]['bot_list'][-1]) // 2)
                    users[message.from_user.id]['bot_list'].append(
                        verify_number(users[message.from_user.id]['bot_taily'],
                                      users[message.from_user.id]['bot_list']))
                    if users[message.from_user.id]['bot_taily'] == users[message.from_user.id]['user_number']:
                        users[message.from_user.id]['bot_win'] = True
                else:
                    std_out_logger.info(f'2 bot_list=  {users[message.from_user.id]["bot_list"]} ')

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

                std_out_logger.info(f'3 bot_list=  {users[message.from_user.id]["bot_list"]} ')
                users[message.from_user.id]['bot_taily'] = 1 + (100 - users[message.from_user.id]['bot_taily']) // 2 + \
                                                           users[message.from_user.id]['bot_taily']
                users[message.from_user.id]['bot_list'].append(users[message.from_user.id]['bot_taily'])

                if users[message.from_user.id]['bot_list'][0] == users[message.from_user.id]['user_number']:
                    users[message.from_user.id]['bot_win'] = True
            else:  # число меньше загаданного пользователем
                if users[message.from_user.id]['bot_list'][-1] < users[message.from_user.id]['bot_list'][-2]:
                    std_out_logger.info(f'4 bot_list=  {users[message.from_user.id]["bot_list"]} ')
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

                    std_out_logger.info(f'5 bot_list=  {users[message.from_user.id]["bot_list"]} ')
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
            await message.answer(text=
                language_dict['play new game after user wins'][users[message.from_user.id]['language']],
                                reply_markup=keyboard1)
            if users[message.from_user.id]['chemp_result'] == 5:
                await message.answer('Chemp finish'),
                await chempionat(message)

        elif int(message.text) > users[message.from_user.id]['secret_number']:
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
            std_out_logger.info(f"\n*** This game is over for user {users[message.from_user.id]['user_name']} ***\n")
            time.sleep(1)
            if not users[message.from_user.id]['chemp']['status']:
                await message.answer(text=language_dict['again'][users[message.from_user.id]['language']],
                                     reply_markup=keyboard_after_fail)
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

@Game_router.message()
async def process_other_answers(message: Message):
    if not message.from_user.id in users:
        await message.answer(language_dict['start chat'][users[message.from_user.id]['language']])
    if users[message.from_user.id]['in_game']:
        await message.answer(language_dict['wrong sent data'][users[message.from_user.id]['language']])
    else:
        if message.text == ('/start'):
            await message.answer(language_dict['restart'][users[message.from_user.id]['language']])
        else:
            await message.answer(language_dict['silly bot'][users[message.from_user.id]['language']])
            await message.answer_sticker(sticker_dict['silly bot'])