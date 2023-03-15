#!/usr/bin/env python3

import re
import json
from pathlib import Path


class UserInputError(Exception):
    pass


class Solved(Exception):
    pass


def _reorder_by_letter(words):
    output = []
    for i in "qjzxvkwyfbghmpduclsntoirae":
        for j in words[::-1]:
            if i in j and j not in output:
                output.append(j)
    return output


def _reorder_by_occurrences(words):
    output = []
    for i in words:
        for j in range(5):
            if i.count(i[j]) != 1:
                output.insert(0, i)
                break
        else:
            output.append(i)
    return output


def reorder(words, board):
    return _reorder_by_occurrences(_reorder_by_letter(words)), board


def make_regex(board):
    regex = ""
    for i in range(5):
        if board[i][2] != []:
            regex += board[i][2][0]
            continue
        regex += "[^"
        for j in board[i][0]:
            regex += j
        regex += "]"
    return regex


def make_second_regex(board):
    output = []
    for i in range(5):
        for j in board[i][1]:
            if j not in output:
                output.append(j)
    return [f".*{i}.*" for i in output]


def zero_maybes(board):
    for i in range(5):
        board[i][1] = []
    return board


def remove_nos_from_maybes(board):
    for i in range(5):
        letter = board[i]
        for j in range(len(letter[0])):
            if letter[0][j] in letter[1]:
                letter[1].remove(letter[0][j])
    return board


def guard_inputs(word, status):
    if len(word) != 5 or len(status) != 5 or not status.isdigit() or not word.isalpha():
        raise UserInputError("Are you sure you entered the word and status correctly?")
    for i in status:
        if i not in "012":
            raise UserInputError("Status must be just (0, 1, 2)")
    if status == "22222":
        raise Solved("You solved it!")
    return word, status


def add_to_board(word, status, board):
    for i in range(5):
        if status[i] == "0":
            for letter in board:
                if word[i] not in letter[0]:
                    letter[0].append(word[i])
        elif status[i] == "1":
            for j in range(5):
                if j == i:
                    if word[i] not in board[i][0]:
                        board[i][0].append(word[i])
                else:
                    if word[i] not in board[j][1]:
                        board[j][1].append(word[i])
        elif status[i] == "2":
            if word[i] not in board[i][2]:
                board[i][2].append(word[i])
    return board


def get_remaining(words, board):
    remaining_words = []
    first_regex = re.compile(make_regex(board))
    for i in words:
        if first_regex.match(i):
            remaining_words.append(i)
    for pattern in make_second_regex(board):
        temp = []
        second_regex = re.compile(pattern)
        for word in remaining_words:
            if second_regex.match(word):
                temp.append(word)
        remaining_words = temp.copy()
    return remaining_words, board


def init_board():
    return [
        [[] for _ in range(3)] for _ in range(5)
    ]  # [no, yes, maybe] for letter in range(5)


def init_words_list():
    with open(f"{Path(__file__).parent}/words.json", "r") as f:
        return json.load(f)


def get_words_board_wrapper(word, status, board=init_board()):
    """wraps many functions defined to make running much simpler

    Args:
        word (str): a word to test
        status (str): a string representation of an input status (consists of 0, 1, 2)
        board (list of lists - board object): this is the current status of the entire board so far. If no board is provided, it will default to a blank board

    Returns:
        words (list): ordered list of possible remaining words given the inputs
        board: the input board so this function can be called in a loop
    """
    return reorder(
        *get_remaining(
            init_words_list(),
            remove_nos_from_maybes(
                add_to_board(
                    *guard_inputs(word.lower(), status),
                    zero_maybes(board),
                ),
            ),
        )
    )


if __name__ == "__main__":
    print("Status: 0 for gray, 1 for yellow, 2 for green\nSolved: 22222")
    count = 1
    last_word = ""
    board = init_board()

    while True:
        try:
            output, board = get_words_board_wrapper(
                input("Word: ") or last_word, input("Status: "), board
            )
        except UserInputError as e:
            print(e)
            continue
        except Solved as e:
            print(e)
            break
        if len(output) == 0:
            print("No words left")
            break
        last_word = output[-1] if output else ""
        print("\n".join(output[:-1]), f"\n{last_word}", len(output), sep="\n")
        count += 1
    print(f"{count} words entered")
