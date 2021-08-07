print('Добро пожаловать в игру: Крестики-Нолики!')
input('Нажмите Enter, чтобы начать...')

game = [['', 1, 2, 3],
        [1, '', '', ''],
        [2, '', '', ''],
        [3, '', '', ''],
]

play_game = game.copy()

def play():
    print('--------')
    for x in play_game:
        print(*x)

def won():
    if game[1][1] == 'X' and game[1][2] == 'X' and game[1][3] == 'X':
        print('Крестики победили!')
        return True
    elif game[2][1] == 'X' and game[2][2] == 'X' and game[2][3] == 'X':
        print('Крестики победили!')
        return True
    elif game[3][1] == 'X' and game[3][2] == 'X' and game[3][3] == 'X':
        print('Крестики победили!')
        return True
    elif game[1][1] == 'X' and game[2][1] == 'X' and game[3][1] == 'X':
        print('Крестики победили!')
        return True
    elif game[1][2] == 'X' and game[2][2] == 'X' and game[3][2] == 'X':
        print('Крестики победили!')
        return True
    elif game[1][3] == 'X' and game[2][3] == 'X' and game[3][3] == 'X':
        print('Крестики победили!')
        return True
    elif game[1][1] == 'X' and game[2][2] == 'X' and game[3][3] == 'X':
        print('Крестики победили!')
        return True
    elif game[3][1] == 'X' and game[2][2] == 'X' and game[1][3] == 'X':
        print('Крестики победили!')
        return True

    elif game[1][1] == 'O' and game[1][2] == 'O' and game[1][3] == 'O':
        print('Нолики победили!')
        return True
    elif game[2][1] == 'O' and game[2][2] == 'O' and game[2][3] == 'O':
        print('Нолики победили!')
        return True
    elif game[3][1] == 'O' and game[3][2] == 'O' and game[3][3] == 'O':
        print('Нолики победили!')
        return True
    elif game[1][1] == 'O' and game[2][1] == 'O' and game[3][1] == 'O':
        print('Нолики победили!')
        return True
    elif game[1][2] == 'O' and game[2][2] == 'O' and game[3][2] == 'O':
        print('Нолики победили!')
        return True
    elif game[1][3] == 'O' and game[2][3] == 'O' and game[3][3] == 'O':
        print('Нолики победили!')
        return True
    elif game[1][1] == 'O' and game[2][2] == 'O' and game[3][3] == 'O':
        print('Нолики победили!')
        return True
    elif game[3][1] == 'O' and game[2][2] == 'O' and game[1][3] == 'O':
        print('Нолики победили!')
        return True
    else:
        return False


def XO():
    move_count = 0
    while not won():
        print('--------')
        if move_count % 2 == 0:
            move = input('X(строка столбец): ')
            if move.isdigit():
                move = move.replace(' ', '')
                move = list(map(int, list(move)))
                if move[0] in range(1, 4) and move[1] in range(1, 4):
                    play_game[move[0]][move[1]] = 'X'
                    move_count += 1
                    play()
                else:
                    print('Так нельзя походить!')
                    XO()
            else:
                print('Вы ввели не то, что требуется!')
                XO()
        else:
            move = input('O(строка столбец): ')
            if move.isdigit():
                move = move.replace(' ', '')
                move = list(map(int, list(move)))
                if move[0] in range(1, 4) and move[1] in range(1, 4):
                    play_game[move[0]][move[1]] = 'O'
                    move_count += 1
                    play()
                else:
                    print('Так нельзя походить!')
                    XO()
            else:
                print('Вы ввели не то, что требуется!')
                XO()
    else:
        print('--------')
        print('Конец игры!')

play()
XO()
print('--------')
print('--------')
print('--------')
print('--------')
print('--------')
input()