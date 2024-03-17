from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ContentType
from UserFilter import users
dp = Dispatcher()
import time
import datetime

a= [1,2,3]
start = time.monotonic()
for x in a:
    x+=1
    time.sleep(1)
end = time.monotonic()
# print(start)
# rest = time.ctime(end -start)
# print ("rest =", rest)
s = end-start
print(s%60)
