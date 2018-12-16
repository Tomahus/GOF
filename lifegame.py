from copy import deepcopy
import tkinter as tk
from itertools import product
import time

# Define methods


def init_world_array(p_rows=10, p_cols=10):

    array_world = [[0 for i in range(p_cols)] for j in range(p_rows)]

    return array_world


def draw_canvas_grid(p_canva, p_rows, p_cols, p_cell_size, p_id_list):

    for i in range(p_cols + 1):
        p_canva.create_line(i * p_cell_size, 0, i * p_cell_size, p_rows * p_cell_size)

    for i in range(p_rows + 1):
        p_canva.create_line(0, i * p_cell_size, p_cols * p_cell_size, i * p_cell_size)

    rect_list = [
        p_canva.create_rectangle(j * p_cell_size, i * p_cell_size,
                                 (j * p_cell_size) + p_cell_size,
                                 (i * p_cell_size) + p_cell_size,
                                 tags="{}".format(j+(i*len(p_id_list[0]))))
        for i in range(len(p_id_list)) for j in range(len(p_id_list[0]))
    ]

    return rect_list



def apply_rules(p_id_array, p_x, p_y):

    pos_list = [pos for pos in product((-1,1,0), repeat=2) if pos != (0,0)]
    neighbours = ([p_id_array[p_x + pos_x][p_y + pos_y]
                  for pos_x,pos_y in pos_list
                  if 0 <= (p_x + pos_x) < len(p_id_array)
                  and 0 <= (p_y + pos_y) < len(p_id_array[0])])

    neighbours_alives = sum(neighbours)
    cell_alive = p_id_array[p_x][p_y] == 1

    if cell_alive:
        if 1 < neighbours_alives < 4:
            return 1
    else:
        if 2 < neighbours_alives < 4:
            return 1

    return 0


def update(p_id_list):

    buffer = deepcopy(p_id_list)

    for i in range(len(p_id_list)):
        for j in range(len(p_id_list[i])):
            buffer[i][j] = apply_rules(p_id_list, i, j)

    swap_cells = [
        (i,j)
        for i in range(len(buffer))
        for j in range(len(buffer[i]))
        if buffer[i][j] != p_id_list[i][j]
    ]

    return buffer, swap_cells


def draw_cells(p_id_list, p_canva, p_rect_list, p_swap_cells):

    for i,j in p_swap_cells:
        item = p_canva.gettags(p_rect_list[j + (i * len(p_id_list[0]))])
        if p_id_list[i][j] == 1:
            p_canva.itemconfigure(item, fill='red')
        else:
            p_canva.itemconfigure(item, fill='white')


def next_generation_loop(p_id_list, p_canvas, p_rows, p_cols, p_cell_size, p_ms, p_rect_list, p_runtime):

    start = time.time()

    id_list, swap_cell = update(p_id_list)
    draw_cells(id_list, p_canvas, p_rect_list,swap_cell)
    root.after(p_ms, next_generation_loop, id_list, p_canvas,
               p_rows, p_cols, p_cell_size, p_ms, p_rect_list,
               p_runtime)

    end = time.time()
    p_runtime.append(end-start)


def built_templates(p_id_list):

    swap = [
        (10, 13),
        (10, 14),
        (10, 15),
        (10, 16),
        (10, 17),
        (10, 18),
        (10, 19),
        (10, 20),
        (10, 21),
        (10, 22)
    ]


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

    return swap, p_id_list


# Define app parameters

canvas_width = 600
canvas_height = 600
window_width = 800
window_height = 800
cell_size = 10
rows = canvas_height // cell_size
cols = canvas_width // cell_size
refresh_rate = 10

# Optimisation time test
runtime = []

# Build the app

root = tk.Tk()
root.geometry("{}x{}".format(window_width, window_height))
app_canvas = tk.Canvas(root, bg="white")
app_canvas.config(width=canvas_width, height=canvas_height)
app_canvas.pack()


# App's logic :

# - Build a 2D array with 0=dead or 1=alive for values --------- OK
# - Build a grid on canvas ------------------------------------- OK
# - Define rules for dead/alive -------------------------------- OK
# - Parse array buffered to apply rules ------------------------ OK
# - Erase Canvas ----------------------------------------------- OK
# - Define Draw method to parse array and draw cell if value = 1 - OK
# - Loop through : Update - Erase - Draw every xx milliseconds-- OK


world_array = init_world_array(rows, cols)
cells_list = draw_canvas_grid(app_canvas, rows, cols, cell_size, world_array)

swap_cells,world_array = built_templates(world_array)
draw_cells(world_array, app_canvas, cells_list, swap_cells)


""" Control widgets """

next_button = tk.Button(root, text="Start", command=lambda:next_generation_loop(world_array, app_canvas,
                                                                                rows, cols, cell_size,
                                                                                refresh_rate, cells_list,
                                                                                runtime))
next_button.pack()

""" App start point """
root.mainloop()


# Optimisation time average calc

average = sum(runtime)/len(runtime)
print("Average milliseconds :",average*1000)

