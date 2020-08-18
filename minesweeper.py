import tkinter as tk
import random


# TO DO: pictures, popup in another class, "cant lose in first move" feature, make code less spaghetti-like


class Minesweeper(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        my_frame = tk.Frame(parent)

        n = 10
        bombs_number = 10

        coords_button_dict = {}
        coords_number_dict = {}
        bomb_list = []
        revealed_squares_list = []
        locally_revealed_list = []
        count_reveal_blank_fields = 0
        win_dict = {}
        top = tk.Toplevel()

        def do_nothing():
            pass

        def reset_board():
            nonlocal coords_button_dict
            nonlocal coords_number_dict
            nonlocal bomb_list
            nonlocal revealed_squares_list
            nonlocal locally_revealed_list
            nonlocal count_reveal_blank_fields
            nonlocal win_dict

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
            nonlocal top
            top = tk.Toplevel()
            top.title('END GAME')

            if endgame == "lost":
                tk.Label(top, text=" You lost. ", font=("Helvetica", 20), padx=30, pady=30).pack()
            else:
                tk.Label(top, text=" You won. ", font=("Helvetica", 20), padx=30, pady=30).pack()

            tk.Button(top, text="reset game", command=popup_click).pack()

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
                        coords_button_dict[coords].config(text=num_bombs_around(coords[0], coords[1]),
                                                          highlightbackground="grey")
                        win_dict[coords[0], coords[1]] = 1

        def win_check():
            count = 0
            for coords in win_dict:
                if win_dict[coords] == 1:
                    count += 1
            if count == n * n - bombs_number:
                popup("win")
            print(count)

        def generate_bombs():
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
            nonlocal coords_number_dict
            nonlocal win_dict

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
                    btn = tk.Button(my_frame, text="  ", font=("Helvetica", 32), padx=10, pady=2,
                                    highlightbackground="yellow",
                                    command=lambda row_n=x, column_n=y: my_click(row_n, column_n))
                    coords_button_dict[(x, y)] = btn
                    coords_button_dict[(x, y)].grid(row=x, column=y)
                    grid_count += 1

        construct_buttons()
        generate_bombs()
        generate_numbers()

        my_frame.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('MINESWEEPER')
    Minesweeper(root).pack()
    root.mainloop()
