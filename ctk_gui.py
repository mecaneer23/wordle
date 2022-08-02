#!/usr/bin/env python3

from tkinter import Text
from customtkinter import ( # https://github.com/TomSchimansky/CustomTkinter
    set_appearance_mode,
    CTk,
    StringVar,
    CTkLabel,
    CTkEntry,
    CTkButton,
    CTkScrollbar,
)
import solver


def main():
    board = solver.board  # used by get_remaining

    def populate_board(event=None):
        try:
            remaining = solver.reorder(solver.get_remaining(word.get(), status.get()))[
                ::-1
            ]
        except solver.UserInputError as e:
            len_remaining.set(e)
            word.set("")
            status.set("")
        except solver.Solved as e:
            print(e)
            root.destroy()
            return
        else:
            word.set("")
            status.set("")
            remaining_output.configure(state="normal")
            remaining_output.delete("1.0", "end")
            remaining_output.insert("1.0", "\n".join(remaining))
            remaining_output.configure(state="disabled")
            len_remaining.set(len(remaining))
        entry.focus()

    root = CTk()
    set_appearance_mode("dark")
    root.title("Wordle Solver")
    root.geometry("300x350")
    word = StringVar()
    status = StringVar()
    len_remaining = StringVar()
    CTkLabel(
        root, text="Status: 0 for gray, 1 for yellow, 2 for green\nSolved: 22222"
    ).grid(row=0, columnspan=2)
    remaining_output = Text(
        root,
        width=20,
        height=10,
        state="disabled",
        background="#212325",
        foreground="#DCE4EE",
    )
    remaining_output.grid(row=1, columnspan=3, sticky="nsew")
    sbar = CTkScrollbar(root, command=remaining_output.yview)
    sbar.grid(row=1, column=3, sticky="ns")
    remaining_output.configure(yscrollcommand=sbar.set)
    CTkLabel(root, textvariable=len_remaining).grid(row=2, columnspan=2)
    CTkLabel(root, text="Enter a word:").grid(row=3, column=0)
    entry = CTkEntry(root, textvariable=word)
    entry.grid(row=3, column=1)
    entry.focus()
    CTkLabel(root, text="Enter a status:").grid(row=4, column=0)
    CTkEntry(root, textvariable=status).grid(row=4, column=1)
    CTkButton(root, command=populate_board, text="Submit").grid(row=5, columnspan=2)
    root.bind("<Return>", populate_board)
    root.mainloop()


if __name__ == "__main__":
    main()
