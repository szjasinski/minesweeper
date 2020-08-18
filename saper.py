from tkinter import *
import random
import time

root = Tk()
root.title('SAPER')

my_frame = Frame(root, width=500, height=500, bg="yellow")
my_frame.pack(fill=BOTH, expand=1)

n = 10
bombs_number = 10

coords_button_dict = {}
coords_number_dict = {}
bomb_list = []
revealed_squares_list = []
locally_revealed_list = []
count_reveal_blank_fields = 0
win_dict = {}


def do_nothing():
    pass


def reset_board():
    global coords_button_dict
    global coords_number_dict
    global bomb_list
    global revealed_squares_list
    global locally_revealed_list
    global count_reveal_blank_fields
    global win_dict

    coords_button_dict.clear()
    coords_number_dict.clear()
    bomb_list.clear()
    revealed_squares_list.clear()
    locally_revealed_list.clear()
    win_dict.clear()
    count_reveal_blank_fields = 0

    for widget in my_frame.winfo_children():
        widget.destroy()

    construct_buttons()
    generate_bombs()
    generate_numbers()


def popup_click():
    reset_board()
    top.destroy()


def popup(endgame):
    global top
    top = Toplevel()
    top.title('END GAME')

    if endgame == "lost":
        Label(top, text=" You lost. ", font=("Helvetica", 20), padx=30, pady=30).pack()
    else:
        Label(top, text=" You won. ", font=("Helvetica", 20), padx=30, pady=30).pack()

    Button(top, text="reset game", command=popup_click).pack()

    # disable buttons after popup
    for coords in coords_button_dict:
        coords_button_dict[coords].config(command=do_nothing)

    show_bombs()


def list_squares_around(x, y):
    squares_around = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                      (x + 1, y - 1), (x + 1, y), (x + 1, y + 1),
                      (x, y - 1), (x, y + 1)]
    output_list = []
    for coords in squares_around:
        if coords in coords_button_dict:
            output_list.append(coords)

    return output_list


def num_bombs_around(x, y):
    squares_around = list_squares_around(x, y)

    output = 0
    for coords in bomb_list:
        if coords in squares_around:
            output += 1

    return output


def reveal_empty_locally(x, y):
    global locally_revealed_list

    squares_around = list_squares_around(x, y)

    if (x, y) not in locally_revealed_list:
        if coords_number_dict[(x, y)] == 0:
            locally_revealed_list.append((x, y))
            coords_button_dict[(x, y)].config(highlightbackground="grey")
            win_dict[(x, y)] = 1
    for elem in squares_around:
        if elem not in locally_revealed_list:
            if coords_number_dict[(x, y)] == 0:
                reveal_empty_locally(elem[0], elem[1])


def reveal_numbers_locally(my_list):
    for elem in my_list:
        squares_around = list_squares_around(elem[0], elem[1])
        for coords in squares_around:
            if coords_number_dict[coords] != 0:
                coords_button_dict[coords].config(text=num_bombs_around(coords[0], coords[1]), highlightbackground="grey")
                win_dict[coords[0], coords[1]] = 1


def win_check():
    count = 0
    for coords in win_dict:
        if win_dict[coords] == 1:
            count += 1
    if count == n*n-bombs_number:
        popup("win")
    print(count)


def generate_bombs():
    global bomb_list

    while len(bomb_list) != bombs_number:
        # randint = random integer N such that a <= N <= b.
        bomb_id = (random.randint(0, n - 1), random.randint(0, n - 1))
        if bomb_id not in bomb_list:
            bomb_list.append(bomb_id)


def show_bombs():
    for button_coords in coords_button_dict:
        if button_coords in bomb_list:
            coords_button_dict[button_coords].config(text="x")


def generate_numbers():
    global coords_number_dict
    global win_dict

    coords_number_dict = coords_button_dict.copy()
    for coords in coords_number_dict:
        coords_number_dict[coords] = num_bombs_around(coords[0], coords[1])

    # create win dictionary
    win_dict = coords_number_dict.copy()
    for coords in win_dict:
        win_dict[coords] = 0


def show_numbers():
    for coords in coords_number_dict:
        if coords not in bomb_list:
            coords_button_dict[coords].config(text=num_bombs_around(coords[0], coords[1]))


def my_click(x, y):
    global coords_button_dict
    global win_dict

    for coords in coords_button_dict:
        if coords[0] == x and coords[1] == y:
            if coords in bomb_list:
                coords_button_dict[coords].config(text="!!", highlightbackground="red")
                popup("lost")
            elif coords_number_dict[coords] == 0:
                coords_button_dict[coords].config(command=do_nothing)
            else:
                coords_button_dict[coords].config(text=num_bombs_around(x, y), highlightbackground="grey")
                win_dict[(x, y)] = 1


    # reveal_blank_fields(x, y)
    # show_numbers()
    if (x, y) not in bomb_list:
        reveal_empty_locally(x, y)
        reveal_numbers_locally(locally_revealed_list)

    win_check()


def construct_buttons():
    grid_count = 0
    for x in range(0, n):
        for y in range(0, n):
            btn = Button(my_frame, text="  ", font=("Helvetica", 32), padx=10, pady=2, highlightbackground="yellow",
                         command=lambda row_n=x, column_n=y: my_click(row_n, column_n))
            coords_button_dict[(x, y)] = btn
            coords_button_dict[(x, y)].grid(row=x, column=y)
            grid_count += 1


construct_buttons()
generate_bombs()
generate_numbers()




root.mainloop()
