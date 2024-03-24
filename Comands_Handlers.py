import time
from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import Router
from lexicon import *
from UserFilter import RESTART
from External_function import time_counter
from config import users, user_belongnes
from loggers import logger, std_out_logger, std_err_logger
from aiogram.types import Message
from KeyBoards import keyboard_attempts, keyboard1, keyboard_for_help

# Инициализируем роутер уровня модуля
Comand_router = Router()
@Comand_router.message(CommandStart(), RESTART())
async def process_start_command(message: Message):
    # Логируем старт Бота
    logger.debug(f'BOT запущен message = {message} "wr_in"')
    user_name = message.chat.first_name
    start_time = time.monotonic()
    await message.answer(
        f'Привет, {message.chat.first_name} !  \U0001F60A\n {start_greeding}')
    users[message.from_user.id] = user_belongnes.copy()
    users[message.from_user.id]['user_name'] = user_name
    users[message.from_user.id]['start_time'] = start_time
    users[message.from_user.id]['game_list'] = []
    users[message.from_user.id]['bot_list'] = []
    time.sleep(1)
    await message.answer(text='Если хотите установить количество попыток введите число от 1 до 10\n'
                         'По умолчанию у вас 5 попыток',
                         reply_markup=keyboard_attempts)
    std_out_logger.info(f'\nБот запустил {message.chat.first_name}')# print('Only print, when new User start bot') log
    std_err_logger.info(f'\nСтруктура словаря юзера {users[message.from_user.id]["user_name"]} = {users[message.from_user.id]} ')
    logger.warning(f'Структура словаря users =  {users}')# pprint(users) # log

@Comand_router.message(F.text.lower().in_(('rus', 'eng', 'de')))
async def set_language(message: Message):
    if message.from_user.id in users.keys():
        if message.text == 'rus' or message.text == 'кгы':
            users[message.from_user.id]['language'] = 0
            await message.answer('\U0001f1f7\U0001f1fa Игра продолжится на русском языке')
        elif message.text == 'eng' or message.text == 'утп':
            users[message.from_user.id]['language'] = 1
            await message.answer('\U0001f1ec\U0001f1e7 The Game is carry on in English')
        elif message.text == 'de' or message.text == 'ву':
            users[message.from_user.id]['language'] = 2
            await message.answer('\U0001f1e9\U0001f1ea Das Spiel wird auf Deutsch fortgesetzt')
    else:
        await message.answer(language_dict['start chat'][users[message.from_user.id]['language']])


@Comand_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    if message.from_user.id in users.keys():
        await message.answer(text=language_dict['game rules'][users[message.from_user.id]['language']] + \
                             users[message.from_user.id]['user_name'] + \
                             language_dict['start ?'][users[message.from_user.id]['language']],
                             reply_markup=keyboard_for_help)
    else:
        await message.answer('Для начала работы с ботом введите /start')


@Comand_router.message(Command(commands='cancel'))
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


@Comand_router.message(F.text.in_(['Переустановить количество попыток', '/att']))
async def get_attempt_number(message: Message):
    if message.from_user.id in users.keys():
        if not users[message.from_user.id]['in_game']:
            await message.answer(text=language_dict['set attempts number'][users[message.from_user.id]['language']],
                                 reply_markup=keyboard_attempts)
            users[message.from_user.id]['set_attempts'] = 'NotSet'
        else:
            users[message.from_user.id]['set_attempts'] = 'NotSet'
            await message.answer(language_dict['attempts number is'][users[message.from_user.id]['language']] +
                                 str(users[message.from_user.id]['attempts']))
    else:
        await message.answer(language_dict['if not start'][users[message.from_user.id]['language']])


@Comand_router.message(F.text.in_(['/schet','Узнать Счёт']))
async def uznatb_schet(message: Message):
    if message.from_user.id in users.keys():
        minut, secund = time_counter(users[message.from_user.id]["start_time"])
        await message.answer(f"{users[message.from_user.id]['user_name']} : {users[message.from_user.id]['wins']}\n"
                             f'BOT : {users[message.from_user.id]["bot_pobeda"]}\n'
                             f'Total Game : {users[message.from_user.id]["total_games"]}'
                             f'\nGameTiming : {minut} min, {secund} sec.')
        time.sleep(1)
        await  message.answer(text=language_dict['had a look at scores ?'][users[message.from_user.id]['language']],
                              reply_markup=keyboard1)
    else:
        await message.answer(language_dict['if not start'][users[message.from_user.id]['language']])


@Comand_router.message(Command(commands='chemp'))
async def set_new_chempionat(message: Message):
    users[message.from_user.id]['chemp']['status'] = True
    await message.answer(language_dict['start chemp'][users[message.from_user.id]['language']])
    await message.answer(language_dict['give 1-100'][users[message.from_user.id]['language']])