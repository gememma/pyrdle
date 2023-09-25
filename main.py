import os
import random

import rich
from rich.console import Console
from rich.prompt import Prompt

emojis = {
    'correct_place': '🟩',
    'correct_letter': '🟨',
    'incorrect': '⬜'
}


def correct_place(letter):
    return f'[black on green]{letter}[/]'


def correct_letter(letter):
    return f'[black on yellow]{letter}[/]'


def incorrect(letter):
    return f'[black on white]{letter}[/]'


def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size
    random_point = random.randint(0, total_bytes)
    file = open(file_name)
    file.seek(random_point)
    file.readline()  # skip this line to clear the partial line
    line = file.readline()
    if len(line) == 0:
        # read first line
        file.seek(0)
        return file.readline()
    else:
        return line


def score_guess(guess, answer):
    scored = []
    emojied = []
    seen = []
    for i, letter in enumerate(guess):
        if answer[i] == guess[i]:
            scored += correct_place(letter)
            emojied.append(emojis['correct_place'])
            seen += letter
        elif letter in answer:
            if letter in seen:
                scored += incorrect(letter)
                emojied.append(emojis['incorrect'])
            else:
                scored += correct_letter(letter)
            emojied.append(emojis['correct_letter'])
            seen += letter
        else:
            scored += incorrect(letter)
            emojied.append(emojis['incorrect'])
            seen += letter
    return ''.join(scored), ''.join(emojied)


WELCOME_MESSAGE = correct_place("WELCOME") + " " + incorrect("TO") + " " + correct_letter("TWORDLE") + "\n"


def main():
    rich.print(WELCOME_MESSAGE)

    allowed_guesses = 6
    used_guesses = 0
    console = Console()

    answer_word = get_random_line("word_list.txt").upper().strip()

    all_emojied = []
    all_scored = []

    # game loop
    while used_guesses < allowed_guesses:
        used_guesses += 1
        guess = Prompt.ask("Enter your guess").upper().strip()
        if len(guess) != len(answer_word):
            print(f"Word should be {len(answer_word)} letters long")
            used_guesses -= 1
        else:
            scored, emojied = score_guess(guess, answer_word)
            all_scored.append(scored)
            all_emojied.append(emojied)
            console.clear()
            for scored in all_scored:
                console.print(scored)
            if guess == answer_word:
                break
    print(f"\n\nPYRDLE {used_guesses}/{allowed_guesses}\nWORD WAS: {answer_word}")
    for em in all_emojied:
        console.print(em)


if __name__ == '__main__':
    main()
