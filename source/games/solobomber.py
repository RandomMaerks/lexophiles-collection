### --------------- MODULES ---------------

from datetime import datetime
import random

### --------------- INFO ---------------

name = "Solobomber"
creator = "RandomMaerks"
description = "Make a word using a letter combo or prompt."
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
    
    with open("resources/prompts.txt", "r", encoding="utf8") as prompts:
        comboList = prompts.read().split("\n")

    wordsUsed = 0
    score = 0
    answerUsed = []

    tries = 3
    print(
        "You have 3 tries. Using words which have already been used will take away one try.\n"
        "Type /giveup to see the result, and /exit to end the game.\n"
        )
    while tries != 0:
        combo = random.choice(comboList)
        print("* Make an English word containing this prompt:", combo)
        
        while True:
            answer = str(input("> "))
            if not answer: continue
            if answer == "/exit":
                print("You've ended the game prematurely!")
                return
            elif answer == "/giveup":
                print("You stopped the game!")
                break

            if combo not in answer:
                print(f"'{answer}' does not include '{combo}'! Try again.")
                continue
            if answer not in context.wordList:
                print(f"'{answer}' does not exist in the selected dictionary! Try again.")
                continue
            break

        if answer == "/giveup":
            break
        
        if answer not in answerUsed:
            score += len(answer)
            print(f"Correct! Word score: {len(answer)}; total: {score}\n")
        else:
            tries -= 1
            plural = "ies" if tries > 1 else "y"
            print(f"'{answer}' has already been used. You have {tries} tr{plural} left.\n")
            
        wordsUsed += 1   
        answerUsed.append(answer)
        continue
            
    print("Game ended!\n")

    plural = "s" if wordsUsed > 1 else ""
    print(
        f"You have used {wordsUsed} word{plural}!\n"
        f"Your score: {score}"
        )

    lines = {
        "Words" : f"({wordsUsed}) {', '.join(answerUsed)}",
        "Score" : f"{score}",
    }
    writeHistory(context.history, lines)