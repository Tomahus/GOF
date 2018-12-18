from copy import deepcopy
import tkinter as tk
from itertools import product
import time
from statistics import mean
from random import randint

# Define methods


def init_world_array(p_rows, p_cols):

    array_world = [[0 for i in range(p_cols)] for j in range(p_rows)]

    return array_world


def draw_canvas_grid(p_canva, p_rows, p_cols, p_cell_size, p_id_list):

    for i in range(p_cols+1):
        p_canva.create_line(i * p_cell_size, 0, i * p_cell_size, p_rows * p_cell_size)

    for j in range(p_rows+1):
        p_canva.create_line(0, j * p_cell_size, p_cols * p_cell_size, j * p_cell_size)

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

    switch_cells = [
        (i,j)
        for i in range(len(buffer))
        for j in range(len(buffer[i]))
        if buffer[i][j] != p_id_list[i][j]
    ]

    return buffer, switch_cells


def draw_cells(p_id_list, p_canva, p_rect_list, p_swap_cells):

    for i,j in p_swap_cells:
        item = p_canva.gettags(p_rect_list[j + (i * len(p_id_list[0]))])
        if p_id_list[i][j] == 1:
            p_canva.itemconfigure(item, fill='blue')
        else:
            p_canva.itemconfigure(item, fill='white')


def next_generation_loop(p_id_list, p_canvas, p_rows, p_cols, p_cell_size,
                         p_ms, p_rect_list, p_runtime, p_next_generation):

    global stop_run
    if not stop_run:
        start = time.time()

        id_list, swap_cell = update(p_id_list)
        draw_cells(id_list, p_canvas, p_rect_list, swap_cell)
        p_next_generation.config(state="disabled")
        root.after(p_ms, next_generation_loop, id_list, p_canvas,
                   p_rows, p_cols, p_cell_size, p_ms, p_rect_list,
                   p_runtime, p_next_generation)

        end = time.time()
        p_runtime.append(end-start)

        # Generation count
        global generation_counter
        generation_counter += 1
        generation_var.set("Generation n° : {}".format(generation_counter))


def start_loop(p_id_list, p_canvas, p_rows, p_cols, p_cell_size, p_ms, p_rect_list, p_runtime, p_next_generation,
               p_rand_button):

    global stop_run
    stop_run = False
    p_rand_button.config(state="disabled")

    next_generation_loop(p_id_list, p_canvas, p_rows, p_cols, p_cell_size,p_ms, p_rect_list,
                         p_runtime, p_next_generation)


def stop_loop(p_start_button, p_rand_button):

    global stop_run
    stop_run = True
    p_start_button.config(state='normal')
    p_rand_button.config(state='normal')


def initiation(p_canva, p_rows, p_cols, p_cell_size):

    p_world_array = init_world_array(p_rows, p_cols)
    p_cells_list = draw_canvas_grid(p_canva, p_rows, p_cols, p_cell_size, p_world_array)
    p_swap_cells, p_world_array = built_templates(p_world_array)
    draw_cells(p_world_array, p_canva, p_cells_list, p_swap_cells)

    return p_world_array, p_cells_list


def built_templates(p_id_list):

    swap = [(10,y)
            for y in range(13,23)
            ]

    for pos in swap:
        p_id_list[pos[0]][pos[1]] = 1

    return swap, p_id_list


def populate_randomly(p_canva, p_id_list, p_cells):

    for i in range(len(p_id_list)):
        for j in range(len(p_id_list[i])):

            p_id_list[i][j] = randint(0,1)
            cell_index = (p_cells[j + (i * len(p_id_list[0]))])
            if p_id_list[i][j] == 1:
                p_canva.itemconfigure(cell_index, fill='blue')
            else:
                p_canva.itemconfigure(cell_index, fill='white')


# Define app parameters

root = tk.Tk()

canvas_width = 600
canvas_height = 600
window_width = 800
window_height = 800
cell_size = 10
rows = canvas_height // cell_size
cols = canvas_width // cell_size
refresh_rate = 50
global stop_run
stop_run = False
global generation_counter
generation_counter = 0
generation_var = tk.StringVar()
generation_var.set("Generation n° : {}".format(generation_counter))

# Optimisation time test
runtime = []

# Build the app

root.geometry("{}x{}".format(window_width, window_height))
app_canvas = tk.Canvas(root, bg="white")
app_canvas.config(width=canvas_width, height=canvas_height)
app_canvas.pack(side=tk.TOP)
buttons_frame = tk.Frame(root)
buttons_frame.pack(side=tk.TOP)
label_frame = tk.Frame(root)
label_frame.pack(side=tk.TOP)

# Logic

world_array, cells_list = initiation(app_canvas, rows, cols, cell_size)

# Control widgets

next_button = tk.Button(buttons_frame, text="Start", command=lambda:start_loop(world_array, app_canvas,
                                                                               rows, cols, cell_size,
                                                                               refresh_rate, cells_list,
                                                                               runtime, next_button,
                                                                               rand_button))


stop_button = tk.Button(buttons_frame, text="Stop", command=lambda:stop_loop(next_button, rand_button))
rand_button = tk.Button(buttons_frame, text='Random', command=lambda: populate_randomly(app_canvas, world_array,
                                                                                        cells_list))

next_button.pack(side=tk.LEFT)
stop_button.pack(side=tk.LEFT)
rand_button.pack(side=tk.LEFT)

generation_counter_label = tk.Label(label_frame, textvariable=generation_var)
generation_counter_label.pack(side=tk.TOP)

# App start point

root.mainloop()

# Optimisation time average calc

print("Average milliseconds :",mean(runtime)*1000)

