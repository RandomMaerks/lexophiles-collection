### --------------- MODULES ---------------

from datetime import datetime
import random

### --------------- INFO ---------------

name = "Unscramble"
creator = "RandomMaerks"
description = "Guess the correct word(s) from a jumbled set of letters."
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
        "Difficulties: [1] Easy (1 word)\n"
        "              [2] Hard (2 words scrambled into each other)\n"
        "              [3] Mess (3 words, same concept as Hard)\n"
        )
    difficulty = ""
    while True:
        try:
            difficultySelection = int(input("> "))
        except Exception:
            print("Invalid index. Try again.")
            continue

        if difficultySelection not in range(1, 4):
            print("Not a mode. Try again.")
            continue
        
        if difficultySelection == 1:
            print("\n--- DIFFICULTY : EASY ---\n")
            difficulty = "Easy"
        elif difficultySelection == 2:
            print("\n--- DIFFICULTY : HARD ---\n")
            difficulty = "Hard"
        elif difficultySelection == 3:
            print("\n--- DIFFICULTY : MESS ---\n")
            difficulty = "Mess"
        break

    keywords = []
    while True:
        keyword = random.choice(context.wordList).upper()
        if len(keyword) < 4: continue

        keywords.append(keyword)
        if difficulty == "Easy" and len(keywords) == 1:
            break
        elif difficulty == "Hard" and len(keywords) == 2:
            break
        elif difficulty == "Mess" and len(keywords) == 3:
            break

    combined = ''.join(keywords)
    scrambled = random.sample(combined, k=len(combined))

    blankDisplay = [''.join(["_" for _ in range(len(keyword))]) for keyword in keywords]
    
    answerList = []
    answerUsed = []

    plural = "" if len(keywords) == 1 else "s"
    print(
        f"You got {len(keywords)} word{plural} all scrambled up. Guess the word{plural} to win.\n"
        "Type /giveup to see the result, and /exit to end the game."
        )
    while True:
        print("\n" + ''.join(scrambled))
        print("\n" + '\n'.join(blankDisplay) + "\n")

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
            
            if len(answer) < 4:
                print("Your word is too short (minimum length: 4)")
                continue

            answerUsed.append(answer)

            if answer in keywords:
                print(f"Nice work! You got {answer}.")
                answerList.append(answer)
                break
            else:
                print("That's not quite right! Try again.")
                continue

        if answer == "/giveup":
            break

        if all(answer in answerList for answer in keywords):
            print("You got all the words!")
            break

        blankDisplay[keywords.index(answer)] = answer
        for letter in answer:
            index = scrambled.index(letter)
            scrambled[index] = "_"

    plural2 = "is" if len(keywords) == 1 else "are"
    print(
        f"\nThe word{plural} {plural2} {', '.join(keywords)}!\n"
        f"Your word{plural}: ({len(answerList)}/{len(answerUsed)} correct) {', '.join(answerUsed)}\n"
        )

    lines = {
        "Difficulty" : f"{difficulty}",
        f"Solution{plural}" : f"{', '.join(keywords)}",
        "Guesses" : f"({len(answerList)}/{len(answerUsed)} correct) {', '.join(answerUsed)}",
    }
    writeHistory(context.history, lines)