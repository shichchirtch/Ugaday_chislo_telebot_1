import random, time
from aiogram.types import ContentType
from aiogram import Router, F
from lexicon import *
from UserFilter import (BOT_WIN, SET_ATT, CHEMPION,
                        DATA_IS_NOT_DIGIT, DATA_IS_DIGIT, USER_NUMBER, BOT_NUMBER)
from External_function import verify_number, choosing_number, reset_user_dict_after_finish
from config import users
from loggers import logger, std_out_logger, std_err_logger
from aiogram.types import Message, ReplyKeyboardRemove
from KeyBoards import keyboard_after_fail, keyboard1, keyboard_attempts, keyboard_after_saying_NO

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
    std_out_logger.info(f'\n  CHEMP FINISHED for {users[message.from_user.id]["user_name"]} Game done !')
    await message.answer(
        f"{users[message.from_user.id]['user_name']} : {users[message.from_user.id]['chemp']['count_user_win']}, "
        f"BOT : {users[message.from_user.id]['chemp']['count_bot_win']}")
    users[message.from_user.id]['chemp']['status'] = False
    if users[message.from_user.id]['chemp']['count_user_win'] > users[message.from_user.id]['chemp']['count_bot_win']:
        await message.answer(f'{users[message.from_user.id]["user_name"]} WINS CHEMPIONAT!\n Go on ?')
    elif users[message.from_user.id]['chemp']['count_user_win'] < users[message.from_user.id]['chemp']['count_bot_win']:
        await message.answer(f'BOT  WINS !\n Go on ?')
    else:
        await message.answer(text='NO WINERS\n Go on ?',
                             reply_markup=keyboard1)
    users[message.from_user.id]['chemp']['count_user_win'] = users[message.from_user.id]['chemp']['count_bot_win'] = 0
    users[message.from_user.id]['chemp_result'] = 0


@Game_router.message(SET_ATT(), DATA_IS_DIGIT(), USER_NUMBER(), ~CHEMPION())
async def user_attempt(message: Message):  # Сюда попадает число при установке количества попыток для угадывания
    if not users[message.from_user.id]['in_game']:
        # users[message.from_user.id]['user_number'] = 'setting_data'
        users[message.from_user.id]['set_attempts'] = "SET"
        if message.text.isdigit() and int(message.text) < 11:
            users[message.from_user.id]['attempts'] = int(message.text)
            users[message.from_user.id]['total'] = int(message.text)
            await message.answer(text=language_dict['attempts number is'][users[message.from_user.id]['language']] +
                                      str(users[message.from_user.id]["attempts"]) + " \n" +
                                      language_dict['give 1-100'][users[message.from_user.id]['language']],
                                 reply_markup=ReplyKeyboardRemove()
                                 )
        else:
            users[message.from_user.id]['attempts'] = 5
            users[message.from_user.id]['total'] = 5
            await message.answer(text=language_dict['number your attempts'][users[message.from_user.id]['language']])
        logger.warning(f'Изменения словаря users =  {users}')  # pprint(users) log
    else:
        await message.answer(
            language_dict['last att'][users[message.from_user.id]['language']] +
            str(users[message.from_user.id]["attempts"]))


@Game_router.message(BOT_WIN())
async def bot_win(message: Message):
    std_out_logger.info(f'\n ******************* BOT WINS {users[message.from_user.id]["user_name"]}, Game done !')
    std_out_logger.info(
        f'******* {users[message.from_user.id]["user_name"]}  имеет статус set_attempts = {users[message.from_user.id]["set_attempts"]}')
    await message.answer(
        language_dict['bot guessed'][users[message.from_user.id]['language']] + str(
            users[message.from_user.id]["bot_list"][-1]))
    await message.answer_sticker(sticker_dict['win'])
    await message.answer(language_dict['My namber was'][users[message.from_user.id]['language']] +
                         str(users[message.from_user.id]['secret_number']))
    await message.answer(text=language_dict['render new att'][users[message.from_user.id]['language']],
                         reply_markup=keyboard_attempts
                         )
    users[message.from_user.id]['bot_pobeda'] += 1
    userID = message.from_user.id
    # CHEMPIONAT PART
    if users[message.from_user.id]['chemp']:
        users[message.from_user.id]['chemp']['count_bot_win'] += 1
        users[message.from_user.id]['chemp_result'] += 1
    reset_user_dict_after_finish(users, userID)  # Здесь происходит перезапись значений в словаре юзера

    if users[message.from_user.id]['chemp_result'] == 5:
        await message.answer('Chemp finish'),
        await chempionat(message)


@Game_router.message(DATA_IS_DIGIT(), USER_NUMBER())
async def set_user_number(message: Message):
    if message.text.isdigit() and int(message.text) <= 100:
        users[message.from_user.id]['user_number'] = int(message.text)
        std_out_logger.info(
            f"\nВыводится статус чемпионата : status =   {users[message.from_user.id]['chemp']['status']}")

        if users[message.from_user.id]['chemp']['status']:  # Если пользователь играет в  чемпионат
            await message.answer(text='Вы загадали Число, я тоже !\n Начинайте угадывать моё число !',
                                 reply_markup=ReplyKeyboardRemove())
            userID = message.from_user.id
            choosing_number(users, userID)
            logger.warning(f'Структура словаря users =  {users}')  # print(users)  #log
            std_out_logger.warning(f"BOT's NUMBER = {users[message.from_user.id]['secret_number']}")

        else:  # Во других случаях
            users[message.from_user.id]['user_number'] = int(
                message.text)  # Здесь происходить загадывание номерая юзером для бота
            std_out_logger.info(
                f'Юзер {users[message.from_user.id]["user_name"]} загадал число {users[message.from_user.id]["user_number"]}')
            print(f'Status user game = {users[message.from_user.id]["in_game"]}')
            if not users[message.from_user.id]["in_game"]:
                await message.answer(text=language_dict['taily is guessed'][users[message.from_user.id]['language']],
                                     reply_markup=keyboard1)
            else:
                await message.answer(language_dict['after_user_win'][users[message.from_user.id]['language']])

    else:
        await message.answer(language_dict['1-100'][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@Game_router.message(DATA_IS_NOT_DIGIT(), BOT_NUMBER(), F.text.lower().in_(positiv_answer))
async def process_positive_answer(message: Message):
    if users[message.from_user.id]['user_number'] == 'setting_data':
        std_out_logger.info(
            f'Юзер {users[message.from_user.id]["user_name"]} играет {users[message.from_user.id]["total_games"] + 1} игру')
        userID = message.from_user.id
        choosing_number(users, userID)
        await message.answer(language_dict['new number'][users[message.from_user.id]['language']],
                             reply_markup=ReplyKeyboardRemove()
                             )
    else:
        if not users[message.from_user.id]['in_game']:
            userID = message.from_user.id
            choosing_number(users, userID)  # вот здесь происходит загадывание секретного числа, и числа с которого бот начинает отвечать

            logger.warning(f'Структура словаря users =  {users}')
            std_out_logger.info(f'BOTs NUMBER  =  {users[message.from_user.id]["secret_number"]} ')

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
    users[message.from_user.id]['set_attempts'] = 'SET'
    std_out_logger.info(f'Юзер {users[message.from_user.id]["user_name"]} ответил нет !')
    if not users[message.from_user.id]['in_game']:
        await message.answer(text=language_dict['pity'][users[message.from_user.id]['language']],
                             reply_markup=ReplyKeyboardRemove())
        await message.answer_sticker(sticker_dict['negative answer'],
                                     reply_markup=keyboard_after_saying_NO)
    elif users[message.from_user.id]['in_game'] and users[message.from_user.id]['game_list'] == []:
        await message.answer(text=language_dict['pity'][users[message.from_user.id]['language']],
                             reply_markup=ReplyKeyboardRemove())
        await message.answer_sticker(sticker_dict['negative answer'],
                                     reply_markup=keyboard_after_saying_NO)
    else:
        await message.answer(language_dict['wrong sent data'][users[message.from_user.id]['language']])


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@Game_router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100, ~F.BOT_WIN())
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:

        ############################################## BOT PART #############################################

        if users[message.from_user.id]['bot_taily'] > users[message.from_user.id]['user_number']:
            if len(users[message.from_user.id]['bot_list']) == 1:
                std_out_logger.info(f'0 bot_list=  {users[message.from_user.id]["bot_list"]} ')

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
                    users[message.from_user.id]['bot_taily'] = (users[message.from_user.id]['bot_taily'] +
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

            std_out_logger.info(f'\nchemp_result  =  {users[message.from_user.id]["chemp_result"]} ')

        if int(message.text) == users[message.from_user.id]['secret_number']:
            # CHEMPIONAT mini block
            if users[message.from_user.id]['chemp']['status']:
                if users[message.from_user.id]['chemp_result'] == 5:
                    await message.answer('Chemp finish'),
                    await chempionat(message)
                else:
                    users[message.from_user.id]['chemp_result'] += 1

            users[message.from_user.id]['wins'] += 1
            userID = message.from_user.id
            std_out_logger.info(f'\nGame is over !  {users[message.from_user.id]["user_name"]} wins ')

            reset_user_dict_after_finish(users, userID)  # Здесь происходит перезапись значений в словаре юзера

            await message.answer(language_dict['wow'][users[message.from_user.id]['language']] +
                                 users[message.from_user.id]['user_name'] +
                                 language_dict['user guessed'][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]["secret_number"]))
            await message.answer_sticker(sticker_dict['win'])
            await message.answer(text=
                                 language_dict['play new game after user wins'][
                                     users[message.from_user.id]['language']],
                                 reply_markup=keyboard1)


        elif int(message.text) > users[message.from_user.id]['secret_number']:
            if int(message.text) not in users[message.from_user.id]['game_list']:
                users[message.from_user.id]['attempts'] -= 1
                users[message.from_user.id]['game_list'].append(int(message.text))

                std_err_logger.info(f'1 game_list=  {users[message.from_user.id]["game_list"]} ')

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

                std_err_logger.info(f'2 game_list=  {users[message.from_user.id]["game_list"]} ')

                await message.answer(language_dict['more'][users[message.from_user.id]['language']])
                await message.answer_sticker(random.choice(upper_tily_list))
                await message.answer(language_dict['bot says number'][users[message.from_user.id]['language']] + str(
                    users[message.from_user.id]['bot_list'][-2]))
            else:
                await message.answer(language_dict['dont repeat your number'][users[message.from_user.id]['language']])

        ########################## NO WINNERS,  ATTEMPTS LOST ############################

        if users[message.from_user.id]['attempts'] == 0:
            std_out_logger.info(
                f'\n Attempts for {users[message.from_user.id]["user_name"]} = 0 Game done ! No Winners...')
            userID = message.from_user.id
            reset_user_dict_after_finish(users, userID)  # Здесь происходит перезапись значений в словаре юзера
            users[message.from_user.id]['attempts'] = users[message.from_user.id]['total']

            await message.answer(language_dict['unf'][users[message.from_user.id]['language']] +
                                 users[message.from_user.id]["user_name"] +
                                 language_dict['no att lost'][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]["secret_number"]))

            time.sleep(1)
            await message.answer_sticker(sticker_dict['no att'])
            std_err_logger.info(f"\n*** This game is over for user {users[message.from_user.id]['user_name']} ***\n")
            time.sleep(1)
            if not users[message.from_user.id]['chemp']['status']:
                await message.answer(text=language_dict['again'][users[message.from_user.id]['language']],
                                     reply_markup=keyboard_after_fail)
            else:  # Если идёт чемпионат, добавляем один раунд
                users[message.from_user.id]['chemp_result'] += 1
                if users[message.from_user.id]['chemp_result'] == 5:
                    std_err_logger.info(
                        f'\n Game in Chemp for {users[message.from_user.id]["user_name"]} = 5 Chemp done ! No Winners\n')
                    await message.answer('-*- CHEMPIONAT FINISHED -*-'),
                    await chempionat(message)  # Запускаю функцию чемпионата
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
