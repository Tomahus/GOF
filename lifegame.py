from copy import deepcopy
from tkinter import *

""" Define methods """


def init_world_array(p_rows=10, p_cols=10):

    array_world = [[0 for i in range(p_cols)] for j in range(p_rows)]
    return array_world


def draw_canvas_grid(p_canva, p_rows=10, p_cols=10, p_cell_size=20):

    for i in range(p_cols + 1):
        p_canva.create_line(i * p_cell_size, 0, i * p_cell_size, p_rows * p_cell_size)

    for i in range(p_rows + 1):
        p_canva.create_line(0, i * p_cell_size, p_cols * p_cell_size, i * p_cell_size)


def apply_rules(p_id_array, p_x, p_y):

    try:
        cell_n = p_id_array[p_x-1][p_y]         # North cell
    except IndexError:
        cell_n = None
    try:
        cell_w = p_id_array[p_x][p_y-1]         # West cell
    except IndexError:
        cell_w = None
    try:
        cell_s = p_id_array[p_x+1][p_y]         # South cell
    except IndexError:
        cell_s = None
    try:
        cell_e = p_id_array[p_x][p_y+1]         # East cell
    except IndexError:
        cell_e = None
    try:
        cell_nw = p_id_array[p_x-1][p_y-1]      # North-West cell
    except IndexError:
        cell_nw = None
    try:
        cell_ne = p_id_array[p_x-1][p_y+1]      # North-East cell
    except IndexError:
        cell_ne = None
    try:
        cell_sw = p_id_array[p_x+1][p_y-1]      # South-West cell
    except IndexError:
        cell_sw = None
    try:
        cell_se = p_id_array[p_x+1][p_y+1]      # South-East cell
    except IndexError:
        cell_se = None

    neighbours_list = (cell_n, cell_e, cell_w, cell_s, cell_nw, cell_ne, cell_se, cell_sw)
    alives = 0

    for element in neighbours_list:
        if element == 1:
            alives += 1
        else:
            pass

    if p_id_array[p_x][p_y] == 1:
        if alives == 3 or alives == 2:
            return 1
        else:
            return 0
    else:
        if alives == 3:
            return 1
        else:
            return 0


def update(p_id_list):

    buffer = deepcopy(p_id_list)

    for i in range(len(p_id_list)):
        for j in range(len(p_id_list[i])):
            buffer[i][j] = apply_rules(p_id_list, i, j)

    p_id_list = deepcopy(buffer)

    return p_id_list


def draw_cells(p_id_list, p_canvas, p_rows, p_cols, p_cell_size):

    p_canvas.delete("all")
    draw_canvas_grid(p_canvas, p_rows, p_cols, p_cell_size)

    for i in range(len(p_id_list)):
        for j in range(len(p_id_list[i])):

            if p_id_list[i][j] == 1:
                p_canvas.create_rectangle(j * p_cell_size, i * p_cell_size,
                                         (j * p_cell_size) + p_cell_size,
                                         (i * p_cell_size) + p_cell_size, fill="black")


def next_generation_loop(p_id_list, p_canvas, p_rows, p_cols, p_cell_size, p_ms):

    id_list = update(p_id_list)
    draw_cells(id_list, p_canvas, p_rows, p_cols, p_cell_size)
    root.after(p_ms, next_generation_loop, id_list, p_canvas, p_rows, p_cols, p_cell_size, p_ms)


def builded_templates(p_id_list, p_template):

    if p_template == 1:
        p_id_list[3][3] = 1
        p_id_list[4][4] = 1
        p_id_list[5][2] = 1
        p_id_list[5][4] = 1
        p_id_list[5][2] = 1
        p_id_list[5][3] = 1

    elif p_template == 2:
        p_id_list[10][13] = 1
        p_id_list[10][14] = 1
        p_id_list[10][15] = 1
        p_id_list[10][16] = 1
        p_id_list[10][17] = 1
        p_id_list[10][18] = 1
        p_id_list[10][19] = 1
        p_id_list[10][20] = 1
        p_id_list[10][21] = 1
        p_id_list[10][22] = 1

    return p_id_list


""" Define app parameters """

canvas_width = 600
canvas_height = 600
window_width = 800
window_height = 800
cell_size = 10
rows = int(canvas_height / cell_size)
cols = int(canvas_width/cell_size)
refresh_rate = 50

""" Build the app """

root = Tk()
root.geometry(str(window_width)+"x"+str(window_height))
app_canvas = Canvas(root, bg="white")
app_canvas.config(width=canvas_width, height=canvas_height)
app_canvas.pack()


""" App's logic :

- Build a 2D array with 0=dead or 1=alive for values --------- OK
- Build a grid on canvas ------------------------------------- OK
- Define rules for dead/alive -------------------------------- OK
- Parse array buffered to apply rules ------------------------ OK
- Array = buffer --------------------------------------------- OK
- Erase Canvas ----------------------------------------------- OK
- Define Draw method to parse array and draw cell if value=1 - OK
- Loop through : Update - Erase - Draw every xx milliseconds-- OK

"""

world_array = init_world_array(rows, cols)
draw_canvas_grid(app_canvas, rows, cols, cell_size)

world_array = builded_templates(world_array, 2)
draw_cells(world_array, app_canvas, rows, cols, cell_size)


""" Control widgets """

next_button = Button(root, text="Start", command=lambda:next_generation_loop(world_array, app_canvas,
                                                                             rows, cols, cell_size,
                                                                             refresh_rate))
next_button.pack()

""" App start point """
root.mainloop()
