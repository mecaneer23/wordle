#!/usr/bin/env node

const fs = require('fs');
const readline = require('readline-sync');

const words = JSON.parse(fs.readFileSync("words.json"));

let board = [[[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []]];

class UserInputError extends Error {
    constructor(message) {
        super(message);
        this.name = 'UserInputError';
    }
}

class Solved extends Error {
    constructor(message) {
        super(message);
        this.name = 'Solved';
    }
}

function reorder(words) {
    let test_1 = [];
    for (i of "qjzxvkwyfbghmpduclsntoirae") {
        for (j of words.reverse()) {
            if (j.includes(i)) {
                if (!test_1.includes(j)) {
                    test_1.push(j);
                }
            }
        }
    }
    let test_2 = [];
    for (i of test_1) {
        var flag = false;
        for (j = 0; j < 5; j++) {
            for (count = -1, index = -2; index != -1; count++, index = i.indexOf(i[j], index + 1));
            if (count != 1) {
                test_2.unshift(i);
                flag = true;
                break;
            }
        }
        if (!flag) {
            test_2.push(i);
        }
    }
    return test_2;
}

function make_regex(board) {
    let regex = "";
    for (var i = 0; i < 5; i++) {
        if (board[i][2].length != 0) {
            regex += board[i][2][0];
        } else {
            regex += "[^";
            for (j of board[i][0]) {
                regex += j;
            }
            regex += "]";
        }
    }
    return regex;
}

function make_second_regex(board) {
    let output = [];
    for (i = 0; i < 5; i++) {
        for (j of board[i][1]) {
            if (!(j in output)) {
                output.push(`.*${j}.*`);
            }
        }
    }
    return output;
}

function is_alpha(string) {
    return /^[a-zA-Z]+$/.test(string);
}

function is_digit(string) {
    return /^[0-9]+$/.test(string);
}

function get_remaining(word, status) {
    if (
        word.length != 5 ||
        status.length != 5 ||
        !is_alpha(word) ||
        !is_digit(status)
    ) {
        throw new UserInputError("Invalid input");
    }
    if (status == "22222") {
        throw new Solved("You solved it!");
    }
    for (i = 0; i < 5; i++) {
        board[i][1] = [];
    }
    for (i = 0; i < 5; i++) {
        if (status[i] == "0") {
            for (j of board) {
                if (!(word[i] in j[0])) {
                    j[0].push(word[i]);
                }
            }
        } else if (status[i] == "1") {
            for (j = 0; j < 5; j++) {
                if (j == i) {
                    if (!(word[i] in board[i][0])) {
                        board[i][0].push(word[i]);
                    }
                } else {
                    if (!(word[i] in board[j][1])) {
                        board[j][1].push(word[i]);
                    }
                }
            }
        } else if (status[i] == "2") {
            if (!(word[i] in board[i][2])) {
                board[i][2].push(word[i]);
            }
        }
    }
    for (i = 0; i < 5; i++) {
        for (j = 0; j < board[i][0].length; j++) {
            if (board[i][0][j] in board[i][1]) {
                board[i][1].remove(board[i][0][j]);
            }
        }
    }
    let remaining_words = [];
    for (i of words) {
        if (new RegExp(make_regex(board)).test(i)) {
            remaining_words.push(i);
        }
    }
    for (pattern of make_second_regex(board)) {
        let temp = [];
        for (i of remaining_words) {
            if (i.match(new RegExp(pattern)) != null) {
                temp.push(i);
            }
        }
        remaining_words = Array.from(temp);
    }
    return remaining_words;
}

function input(string) {
    return readline.question(string);
}

function main() {
    console.log("Status: 0 for gray, 1 for yellow, 2 for green\nSolved: 22222");
    let count = 1;
    let last_word = "";
    let output = [];
    while (true) {
        try {
            output = reorder(get_remaining(input("Word: ") || last_word, input("Status: ")));
        } catch (e) {
            if (e instanceof UserInputError) {
                console.log(e.message);
                continue;
            } else if (e instanceof Solved) {
                console.log(e.message);
                break;
            } else {
                throw e;
            }
        }
        if (output.length == 0) {
            console.log("No words left");
            break;
        }
        last_word = output.length > 0 ? output[output.length-1] : "";
        output.slice(0, -1).forEach(element => {
            console.log(element);
        });
        console.log();
        console.log(last_word);
        console.log(output.length);
        count++;
    }
    console.log(`${count} words entered`);
}

main()