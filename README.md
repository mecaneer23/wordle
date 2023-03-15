# Wordle

## Overview

Wordle is a simple guessing game, similar to Mastermind. In Wordle, one has six attempts to guess the correct word. Every attempt, another player (or a computer) will provide information about the correctness of a given input.

This repository provides both a [wordle game](game.py), and [wordle solver(s)](solver.py).

Multiple gui versions are also supported:

- In [terminal](solver.py) (as previously mentioned)
- In a [Tkinter window](tk_gui.py) (or [custom themed version](ctk_gui.py))
- In the browser (using a [JavaScript implementation](index.html))
- In the browser (using a [Python implementation](eel_gui.py) (eel.py))

There is also a [node.js solver](solver.js) for the terminal.

Every solver uses the same [words.json](words.json) file to source the possible words.

## Playing the game

Enter `python3 game.py` into a terminal. Optionally, include a word which a friend will attempt to guess. If no word is provided, the game will randomly choose one from words.json.

Once the game has started, enter five-letter words one at a time. As you enter them, the game will tell you if each letter is in the right spot (highlighted green), in the word but in the incorrect spot (highlighted yellow), or not in the word at all. You have six tries to use this information to determine the correct word.

### Examples

#### Providing a word

`python3 game.py hello`

#### Randomly generating a word

`python3 game.py`

### Bugs

If a given letter appears only one time in the word, but you enter it multiple times in a guess, the game will highlight both letters without regard to the other.

## Using the solver

This solver should be used simultaneously while playing a wordle game.
Enter `python3 solver.py` into a terminal. One at a time, enter guessed words into the solver. Once you have entered the same word into the game, relay the information to the solver, where green is 2, yellow is 1, and gray is 0. The solver will calculate all possible remaining words and provide a list, ordered by theoretically most likely to least likely.
