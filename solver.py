#!/usr/bin/env python3

import re
import json

with open("words.json", "r") as f:
    words = json.load(f)
print("Status: 0 for gray, 1 for yellow, 2 for green\nSolved: 22222")

wordle_status = [[[] for _ in range(3)] for _ in range(5)]


def make_regex(wordle_status):
    regex = ""
    for i in range(5):
        if wordle_status[i][2] != []:
            regex += wordle_status[i][2][0]
        else:
            # if wordle_status[i][1] != []:
            #     regex += "(["
            #     for j in wordle_status[i][1]:
            #         regex += j
            #     regex += "])"
            # else:
                regex += "("
            # if wordle_status[i][0] != []:
                regex += "[^"
                for j in wordle_status[i][0]:
                    regex += j
                regex += "])"
    return regex


def make_second_regex(wordle_status):
    output = []
    for i in range(5):
        for j in wordle_status[i][1]:
            if j not in output:
                output.append(j)
    for i in range(len(output)):
        output[i] = f".*{output[i]}.*"
    return output


solved = False
while not solved:
    for i in range(5):
        wordle_status[i][1] = []
    word = input("Enter a word: ")
    status = input("Enter a status: ")
    if len(word) != 5 or len(status) != 5 or not status.isdigit():
        print("Are you sure you entered the word right?")
        continue
    if status == "22222":
        solved = True
        print("You solved it!")
        continue
    for i in range(5):
        if status[i] == "0":
            for j in wordle_status:
                if word[i] not in j[0]:
                    j[0].append(word[i])
        elif status[i] == "1":
            for j in range(5):
                if j != i:
                    if word[i] not in wordle_status[j][1]:
                        wordle_status[j][1].append(word[i])
                else:
                    if word[i] not in wordle_status[i][0]:
                        wordle_status[i][0].append(word[i])
        elif status[i] == "2":
            if word[i] not in wordle_status[i][2]:
                wordle_status[i][2].append(word[i])
    for i in range(5):
        for j in range(len(wordle_status[i])):
            if wordle_status[i][0][j] in wordle_status[i][1]:
                wordle_status[i][1].remove(wordle_status[i][0][j])
    remaining_words = []
    temp = []
    for i in words[::-1]:
        if re.compile(make_regex(wordle_status)).match(i):
            remaining_words.append(i)
    for pattern in make_second_regex(wordle_status):
        for i in remaining_words:
            if re.compile(pattern).match(i):
                temp.append(i)
        remaining_words = temp
        temp = []
    for i in remaining_words:
        print(i)
    print(len(remaining_words))
