from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# создаю конструктор клавиатур
kb_builder = ReplyKeyboardBuilder()
#Создаю кнопки
start_button_1 = KeyboardButton(text='ДА')
start_button_2 = KeyboardButton(text='НЕТ')
att_button = KeyboardButton(text='Переустановить количество попыток')
schet_button = KeyboardButton(text='Узнать Счёт')

#  Создаю клавиатуру на согласие играть
keyboard1 = ReplyKeyboardMarkup(
    keyboard=[[start_button_1, start_button_2]],
    resize_keyboard=True)

#  создаю кнопки для установки количества попыток
buttons_attempts: list[KeyboardButton] = [KeyboardButton(text=f'{i + 1}') for i in range(10)]

#  создаю клавиатуру установки количества попыток
keyboard_attempts = ReplyKeyboardMarkup(
    keyboard=[buttons_attempts],
    resize_keyboard=True)
#  создаю клавитуру после проигрыша
keyboard_after_fail = ReplyKeyboardMarkup(
    keyboard=[[start_button_1, start_button_2],[att_button],[schet_button]],
    resize_keyboard=True)