### --------------- MODULES ---------------

from datetime import datetime
import random
from resources.word_finder import wordFinder

### --------------- INFO ---------------

name = "Word Chain"
creator = "RandomMaerks"
description = "Make a unique word using the last letter of the previous guess."
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
        "Mode: [1] Solo: Human-only\n"
        "      [2] Computer: Battle against a word randomiser\n"
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
            print("\n--- MODE : SOLO ---\n")
            mode = "Solo"
        elif modeSelection == 2:
            print("\n--- MODE : COMPUTER ---\n")
            mode = "Computer"
        break

    answerUsed = []
    score = 0
    wordsUsed = 0
    
    tries = 3
    print(
        "You have 3 tries. Using invalid or already used words will take away one try.\n"
        "Type /giveup to see the result, and /exit to end the game.\n"
        )
    
    wordToCheck = random.choice(context.wordList)
    answerUsed.append(wordToCheck)
    
    while tries != 0:
        print("* Write an English word containing the last letter of the word:", wordToCheck)

        while True:
            answer = str(input("> "))
            if not answer: continue
            if answer == "/exit":
                print("You've ended the game prematurely!")
                return
            elif answer == "/giveup":
                print("You stopped the game!")
                break
            
            if answer not in context.wordList:
                print(f"'{answer}' does not exist in the selected dictionary! Try again.")
                continue
            break

        if answer == "/giveup":
            break
        
        if not answer.startswith(wordToCheck[-1]):
            tries -= 1
            plural = "ies" if tries > 1 else "y"
            print(f"'{answer}' does not start with the letter [{wordToCheck[-1]}]. You have {tries} tr{plural} left.")
        elif answer in answerUsed:
            tries -= 1
            plural = "ies" if tries > 1 else "y"
            print(f"'{answer}' has already been used. You have {tries} tr{plural} left.")
        else:
            score += len(answer)
            wordsUsed += 1
            answerUsed.append(answer)
            if mode == "Solo":
                wordToCheck = answer
            elif mode == "Computer":
                computerTries = 0
                while computerTries < len(context.wordList):
                    wordToCheck = random.choice(context.wordList)
                    if wordToCheck.startswith(answer[-1]):
                        print(f"The computer has chosen the word '{wordToCheck}'.")
                        answerUsed.append(wordToCheck)
                        break
                    elif computerTries > len(context.wordList):
                        print("The computer cannot find any valid word!")
                        break
                    computerTries += 1

    print("Game ended!\n")
                
    plural = "s" if wordsUsed > 1 else ""
    print(
        f"You have used {wordsUsed} word{plural}!\n"
        f"Your score: {score}"
        )

    lines = {
        "Mode" : f"{mode}",
        "Words" : f"({wordsUsed}) {', '.join(answerUsed)}",
        "Score" : f"{score}",
    }
    writeHistory(context.history, lines)