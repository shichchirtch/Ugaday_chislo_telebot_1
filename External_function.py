import random
from UserFilter import users
def verify_game_status(data: dict) -> bool:
    return users[data.from_user.id]['in_game']


def get_random_number() -> int:
    return random.randint(1, 100)

def verify_number(number:int, list_number:list[int])->int:
    # print('data to verify ', number)
    if number not in list_number:
        # print('verify works ! ', number)
        return number
    elif number+1 not in list_number:
        # print('2verify works ! ', number)
        return number+1
    else:
        # print('3verify works ! ', number)
        return number-2