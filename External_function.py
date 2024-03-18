import random
import time
def get_random_number() -> int:
    return random.randint(1, 100)

def verify_number(number:int, list_number:list[int])->int:
    if number not in list_number:
        return number
    elif number+1 not in list_number:
        return number+1
    else:
        return number-2

def time_counter(start_time):
    current_time = time.monotonic()
    secund = (current_time - start_time) % 60
    minut = (current_time - start_time) // 60
    return int(minut), int(secund)

def choosing_number(us_dict:dict, userID)->dict:
    us_dict[userID]['in_game'] = True
    us_dict[userID] ['secret_number'] = get_random_number()
    us_dict[userID]['set_attempts'] = 'reSET'
    us_dict[userID]['bot_taily'] = get_random_number()
    us_dict[userID]['bot_list'].append(us_dict[userID]['bot_taily'])
    return us_dict

