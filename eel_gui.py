#!/usr/bin/env python3

import eel
import solver

eel.init("eel_gui")

@eel.expose
def solve(word, status):
    return solver.reorder(solver.get_remaining(word, status))[::-1]

@eel.expose
class UserInputError(solver.UserInputError):
    pass

@eel.expose
class Solved(solver.Solved):
    pass

eel.start("index.html", size=(350, 400))