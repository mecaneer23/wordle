#!/usr/bin/env python3

import eel
import solver

eel.init("eel_gui")

board = solver.init_board()

@eel.expose
def solve(word, status):
    global board
    remaining, board = solver.get_words_board_wrapper(
        word, status, board
    )
    return remaining[::-1]

@eel.expose
class UserInputError(solver.UserInputError):
    pass

@eel.expose
class Solved(solver.Solved):
    pass

eel.start("index.html", size=(350, 400))