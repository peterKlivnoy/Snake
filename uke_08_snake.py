from textwrap import fill
from tkinter import font
from uib_inf100_graphics import *
import copy
from random import *
import math
import gspread

"""
gc = gspread.service_account(filename="creds.json")
sh = gc.open("scrapetosheets").sheet1
high_score = []
for i in range(1, 11):
    high_score.append(sh.row_values(i))

for i in range(1, 10):
    high_score[i][0] = int(high_score[i][0])

high_score.pop(0)
high_score.sort()
high_score.reverse()
print(high_score)
"""


def app_started(app):
    # Modellen.
    # Denne funksjonen kalles én gang ved programmets oppstart.
    # Her skal vi __opprette__ variabler i som behøves i app.
    app.gc = gspread.service_account(filename="creds.json")
    app.sh = app.gc.open("scrapetosheets").sheet1
    app.high_score = []
    for i in range(1, 12):
        app.high_score.append(app.sh.row_values(i))

    for i in range(1, 11):
        print(i)
        app.high_score[i][0] = int(app.high_score[i][0])

    app.high_score.pop(0)
    app.high_score.sort()
    app.high_score.reverse()

    app.char = "abcdefghijklmnopqrstuvwxyzæøå1234567890ABCDEFGHIJKLNMOPQRSTUVWXYZÆØÅ"
    app.player_name_list = []
    app.player_name = ""
    app.fruit_nr = 1
    app.board_nr = None
    app.head_pot = [[4, 3], [4, 5], [4, 7]]
    app.debug_mode = True
    app.head_pos = None
    app.snake_size = 3
    app.direction = "h"
    app.state = "start_screen"
    app.timer_delay = 150
    app.boards = [[
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
        [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
        [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]]
    app.start_buttons = [
        # [x1, y1, x2, y2, "Navn på knapp", funksjon]

    ]
    app.colours = ["red", "orange", "yellow",
                   "green", "blue", "indigo", "violet"]

    app.button_colors = ["lightgray", "gray"]
    app.button_color = ["lightgray", "lightgray",
                        "lightgray", "lightgray", "lightgray", "lightgray"]


def update(app):
    app.player_name = "".join(app.player_name_list)
    app.start_buttons = [
        # [x1, y1, x2, y2, "Navn på knapp", funksjon]

        [app.width*20/100, app.height*30/100, app.width-app.width*60 / \
            100, app.height-app.height*30/100, "9x7", set_board, 0, "lightgray", "start_screen"],
        [app.width*40/100, app.height*30/100, app.width-app.width*40/100,
            app.height-app.height*30/100, "12x10", set_board, 1, "lightgray", "start_screen"],
        [app.width*60/100, app.height*30/100, app.width-app.width*20/100,
            app.height-app.height*30/100, "15x13", set_board, 2, "lightgray", "start_screen"],

        [app.width*1/8, app.height*8/10, app.width*2/8,
            app.height, "1", set_fruit, 1, app.button_color[0], "start_screen"],
        [app.width*2/8, app.height*8/10, app.width*3/8,
            app.height, "2", set_fruit, 2, app.button_color[1], "start_screen"],
        [app.width*3/8, app.height*8/10, app.width*4/8,
            app.height, "3", set_fruit, 3, app.button_color[2], "start_screen"],
        [app.width*4/8, app.height*8/10, app.width*5/8,
            app.height, "4", set_fruit, 4, app.button_color[3], "start_screen"],
        [app.width*5/8, app.height*8/10, app.width*6/8,
            app.height, "5", set_fruit, 5, app.button_color[4], "start_screen"],
        [app.width*6/8, app.height*8/10, app.width*7/8,
            app.height, "Random", set_fruit, 6, app.button_color[5], "start_screen"]

    ]


def update_scoreboard(app):
    if app.snake_size> app.high_score[-1][0]:
        app.high_score.append([app.snake_size, app.player_name])
        app.high_score.sort()
        app.high_score.reverse()
        print(app.high_score)
        new_names = []
        new_scores = []
        for i in range(10):
            new_names.append(app.high_score[i][1])
            new_scores.append(app.high_score[i][0])
        for i in range(2, 12):
            app.sh.update(f'A{i}', new_scores[i-2])
            app.sh.update(f'b{i}', new_names[i-2])

def delete_all_fruit(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] < 0:
                grid[x][y] = 0


def set_fruit(app, n):
    for i in range(3):
        delete_all_fruit(app.boards[i])
        if n == 6:
            app.fruit_nr = randint(1, 5)
        else:
            app.fruit_nr = n
        for j in range(app.fruit_nr):
            add_apple_at_random_location(app.boards[i])
    for i in range(6):
        app.button_color[i] = "lightgrey"
        app.button_color[n-1] = "gray"


def set_board(app, n):
    app.board = copy.deepcopy(app.boards[n])
    app.head_pos = app.head_pot[n]
    app.state = "active"
    app.board_nr = n
    app.debug_mode = True


def point_in_rectangle(x1, y1, x2, y2, x, y):
    return (min(x1, x2) <= x <= max(x1, x2)
            and min(y1, y2) <= y <= max(y1, y2))


def execute_button_action_if_clicked(app, button, mouse_x, mouse_y):
    x1, y1, x2, y2, label, func, n, color, state = button
    if point_in_rectangle(x1, y1, x2, y2, mouse_x, mouse_y) and app.state == state:
        func(app, n)


def mouse_pressed(app, event):
    for button in app.start_buttons:
        execute_button_action_if_clicked(app, button, event.x, event.y)


def draw_button(canvas, button):
    x1, y1, x2, y2, label, func, n, color, state = button
    canvas.create_rectangle(x1, y1, x2, y2, fill=color)
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    canvas.create_text(mid_x, mid_y, text=label, fill="black")


def subtract_one_from_all_positives(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] > 0:
                grid[x][y] -= 1


def add_apple_at_random_location(grid):
    x = randint(0, len(grid[0])-1)
    y = randint(0, len(grid)-1)
    if grid[y][x] == 0:
        grid[y][x] = -1
    else:
        add_apple_at_random_location(grid)


def get_new_head(app):
    new_head = copy.deepcopy(app.head_pos)
    if app.direction == "v":
        new_head[0] -= 1
    elif app.direction == "h":
        new_head[0] += 1
    elif app.direction == "o":
        new_head[1] -= 1
    elif app.direction == "n":
        new_head[1] += 1
    return new_head


def is_legal_move(row, col, board):
    if row > len(board)-1:
        return False
    elif row < 0:
        return False
    elif col > len(board[0])-1:
        return False
    elif col < 0:
        return False
    elif board[row][col] > 0:
        return False
    else:
        return True


def move_snake(app):
    app.head_pos = get_new_head(app)
    if is_legal_move(app.head_pos[1], app.head_pos[0], app.board):
        if app.board[app.head_pos[1]][app.head_pos[0]] == -1:
            app.snake_size += 1
            add_apple_at_random_location(app.board)
        else:
            subtract_one_from_all_positives(app.board)

        app.board[app.head_pos[1]][app.head_pos[0]] = app.snake_size
    else:
        app.state = "game_over"


def timer_fired(app):
    # En kontroller.
    # Denne funksjonen kalles ca 10 ganger per sekund som standard.
    # Funksjonen kan __endre på__ eksisterende variabler i app.

    i = 0
    if i % 20 == 0:
        update(app)
    if not app.state == "game_over" and not app.debug_mode:
        move_snake(app)
    i += 1


def reset_game(app):
    update_scoreboard(app)
    app.snake_size = 3
    app.direction = "h"
    set_board(app, app.board_nr)


def key_pressed(app, event):
    # En kontroller.
    # Denne funksjonen kalles hver gang brukeren trykker på tastaturet.
    # Funksjonen kan __endre på__ eksisterende variabler i app.

    if event.key == "Escape":
        app.quit()
    if app.state == "active":
        if event.key == "m":
            app.debug_mode = not app.debug_mode
        if event.key == "Space":
            move_snake(app)
        elif event.key == "w" and app.direction != "n":
            app.direction = "o"
        elif event.key == "s" and app.direction != "o":
            app.direction = "n"
        elif event.key == "a" and app.direction != "h":
            app.direction = "v"
        elif event.key == "d" and app.direction != "v":
            app.direction = "h"
    elif app.state == "game_over":
        if event.key == "r":
            reset_game(app)
        elif event.key == "e":
            reset_game(app)
            app.state = "start_screen"
    elif app.state == "start_screen":
        if event.key in app.char:
            app.player_name_list.append(event.key)
        if event.key == "BackSpace" and len(app.player_name_list) > 0:
            app.player_name_list.pop()


def draw_scoreboard(app, canvas, x1, y1):
    width = (app.width*2/10)/2
    height = (app.height*5/10)/10

    canvas.create_rectangle(
        x1, y1-2*height, x1+2*width, y1, fill="grey", outline="white")
    canvas.create_text(x1+width, y1-height,
                       text="HighScore", anchor='center', fill="black", font=f'Times {math.floor(2*0.0266*app.height)} bold')

    for i in range(10):
        canvas.create_rectangle(
            x1, y1+height*i, x1+width, y1+height*(i+1), fill="grey", outline="white")
        canvas.create_rectangle(
            x1+width, y1+height*i, x1+width+width, y1+height*(i+1), fill="grey", outline="white")
        canvas.create_text(x1+width*(0.5), y1+height*(i+0.5),
                           text=app.high_score[i][1], anchor='center', fill="black", font=f'Times {math.floor(0.0266*app.height)} bold')
        canvas.create_text(x1+width*(1.5), y1+height*(i+0.5),
                           text=app.high_score[i][0], anchor='center', fill="black", font=f'Times {math.floor(0.0266*app.height)} bold')


def draw_board(app, canvas, x1, y1, x2, y2, board, debug_mode):

    nr_col = len(board[0])
    nr_row = len(board)
    width = (x2-x1)/nr_col
    height = (y2-y1)/nr_row
    for y in range(len(board)):
        for x in range(len(board[0])):

            if board[y][x] > 0:
                canvas.create_rectangle(x1+width*x, y1+height*y, x1 +
                                        width*(x+1), y1+height*(y+1), fill=app.colours[(app.snake_size-board[y][x]) % 7], outline="black")
            elif board[y][x] < 0:
                canvas.create_rectangle(x1+width*x, y1+height*y, x1 +
                                        width*(x+1), y1+height*(y+1), fill="cyan", outline="black")
            else:
                canvas.create_rectangle(x1+width*x, y1+height*y, x1 +
                                        width*(x+1), y1+height*(y+1), fill="lightgray", outline="black")
            if debug_mode:
                canvas.create_text(x1+width*(x+0.5), y1+height*(y+0.5),
                                   text=f'{x},{y}\n {board[y][x]}', anchor='center', fill="black", font='Times 12 bold')
    canvas.create_text(
        app.width*1/100, app.height*1/100, text=f"Score : {app.snake_size}", anchor="nw", fill="black", font=f"Times {math.floor(0.0266*app.height)} bold")


def redraw_all(app, canvas):
    if app.debug_mode:
        canvas.create_text(app.width/2, 15,
                           text=f'{app.head_pos=} {app.snake_size=} {app.direction=}', anchor='center', fill="black", font='Times 12 bold')
    if app.state == "active":

        draw_board(app, canvas, app.width*5/100, app.height*5/100, app.width-app.width*5/100,
                   app.height-app.height*5/100, app.board, app.debug_mode)
        if app.debug_mode:
            canvas.create_text(app.width/2, app.height/2,
                               text="Kontroller retning med -wasd- \n Bytt mellom debugmode med \"m\"", anchor="center", fill="black", font="Times 24 bold")

    elif app.state == "start_screen":
        canvas.create_text(app.width/2, app.height*1/6,
                           text=f"Navn: {app.player_name}", anchor="center", fill="black", font="Times 24 bold")
        for button in app.start_buttons:
            draw_button(canvas, button)
        draw_scoreboard(app, canvas, app.width*8/10, app.height*2/10)
    elif app.state == "game_over":
        canvas.create_text(app.width/2, app.height/2,
                           text=f"You Lost \n Score = {app.snake_size} \n Press \"r\" to play again \n Press \"E\" to go to homepage", anchor="center", fill="black", font='Times 20 bold')

    # Visningen.
    # Denne funksjonen tegner vinduet. Funksjonen kalles hver gang
    # modellen har endret seg, eller vinduet har forandret størrelse.
    # Funksjonen kan __lese__ variabler fra app, men har ikke lov til
    # å endre på dem.

    ...


run_app(width=500, height=400, title="Snake")
