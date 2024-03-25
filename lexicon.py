




start_greeding = ('Давайте сыграем в игру "Угадай число"?\n\n'
                  '\U0001f1f7\U0001f1fa По умолчанию используется русский язык.\n'
                  '\U0001F7E2 Чтобы переключить язык на английский введите eng,\n'
                  '\U0001F7E2 чтобы переключить на немецкий введите de\n'
                  '\U0001f1ec\U0001f1e7 Change to Eglish - enter eng!\n'
                  '\U0001f1e9\U0001f1ea Wecksel auf Deitsch - geben Sie de ein !\n'
                  'Чтобы получить правила игры и список доступных\n'
                  'команд - отправьте команду /help')
# print(start_greeding)
language_dict = {'if not start': ('Для начала работы с ботом введите /start',
                                  'To start interraction with the bot, enter /start',
                                  'Um mit dem Bot zu arbeiten, geben Sie /start ein'),

                 'game rules': ('Правила игры:\n\nЯ загадываю число от 1\uFE0F\u20E3 до 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3, '
                                f'а вам нужно его угадать\nУ вас есть заданное Вами количество попыток '
                                f'попыток\n\nДоступные команды:\n/help - правила '
                                f'игры и список команд\n/cancel - выйти из игры\n'
                                f'/chemp - чемпионат из 5\uFE0F\u20E3 игр с ботом\n\nСо скольки попыток Вы угадаете число ?'
                                f'\n(Не больше \U0001f51f ! по умолчанию 5\uFE0F\u20E3)'
                                f'\n/att - количество попыток с которых Вы хотите угадать число\n'
                                f'/schet - Посмотреть счёт\n',

                                'Rules of the game:\n\nI guess a number from 1 to 100,'
                                'You need to guess it\nYou have the number of attempts specified by you'
                                'attempts\n\nAvailable commands:\n/help - rules '
                                'games and list of commands\n/cancel - quit the game\n'
                                '/chemp - A Campship from 5\uFE0F\u20E3 rounds with the BOT\n\nHow many attempts will it take you to guess the number?'
                                '\n(No more than \U0001f51f ! default 5\uFE0F\u20E3)'
                                '\n/att - the number of attempts from which you want to guess the number\n'
                                '/schet - View account\n',

                                f'Spielregeln:\n\nIch schätze eine Zahl von 1 bis 100,'
                                f'Sie müssen es erraten\nSie haben die von Ihnen angegebene Anzahl an Versuchen.'
                                f'attempts\n\nVerfügbare Befehle:\n/help - Rules '
                                f'Spiele und Liste der Befehle\n/Abbrechen – Spiel beenden\n'
                                f'/chemp - Meisterschaft von 5\uFE0F\u20E3 Spielen mit dem BOT\n\nWie viele Versuche werden Sie brauchen, um die Zahl zu erraten?'
                                f'\n(Nicht mehr als \U0001f51f ! Standard 5\uFE0F\u20E3)'
                                f'\n/att – die Anzahl der Versuche, aus denen Sie die Zahl erraten möchten\n'
                                '/schet – Konto anzeigen\n'),

                 'start ?': (' : BOT\n\nНачинаем игру ?',
                             " : BOT\n\nLet's start the game?",
                             ' : BOT\n\nLasst uns das Spiel beginnen?'),

                 'exit from game': ('Вы вышли из игры. Если захотите сыграть снова - напишите об этом',
                                    'You are out of the game. If you want to play again, write about it',
                                    'Du bist aus dem Spiel. Wenn du noch einmal spielen möchtest, schreib darüber'),

                 'user not in game now': ('А мы итак с вами не играем.\nМожет, сыграем разок?',
                                          "We don't play with you anyway.\nMaybe we can play once?",
                                          'Wir spielen sowieso nicht mit dir.\nVielleicht können wir einmal spielen?'),

                 'set attempts number': ('Установить количество попыток введите число от 1\uFE0F\u20E3 до \U0001f51f',
                                         'Set number of attempts, enter a number from 1\uFE0F\u20E3 to \U0001f51f',
                                         'Anzahl der Versuche festlegen, Zahl von 1\uFE0F\u20E3 bis \U0001f51f eingeben'),

                 'attempts number is': ('Количество Ваших попыток = ',
                                        'Number of your attempts = ',
                                        'Anzahl Ihrer Versuche ='),

                 'had a look at scores ?': ('Посмотрел счёт ? \n А теперь сыграем ?',
                                            "Have You checked your result ? \nLet's go playing now ?",
                                            'Hast du dir die Rechnung angesehen? \nLass uns jetzt spielen?'),

                 'start chemp': ('Начинаем чемпионат из 5\uFE0F\u20E3  игр !',
                                 "We're starting a 5\uFE0F\u20E3 -game championship!",
                                 'Wir starten eine 5\uFE0F\u20E3 -Spiele-Meisterschaft!'),

                 'give me your number': ('Загадывайте число, которое я должен буду отгадать !',
                                         'Render a number that I will have to guess!',
                                         'Geben Sie eine Zahl aus, die ich erraten muss!'),

                 'give 1-100': ('Теперь загадайте число для меня от 1\uFE0F\u20E3 до 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3 !',
                     'Now guess a number for me from 1\uFE0F\u20E3 to 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3 !',
                     'Erraten Sie mir jetzt eine Zahl von 1\uFE0F\u20E3 bis 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3 !'),

                 'number your attempts': ('Количество ваших попыток 5\uFE0F\u20E3 ,\n загадайте число для меня, пожалуйста !',
                     'The number of your attempts is 5\uFE0F\u20E3 ,\n Guess the number for me, please !',
                     'Die Anzahl Ihrer Versuche beträgt 5\uFE0F\u20E3 \n Bitte erraten Sie mir die Zahl !'),

                 'last att': ('Количество оставшихся попыток - ',
                      'Number of remaining attempts - ',
                      'Anzahl der verbleibenden Versuche - '),

                 'bot guessed': ('Бот угадал ! Ваше число было ',
                      'The Bot guessed right! Your number was ',
                      'Der Bot hat richtig geraten! Deine Nummer war '),

                 'render new att': ('С какой попытки сейчас хотите угадать ? \nВведите цифру от 1\uFE0F\u20E3 до \U0001f51f',
                      'What attempt do you want to guess now? \nEnter a number from 1\uFE0F\u20E3 to \U0001f51f',
                      'Welchen Versuch willst du jetzt erraten? \nGeben Sie eine Zahl zwischen 1\uFE0F\u20E3  und \U0001f51f ein'),

                 'taily is guessed': ('Вы загадали Число !\nНачинаем игру ? \U0001f3b0',
                      "You guessed a Number !\nLet's start the Game? \U0001f3b0",
                      'Du hast eine Zahl erraten !\nLasst uns das Spiel beginnen? \U0001f3b0 '),

                 '1-100': ('Загадайте для меня число от 1\uFE0F\u20E3 до 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3',
                      'Render me a number from 1\uFE0F\u20E3 to 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3',
                      'Gib mir eine Zahl von 1\uFE0F\u20E3 bis 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3'),

                 'new number': ('Какое число в этот раз для меня загадаете ?',
                      'What number will you wish for me this time?',
                      'Welche Nummer wünschst du mir dieses Mal?'),

                 'Bot guessed': ('Ура!  \U0001f37e \n\nЯ загадал число от 1\uFE0F\u20E3 до 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3,  попробуй угадать с ',
                      'Well !  \U0001f37e \n\nI guessed a number from 1\uFE0F\u20E3 to 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3, try to guess it in ',
                      'Gut !  \U0001f37e \n\nIch habe eine Zahl von 1\uFE0F\u20E3 bis 1\uFE0F\u20E30\uFE0F\u20E30\uFE0F\u20E3 erraten, versuche sie in '),

                 'Bot guessed part2': (' попыток !',
                      ' times !',
                      ' Versuchen zu erraten !'),

                 'not digit sent in game': ('Пока мы играем в игру, я могу реагировать только на числа от 1 до 100 и команды /cancel и /stat',
                      'While we are playing the game I can only respond to numbers from 1 to 100 and the /cancel and /stat commands',
                      'Während wir das Spiel spielen, kann ich nur auf Zahlen von 1 bis 100 und die Befehle /cancel und /stat reagieren'),

                 'pity': ('Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом \U0001f197 \u2753',
                      "It's a pity :(\n\nIf you want to play, just write about it  \U0001f197 \u2753",
                      'Schade :(\n\nWenn du mitspielen willst, schreib einfach darüber \U0001f197 \u2753'),

                 'wrong sent data': ('Мы же сейчас с вами играем. \nПрисылайте, пожалуйста, числа от 1 до 100',
                                     "We're playing with you now. \nPlease send numbers from 1 to 100",
                                     'Wir spielen jetzt mit dir.\nBitte senden Sie Zahlen von 1 bis 100'),

                 'wow': ('Ура !!! \U0001f389 ', 'WELL ! SUPER !!! \U0001f389 ', 'Sehr Gut ! \U0001f389 '),

                 'user guessed': (' Вы угадали !\U0001f3c6\nМоё число ',
                      'You guessed my number \U0001f3c6 ',
                      'Du hast meine Nummer erraten \U0001f3c6 '),

                 'play new game after user wins': ('\n\nМожет, сыграем еще?', '\n\nMaybe we can play again?',
                      '\n\nVielleicht können wir wieder spielen?'),

                 'less': ('Мое число меньше \u2198\uFE0F', 'My number is less \u2198\uFE0F', 'Meine Zahl ist geringer \u2198\uFE0F'),

                 'bot says number': ('Я назову число ', "I will tell you the Number ", 'Ich sage dir die Nummer '),

                 'dont repeat your number': ('Вы же знаете, что я не это число загадал)))',
                      'You know that this is not the number I wished for)))',
                      'Du weißt, dass das nicht die Nummer ist, die ich mir gewünscht habe)))'),

                 'more': ('Мое число больше \u2197\uFE0F', 'My number is higher \u2197\uFE0F', 'Meine Zahl ist höher \u2197\uFE0F'),

                 'unf': ('\U0001F61E К сожалению ', '\U0001F61E Unfortunatelly ', '\U0001F61E Leider '),

                 'no att lost': (', у нас больше не осталось попыток. Никто не выиграл :(\n\nМое число было ',

                      ', we have no more attempts left. Nobody won :(\n\nMy number was',
                      ', wir haben keine weiteren Versuche mehr. Niemand hat gewonnen :(\n\nMeine Nummer war'),

                 'again': ('\n\nДавайте сыграем ещё ! \U0001F609',
                           "\n\nLet's play again! \U0001F609",
                           '\n\nLass uns nochmal spielen! \U0001F609'),

                 'in game false': ('Мы еще не играем. Хотите сыграть?\nУгадайте число с ',
                      "We're not playing yet. Do you want to play?\nGuess the number with ",
                      'Wir spielen noch nicht. Möchtest du spielen?\nErrate die Zahl mit '),

                 'mal': (' попыток', ' attempts', ' mals'),

                 'start chat': ('Для начала работы с ботом введите /start',
                      'To start working with the bot, enter /start',
                      'Um mit dem Bot zu arbeiten, geben Sie /start ein'
                      ),
                 'silly bot': ('Я довольно ограниченный бот, давайте просто сыграем в игру?',
                      "I'm a pretty limited bot, let's just play a game?",
                      'Ich bin ein ziemlich eingeschränkter Bot, lass uns einfach ein Spiel spielen?'),

                 'My namber was': ('Моё число было ',
                      'I wished for a number ',
                      'Ich wünschte mir eine Nummer'),

                 'wrong content type': (', Вы хотите сыграть в игру ?',
                      ', do you want to play a game?',
                      'Willst du ein Spiel spielen?'),
                 'restart': ('Нельзя запусть бота дважды !)))',
                             'This is impossible to start BOT twice',
                             'Das ist unmöch den BOT zu restart'),

                 'after_user_win':('Вы загадали Число !\nЯ тоже ! \nНачинайте отгадывать !',
                                   'You guessed the Number!\nMe too! \nStart guessing!',
                                    'Du hast die Zahl erraten!\nIch auch! \nFangen Sie an zu raten!'
                                   )
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

sticker_dict = {'process_cancel_command': 'CAACAgIAAxkBAAEDsZll2HU40blXBxl0fJfM1gxprSiB-AACZwADr8ZRGsmQice9AYoCNAQ',
                'win':'CAACAgIAAxkBAAEDsZNl2HSDGiWepbBz9sB7qIBAXGRAEAACYQADr8ZRGq70R9934jY7NAQ',
                'start game sticker':'CAACAgMAAxkBAAEDsZdl2HTxxM_Ex5LbFgXh5kXTu60FJQACzAUAAr-MkAQdi6X60cRhBTQE',
                'negative answer': 'CAACAgMAAxkBAAEDsZVl2HTCLn_lM0nM94erqfXnriAPpQAC5wQAAr-MkARY4Gt1LYVUxTQE',
                'no att':'CAACAgIAAxkBAAEDsY9l2HPkZZUsr8Ms1jKbIC2NpvA-cQACtAIAAjZ2IA4zoo2zbPUj6zQE',
                'silly bot':'CAACAgIAAxkBAAEDsatl2HWZwDhJpwvwho9h62MeKsWQIgACXw4AAqgILwiHbCuoW3ksfDQE'

                }

positiv_answer = ['да', 'давай', 'сыграем', 'игра', 'yes', 'es', 'нуы',
                  'играть', 'хочу играть', 'OK', 'ok', 'хочу', 'lfdfq',
                  'хорошо', 'ну', 'ладно', 'lf', 'la', 'da', 'jr', '[jxe', 'ja']

negative_answer = ['нет', 'не', 'не хочу', 'не буду', 'no', 'net', 'yen', 'ytn', 'nein', 'nicht', 'ne', 'nie']
