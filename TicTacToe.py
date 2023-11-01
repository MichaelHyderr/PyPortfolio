import random
from copy import deepcopy

# ---- BOARD DEL GIOCO E RELATIVA DICT DI RIFERIMENTO ----
BOARD = """
       1     2     3
          |     |     
    a  •  |  •  |  •  
     _____|_____|_____
          |     |     
    b  •  |  •  |  •  
     _____|_____|_____
          |     |     
    c  •  |  •  |  •  
          |     |     
"""

BOARD_DICT = {"Coordinate": ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"],
              "Symbol": ["•", "•", "•", "•", "•", "•", "•", "•", "•"],
              "Board Index": [52, 58, 64, 121, 127, 133, 190, 196, 202]}  # index del • nella stringa board


def winning_conditions():
    a = board_dict["Symbol"][:3]  # tutte le combo possibili per la vittoria
    b = board_dict["Symbol"][3:6]
    c = board_dict["Symbol"][6:9]
    d = board_dict["Symbol"][::3]
    e = board_dict["Symbol"][1::3]
    f = board_dict["Symbol"][2::3]
    g = board_dict["Symbol"][::4]
    h = board_dict["Symbol"][2:-2:2]
    check_list = [a, b, c, d, e, f, g, h]
    for combo in check_list:
        if set(combo) == {"X"}:  # set estrapola tutti i caratteri unici, se sono 3 X crea una lista con un elemento "X"
            print(board)
            print("You Won")
            return True
        elif set(combo) == {"O"}:
            print("AI Won...")
            return True
    return False


def keep_playing():
    play = input("Do you want to keep playing?Type 'Y' or 'N': ").upper()
    if play == "Y":
        reset_game_state()
        print(board)
        return True
    elif play == "N":
        print("Thanks for playing!!!")
        return False
    else:
        print("Wrong answer!")
        return keep_playing()


def ai_turn():
    global board
    o = random.choice(board_dict["Coordinate"])  # Sceglie la coordinata
    index = board_dict["Coordinate"].index(o)  # Individua l'index di quella coordinata nella lista delle coo
    if board_dict["Symbol"][index] == "•":  # Verifica che quella coo corrisponde a • e quindi libera
        board_dict["Symbol"][index] = "O"
        board_list = list(board)  # converto board a una lista per semplicità di scrittura
        board_list[board_dict["Board Index"][index]] = "O"  # individuo il • nella lista e lo cambio in O
        board = "".join(board_list)  # ricreo la stringa board
        print(f"AI move: {o}")
        print(board)
    else:
        ai_turn()  # nel caso la posizione non è libera


def player_turn():
    global board
    x = input("Select your position using the table coordinates (e.g.: 'a1') or type 'quit' to quit the game: ").lower()
    if x == "quit":
        print("Game Over")
        return False
    elif x in board_dict["Coordinate"]:  # Verifico che esiste
        index = board_dict["Coordinate"].index(x)
        if board_dict["Symbol"][index] == "•":  # Verifico che è libera come sopra
            board_dict["Symbol"][index] = "X"
            board_list = list(board)
            board_list[board_dict["Board Index"][index]] = "X"
            board = "".join(board_list)
            return True
        else:
            print("Already taken")
            return player_turn()
    else:
        print("Wrong coordinate")
        return player_turn()


def reset_game_state():
    global board, board_dict
    board = BOARD
    board_dict = deepcopy(BOARD_DICT)





def game():
    player_score = 0
    ai_score = 0
    reset_game_state()
    game_is_on = True
    print(board)
    while game_is_on:
        if not player_turn():  # player_turn ritorna falso quando viene scritto "quit"
            game_is_on = False
        else:
            if winning_conditions():
                player_score += 1
                score = f"Player {player_score} - {ai_score} AI"
                print(score)
                if not keep_playing():
                    game_is_on = False
                    print("Game Over")
            else:
                ai_turn()
                if winning_conditions():
                    ai_score += 1
                    score = f"Player {player_score} - {ai_score} AI"
                    print(score)
                    if not keep_playing():
                        game_is_on = False
                        print("Game Over")


print("-----WELCOME TO THE ULTIMATE TICTACTOE GAME-----")
game()




