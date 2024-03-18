import random
import time
def get_random_number() -> int:
    return random.randint(1, 100)
# a= time.monotonic()
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
# time.sleep(1)
def time_counter(start_time):
    current_time = time.monotonic()
    secund = (current_time - start_time) % 60
    minut = (current_time - start_time) // 60
    return int(minut), int(secund)

# print(time_counter(a))