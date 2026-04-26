### --------------- MODULES ---------------

from datetime import datetime
import random
from resources.word_finder import wordFinder

### --------------- INFO ---------------

name = "Wordle"
creator = "RandomMaerks"
description = "The New York Times Wordle, but with custom word length."
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

    print(
        "\n"
        "Mode: [1] Classic: Use NYT's past solutions, limiting word length to 5\n"
        "      [2] Custom: Use preselected dictionary, allowing custom word length\n"
        )
    print("* Choose mode (int): ")
    mode = ""
    while True:
        try:
            modeSelection = int(input("> "))
        except Exception:
            print("Invalid index. Try again.")
            continue

        if modeSelection not in range(1, 3):
            print("Not a mode. Try again.")
            continue
        
        if modeSelection == 1:
            print("\n--- MODE : CLASSIC ---\n")
            mode = "Classic"
        elif modeSelection == 2:
            print("\n--- MODE : CUSTOM ---\n")
            mode = "Custom"
        break

    if mode == "Classic":
        solutionList = open("resources/wordle.txt", "r", encoding="utf8")
        solution = solutionList.read().split("\n")
        keyword = random.choice(solution)
        wordLength = 5
    elif mode == "Custom":
        print("* Enter word length (int > 0):")
        while True:
            try:
                wordLength = int(input("> "))
            except Exception:
                print("Not an integer. Try again.")
                continue

            if wordLength <= 0:
                print("Word length cannot be smaller than 1. Enter a different number.")
                continue
            elif wordLength > 15:
                print("* That'd be a long word. Are you sure you want to continue (y/n)?")
                question = str(input("> "))
                if question == "n":
                    print("* Enter word length (int > 0):")
                    continue
                elif question != "y":
                    print("Invalid answer. Choosing 'yes' automatically.")                    
            break
        while True:
            keyword = random.choice(context.wordList)
            if len(keyword) == wordLength:
                break
    
    print("\n[×] = Grey; [?] = Yellow; [!] = Green\n")

    guessNumber = 1
    answerList = []
    checkerList = []
    totalGuesses = 6 if wordLength <= 5 else wordLength+1

    print(
        f"You have {totalGuesses} guesses in total. Use them wisely.\n"
        "Type /giveup to see the result, and /exit to end the game.\n"
        )
    
    while True:
        keywordModified = keyword
        checker = ["×" for i in range(wordLength)]
        
        print(f"\n[ Guess {guessNumber}/{totalGuesses} ]")
        
        while True:
            answer = str(input("> "))
            if not answer: continue
            if answer == "/exit":
                print("You've ended the game prematurely!")
                return
            elif answer == "/giveup":
                print("You stopped the game!")
                break

            if len(answer) != wordLength:
                print("Invalid word! Try again.")
                continue
            if answer not in context.wordList:
                print(f"'{answer}' is not in the selected dictionary! Try again")
                continue
            break

        if answer == "/giveup":
            break

        answer = answer.lower()
        
        for letter in range(0, wordLength):
            if answer[letter] == keywordModified[letter]:
                checker[letter] = "!"
                keywordModified = keywordModified[:letter] + "0" + keywordModified[letter+1:]
                
        for letter in range(0, wordLength):
            if answer[letter] == keywordModified[letter]:
                continue
            elif answer[letter] == keyword[letter]:
                continue
            elif answer[letter] not in keywordModified:
                continue
            foundIndex = keywordModified.find(answer[letter])
            checker[letter] = "?"
            keywordModified = keywordModified[:foundIndex] + "0" + keywordModified[foundIndex+1:]

        checkerList.append(''.join(checker))
        answerList.append(answer.upper())

        print()
        for guess in range(guessNumber):
            print(answerList[guess])
            print(checkerList[guess])
        
        guessNumber += 1
     
        if answer == keyword:
            print("\nYou guessed the word!")
            break
        elif guessNumber == totalGuesses + 1:
            print("\nYou're out of guesses!")
            break
        
    print(
        f"The word is {keyword.upper()}!\n"
        f"Your words: {', '.join(answerList)}\n"
        f"Number of guesses: {guessNumber-1}"
        )

    lines = {
        "Mode" : f"{mode}",
        "Solution" : f"{keyword.upper()}",
        "Guesses" : f"({guessNumber-1}/{totalGuesses}) {', '.join(answerList)}",
    }
    writeHistory(context.history, lines)