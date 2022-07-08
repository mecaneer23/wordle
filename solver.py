#!/usr/bin/env python3

import re
import json
import os

with open("words.json", "r") as f:
    words = json.load(f)
print("Status: 0 for gray, 1 for yellow, 2 for green\nSolved: 22222")

wordle_status = [[[], []], [[], []], [[], []], [[], []], [[], []]]


def make_regex(wordle_status):
    regex = ""
    for i in range(5):
        if wordle_status[i][1] != []:
            regex += wordle_status[i][1][0]
        else:
            regex += "[^"
            for j in wordle_status[i][0]:
                regex += j
            regex += "]"
    return re.compile(regex)


def horizontal_print(items):
    max_cols = os.get_terminal_size().columns
    for i in range(len(items)%max_cols):
        print(items[i])

solved = False
while not solved:
    word = input("Enter a word: ")
    status = input("Enter a status: ")
    if len(word) != 5 or len(status) != 5 or not status.isdigit():
        print("Are you sure you entered the word right?")
        continue
    for i in range(5):
        if status[i] == "0":
            for j in wordle_status:
                j[0].append(word[i])
        elif status[i] == "1":
            for j in range(5):
                if j != i:
                    wordle_status[i][0].append(word[i])
        elif status[i] == "2":
            wordle_status[i][1].append(word[i])
    counter = 0
    # lst = []
    for i in words[::-1]:
        if make_regex(wordle_status).match(i):
            print(i)
            # lst.append(i)
            counter += 1
    # horizontal_print(lst)
    print(counter)
    # print(wordle_status)
    # print(make_regex(wordle_status))
