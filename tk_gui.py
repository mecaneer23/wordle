#!/usr/bin/env python3

from tkinter import Tk, ttk, StringVar, scrolledtext
import solver

def main():
    board = solver.board
    def populate_board(event=None):
        try:
            remaining = solver.get_remaining(word.get(), status.get())
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
    root = Tk()
    root.title("Wordle Solver")
    word = StringVar()
    status = StringVar()
    len_remaining = StringVar()
    ttk.Label(root, text="Status: 0 for gray, 1 for yellow, 2 for green\nSolved: 22222").grid(row=0, columnspan=2)
    remaining_output = scrolledtext.ScrolledText(root, width=20, height=10)
    remaining_output.grid(row=1, columnspan=3)
    remaining_output.configure(state="disabled")
    ttk.Label(root, textvariable=len_remaining).grid(row=2, columnspan=2)
    ttk.Label(root, text="Enter a word:").grid(row=3, column=0)
    entry = ttk.Entry(root, textvariable=word)
    entry.grid(row=3, column=1)
    entry.focus()
    ttk.Label(root, text="Enter a status:").grid(row=4, column=0)
    ttk.Entry(root, textvariable=status).grid(row=4, column=1)
    ttk.Button(root, command=populate_board, text="Submit").grid(row=5, columnspan=2)
    root.bind("<Return>", populate_board)
    root.mainloop()


if __name__ == "__main__":
    main()