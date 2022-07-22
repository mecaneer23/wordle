#!/usr/bin/env python3

import re
import json
from pathlib import Path

with open(f"{Path(__file__).parent}/words.json", "r") as f:
    words = json.load(f)

board = [[[] for _ in range(3)] for _ in range(5)]


class UserInputError(Exception):
    pass


class Solved(Exception):
    pass


def reorder(words):
    test_1 = []
    for i in "qjzxvkwyfbghmpduclsntoirae":
        for j in words[::-1]:
            if i in j:
                if j not in test_1:
                    test_1.append(j)
    test_2 = []
    for i in test_1:
        for j in range(5):
            if i.count(i[j]) != 1:
                test_2.insert(0, i)
                break
        else:
            test_2.append(i)
    return test_2


def make_regex(board):
    regex = ""
    for i in range(5):
        if board[i][2] != []:
            regex += board[i][2][0]
        else:
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


def get_remaining(word, status):
    if len(word) != 5 or len(status) != 5 or not status.isdigit() or not word.isalpha():
        raise UserInputError("Are you sure you entered the word and status correctly?")
    if status == "22222":
        raise Solved("You solved it!")
    for i in range(5):
        board[i][1] = []
    for i in range(5):
        if status[i] == "0":
            for j in board:
                if word[i] not in j[0]:
                    j[0].append(word[i])
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
    for i in range(5):
        for j in range(len(board[i][0])):
            if board[i][0][j] in board[i][1]:
                board[i][1].remove(board[i][0][j])
    remaining_words = []
    for i in words:
        if re.compile(make_regex(board)).match(i):
            remaining_words.append(i)
    for pattern in make_second_regex(board):
        temp = []
        for i in remaining_words:
            if re.compile(pattern).match(i):
                temp.append(i)
        remaining_words = temp.copy()
    return remaining_words


if __name__ == "__main__":
    print("Status: 0 for gray, 1 for yellow, 2 for green\nSolved: 22222")
    count = 1
    last_word = ""
    while True:
        try:
            output = reorder(
                get_remaining(input("Word: ") or last_word, input("Status: "))
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
