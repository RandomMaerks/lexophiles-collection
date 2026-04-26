### --------------- MODULES ---------------

from datetime import datetime
import random
from resources.word_finder import wordFinder

### --------------- INFO ---------------

name = "Hangman"
creator = "RandomMaerks"
description = "Find the word by guessing the correct letters."
version = "1.0"

### --------------- FUNCTIONS ---------------

def writeHistory(historyDir, lines):
    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    historyLines = [f"[{currentTime}] {name}"]
    for key in lines:
        historyLines.append(f"> {key}: {lines[key]}")

    with open(historyDir, "a", encoding="utf8") as history:
        history.write('\n'.join(historyLines) + '\n\n')

def displayTitle():
    print(
        f"\n"
        f"+-{'-'*len(name)}-+\n"
        f"| {name} |\n"
        f"+-{'-'*len(name)}-+\n"
        f"Creator: {creator}\n"
        f"Version: {version}\n"
    )

### --------------- MAIN GAME ---------------

def run(context):
    displayTitle()

    row1 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
    row2 = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
    row3 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']

    toUse = ''.join(row1) + ''.join(row2) + ''.join(row3)
    while True:
        keyword = random.choice(context.wordList).upper()
        if any(x not in toUse for x in keyword):
            continue
        break
    lineDisplay = ["_" for i in range(len(keyword))]

    totalWrong = 6
    guessNumber = 0
    wrongGuess = 0

    letterUsed = []

    hangDisplay = [
        "  ______  \n",
        "  |       \n",
        "  |       \n",
        "  |       \n",
        "  |       \n",
        "[][][][][]\n"
        ]

    winDisplay = [
        "    \n",
        "         \n",
        "    \\O/    \n",
        "     |   \n",
        "    / \\    \n",
        "[][][][][]\n"
        ]

    man = [
        ["  |    o  \n", "  |       \n", "  |       \n"],
        ["  |    o  \n", "  |    |  \n", "  |       \n"],
        ["  |    o  \n", "  |   /|  \n", "  |       \n"],
        ["  |    o  \n", "  |   /|\\  \n", "  |       \n"],
        ["  |    o  \n", "  |   /|\\  \n", "  |   /   \n"],
        ["  |    o  \n", "  |   /|\\  \n", "  |   / \\ \n"]
        ]

    print(
        "You can only guess the wrong letter 6 times before the man is hanged. Be careful.\n"
        "Type /giveup to see the result, and /exit to end the game.\n"
        )
    while True:
        row1 = ["_" if x in letterUsed else x for x in row1]
        row2 = ["_" if x in letterUsed else x for x in row2]
        row3 = ["_" if x in letterUsed else x for x in row3]
        
        print(
            f"{''.join(hangDisplay)}\n\n"
            f"{''.join(lineDisplay)}\n\n"
            f"[{']['.join(row1)}]\n"
            f" [{']['.join(row2)}]\n"
            f"  [{']['.join(row3)}]\n"
            )

        if wrongGuess == totalWrong:
            print("You couldn't save the man!")
            break
        
        print("* Enter a letter:")
        while True:
            answer = str(input("> "))
            if not answer: continue
            if answer == "/exit":
                print("You've ended the game prematurely!")
                return
            elif answer == "/giveup":
                print("You stopped the game!")
                break
            answer = answer.upper()

            if len(answer) != 1 or answer not in toUse:
                print("That's not a letter! Try again.")
                continue
            if answer in letterUsed:
                print("That letter has already been used! Try again.")
                continue
            break

        if answer == "/giveup":
            break

        validLetter = False
        for letter in range(len(keyword)):
            if keyword[letter] == answer:
                lineDisplay[letter] = answer
                validLetter = True

        if validLetter == True:
            print(f"{answer.upper()} exists in the keyword!\n")
        else:
            wrongGuess += 1
            print(f"{answer.upper()} does NOT exist in the keyword! Wrong guesses: {wrongGuess}\n")
            for line, line2 in zip(range(1, 4), range(3)):
                hangDisplay[line] = man[wrongGuess-1][line2]

        letterUsed.append(answer)
        guessNumber += 1
        
        if ''.join(lineDisplay) == keyword:
            row1 = ["_" if x in letterUsed else x for x in row1]
            row2 = ["_" if x in letterUsed else x for x in row2]
            row3 = ["_" if x in letterUsed else x for x in row3]
            print(
                f"{''.join(winDisplay)}\n\n"
                f"{''.join(lineDisplay)}\n\n"
                f"[{']['.join(row1)}]\n"
                f" [{']['.join(row2)}]\n"
                f"  [{']['.join(row3)}]\n"
            )
            print("You guessed the word!")
            break

    print(
        f"The word is {keyword}!\n"
        f"Your letters: {' '.join(letterUsed)}\n"
        f"Number of guesses: {guessNumber-1}"
        )

    lines = {
        "Solution" : f"{keyword}",
        "Guesses" : f"({guessNumber-1}) {' '.join(letterUsed)} ; {wrongGuess}/6 wrong guesses",
    }
    writeHistory(context.history, lines)