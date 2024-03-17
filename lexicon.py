from aiogram.types import Message

# message = Message()
start_greeding = ('Давайте сыграем в игру "Угадай число"?\n\n'
                  'По умолчанию используется русский язык.\n'
                  'Чтобы переключить язык на английский введите eng,\n'
                  'чтобы переключить на немецкий введите de\n'
                  'Change to Eglish - enter eng!\n'
                  'Wecksel auf Deitsch - geben Sie de ein !\n'
                  'Чтобы получить правила игры и список доступных\n'
                  'команд - отправьте команду /help')
# print(start_greeding)
language_dict = {0: ('Для начала работы с ботом введите /start',
                     'To start interraction with the bot, enter /start',
                     'Um mit dem Bot zu arbeiten, geben Sie /start ein'),

                 1: ('Правила игры:\n\nЯ загадываю число от 1 до 100, '
                     f'а вам нужно его угадать\nУ вас есть заданное Вами количество попыток '
                     f'попыток\n\nДоступные команды:\n/help - правила '
                     f'игры и список команд\n/cancel - выйти из игры\n'
                     f'/stat - посмотреть статистику\n\nСо скольки попыток Вы угадаете число ?'
                     f'\n(Не больше 10 ! по умолчанию 5)'
                     f'\n/att - количество попыток с которых Вы хотите угадать число\n'
                     f'/schet - Посмотреть счёт\n',

                     'Rules of the game:\n\nI guess a number from 1 to 100,'
                     'You need to guess it\nYou have the number of attempts specified by you'
                     'attempts\n\nAvailable commands:\n/help - rules '
                     'games and list of commands\n/cancel - quit the game\n'
                     '/stat - view statistics\n\nHow many attempts will it take you to guess the number?'
                     '\n(No more than 10 ! default 5)'
                     '\n/att - the number of attempts from which you want to guess the number\n'
                     '/schet - View account\n',

                     f'Spielregeln:\n\nIch schätze eine Zahl von 1 bis 100,'
                     f'Sie müssen es erraten\nSie haben die von Ihnen angegebene Anzahl an Versuchen.'
                     f'attempts\n\nVerfügbare Befehle:\n/help - Rules '
                     f'Spiele und Liste der Befehle\n/Abbrechen – Spiel beenden\n'
                     f'/stat - Statistiken anzeigen\n\nWie viele Versuche werden Sie brauchen, um die Zahl zu erraten?'
                     f'\n(Nicht mehr als 10 ! Standard 5)'
                     f'\n/att – die Anzahl der Versuche, aus denen Sie die Zahl erraten möchten\n'
                     '/schet – Konto anzeigen\n'),

                 2: (' : BOT\n\nНачинаем игру ?',
                     " : BOT\n\nLet's start the game?",
                     ' : BOT\n\nLasst uns das Spiel beginnen?'),

                 3: ('Вы вышли из игры. Если захотите сыграть снова - напишите об этом',
                     'You are out of the game. If you want to play again, write about it',
                     'Du bist aus dem Spiel. Wenn du noch einmal spielen möchtest, schreib darüber'),

                 4: ('А мы итак с вами не играем.\nМожет, сыграем разок?',
                     "We don't play with you anyway.\nMaybe we can play once?",
                     'Wir spielen sowieso nicht mit dir.\nVielleicht können wir einmal spielen?'),

                 5: ('Установить количество попыток введите число от 1 до 10',
                     'Set number of attempts, enter a number from 1 to 10',
                     'Anzahl der Versuche festlegen, Zahl von 1 bis 10 eingeben'),

                 6: ('Количество Ваших попыток = ',
                     'Number of your attempts = ',
                     'Anzahl Ihrer Versuche ='),

                 7: ('Посмотрел счёт ? \n А теперь сыграем ?',
                     "Have You checked your result ? \nLet's go playing now ?",
                     'Hast du dir die Rechnung angesehen? \nLass uns jetzt spielen?'),

                 8: ('Теперь загадайте число для меня от 1 до 100 !',
                     'Now guess a number for me from 1 to 100!',
                     'Erraten Sie mir jetzt eine Zahl von 1 bis 100 !'),

                 9: ('Количество ваших попыток 5,\n загадайте число для меня, пожалуйста !',
                     'The number of your attempts is 5,\n Guess the number for me, please !',
                     'Die Anzahl Ihrer Versuche beträgt 5\n Bitte erraten Sie mir die Zahl !'),

                 10: ('Количество оставшихся попыток - ',
                      'Number of remaining attempts - ',
                      'Anzahl der verbleibenden Versuche - '),

                 11: ('Бот угадал ! Ваше число было ',
                      'The Bot guessed right! Your number was ',
                      'Der Bot hat richtig geraten! Deine Nummer war '),

                 12: ('С какой попытки сейчас хотите угадать ? \nВведите цифру от 1 до 10',
                      'What attempt do you want to guess now? \nEnter a number from 1 to 10',
                      'Welchen Versuch willst du jetzt erraten? \nGeben Sie eine Zahl zwischen 1 und 10 ein'),

                 13: ('Вы загадали Число, я тоже !\nНачинаем игру ?',
                      "You guessed a Number, so did I!\nLet's start the Game?",
                      'Du hast eine Zahl erraten, ich auch!\nLasst uns das Spiel beginnen?'),

                 14: ('Загадайте для меня число от 1 до 100',
                      'Render me a number from 1 to 100',
                      'Gib mir eine Zahl von 1 bis 100'),

                 15: ('Какое число в этот раз для меня загадаете ?',
                      'What number will you wish for me this time?',
                      'Welche Nummer wünschst du mir dieses Mal?'),

                 16: ('Ура!\n\nЯ загадал число от 1 до 100,  попробуй угадать с ',
                      'Well !\n\nI guessed a number from 1 to 100, try to guess it in ',
                      'Gut !\n\nIch habe eine Zahl von 1 bis 100 erraten, versuche sie in '),

                 17: (' попыток !',
                      ' times !',
                      ' Versuchen zu erraten !'),

                 18: ('Пока мы играем в игру, я могу реагировать только на числа от 1до 100 и команды /cancel и /stat',
                      'While we are playing the game I can only respond to numbers from 1 to 100 and the /cancel and /stat commands',
                      'Während wir das Spiel spielen, kann ich nur auf Zahlen von 1 bis 100 und die Befehle /cancel und /stat reagieren'),

                 19: ('Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом',
                      "It's a pity :(\n\nIf you want to play, just write about it",
                      'Schade :(\n\nWenn du mitspielen willst, schreib einfach darüber'),

                 20: ('Мы же сейчас с вами играем. \nПрисылайте, пожалуйста, числа от 1 до 100',
                      "We're playing with you now. \nPlease send numbers from 1 to 100",
                      'Wir spielen jetzt mit dir.\nBitte senden Sie Zahlen von 1 bis 100'),

                 21: ('Ура !!! ', 'WELL ! SUPER !!! ', 'Sehr Gut ! '),

                 22: ('Вы угадали Моё число ',
                      'You guessed my number',
                      'Du hast meine Nummer erraten'),

                 23: ('\n\nМожет, сыграем еще?', '\n\nMaybe we can play again?',
                      '\n\nVielleicht können wir wieder spielen?'),

                 24: ('Мое число меньше', 'My number is less', 'Meine Zahl ist geringer'),

                 25: ('Я назову число ', "I will tell you the Number ", 'Ich sage dir die Nummer '),

                 26: ('Вы же знаете, что я не это число загадал)))',
                      'You know that this is not the number I wished for)))',
                      'Du weißt, dass das nicht die Nummer ist, die ich mir gewünscht habe)))'),

                 27: ('Мое число больше', 'My number is higher', 'Meine Zahl ist höher'),

                 28: ('К сожалению ', 'Unfirtunatelly ', 'Leider '),

                 29: (', у нас больше не осталось попыток. Никто не выиграл :(\n\nМое число было ',

                      ', we have no more attempts left. Nobody won :(\n\nMy number was',
                      ', wir haben keine weiteren Versuche mehr. Niemand hat gewonnen :(\n\nMeine Nummer war'),

                 30: ('\n\nДавайте сыграем ещё !', "\n\nLet's play again!", '\n\nLass uns nochmal spielen!'),

                 31: ('Мы еще не играем. Хотите сыграть?\nУгадайте число с ',
                      "We're not playing yet. Do you want to play?\nGuess the number with ",
                      'Wir spielen noch nicht. Möchtest du spielen?\nErrate die Zahl mit '),

                 32: (' попыток', ' attempts', ' mals'),

                 33: ('Для начала работы с ботом введите /start',
                      'To start working with the bot, enter /start',
                      'Um mit dem Bot zu arbeiten, geben Sie /start ein'
                      ),
                 34: ('Я довольно ограниченный бот, давайте просто сыграем в игру?',
                      "I'm a pretty limited bot, let's just play a game?",
                      'Ich bin ein ziemlich eingeschränkter Bot, lass uns einfach ein Spiel spielen?'),

                 35:('Моё число было ',
                     'I wished for a number ',
                     'Ich wünschte mir eine Nummer'),

                 36:(', Вы хотите сыграть в игру ?',
                     ', do you want to play a game?',
                     'Willst du ein Spiel spielen?')
                }

upper_tily_list = ['CAACAgIAAxkBAAEDsZFl2HQvjYlDvPNaL9pcfqZR4Pp5wQACfQ4AAqgILwh8uDWrBIcPxDQE',
                   'CAACAgIAAxkBAAEDsbNl2HcZWFK7EOpW-VeLxqhJxHpGBAACdQ4AAqgILwg3M2bO6dTA3jQE',
                   'CAACAgIAAxkBAAEDsbdl2HgiMiQ4TPyzr3G3SbDUb18PKQACgAEAAiUDUg-7R8_vNtvrmjQE',
                   'CAACAgIAAxkBAAEDsbll2Hg56vqLrXHFpA5oHuFMZlFn2gAClgEAAiUDUg9RmKWlaV2-BTQE',
                   'CAACAgIAAxkBAAEDsbtl2HhWIPm8IPjdHTZxKUBJ-VIHuQACkgEAAiUDUg8UU-SmOS_2KjQE'
                   ]

lower_tily_list = ['CAACAgIAAxkBAAEDsa1l2HYlXJxjAAFwAiR19vdgPtDX_OYAAnwOAAKoCC8IGWYlexpYAAGENAQ',
                   'CAACAgIAAxkBAAEDscFl2Hnlxbqlg_0HBKxCymS2nNvU3AAClAEAAiUDUg9sdCC_w_PB8zQE',
                   'CAACAgIAAxkBAAEDscNl2Hn1Cwy5j0OIcBgYRlgw-O1uRgACjgEAAiUDUg95yNbGKW8ZejQE',
                   'CAACAgIAAxkBAAEDsc1l2HobGtH9KBXMagcYxvEhuOxp1gAChgEAAiUDUg-b63UIwRKxdDQE',
                   'CAACAgIAAxkBAAEDsc9l2Ho-Brt3q6PjQYRnDBMfMSJ8LQACbA4AAqgILwif4k8L_BlQOjQE']

positiv_answer = ['да', 'давай', 'сыграем', 'игра', 'yes', 'es', 'нуы',
                  'играть', 'хочу играть', 'OK', 'ok', 'хочу', 'lfdfq',
                  'хорошо', 'ну', 'ладно', 'lf', 'la', 'da', 'jr', '[jxe', 'ja']

negative_answer = ['нет', 'не', 'не хочу', 'не буду', 'no', 'net', 'yen', 'ytn', 'nein', 'nicht', 'ne', 'nie']
