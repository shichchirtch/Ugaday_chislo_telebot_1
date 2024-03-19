import time
from aiogram.types import Message

users = {}
user_name = 'empty'  #message["message_id"]['from']['first_name']
#Message.# message.chat.first_name
user_belongnes={
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
            'start_time': None,
            'chemp': {'count_bot_win': 0, 'count_user_win': 0, 'status': False},
            'chemp_result': 0
        }