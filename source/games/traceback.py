### --------------- MODULES ---------------

from datetime import datetime
import random

### --------------- INFO ---------------

name = "Traceback"
creator = "RandomMaerks"
description = "Find the original word from a set of word hints."
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
        "Difficulties: [1] Easy (4 letters, min 2 correct)\n"
        "              [2] Medium (5 letters, 1-2 correct)\n"
        "              [3] Hard (6 letters, 1 valid)\n"
        "              [4] Outrageous (7-9, guaranteed no valid)\n"
        )

    print("* Choose difficulty (int): ")
    difficulty = ""
    while True:
        try:
            difficultySelection = int(input("> "))
        except Exception:
            print("Invalid index. Try again.")
            continue

        if difficultySelection not in range(1, 5):
            print("Not a mode. Try again.")
            continue
        
        if difficultySelection == 1:
            print("\n--- DIFFICULTY : EASY ---\n")
            difficulty = "Easy"
        elif difficultySelection == 2:
            print("\n--- DIFFICULTY : MEDIUM ---\n")
            difficulty = "Medium"
        elif difficultySelection == 3:
            print("\n--- DIFFICULTY : HARD ---\n")
            difficulty = "Hard"
        elif difficultySelection == 4:
            print("\n--- DIFFICULTY : OUTRAGEOUS ---\n")
            difficulty = "Outrageous"
        break

    while True:
        keyword = random.choice(context.wordList)
        if difficulty == "Easy" and len(keyword) != 4:
            continue
        elif difficulty == "Medium" and len(keyword) != 5:
            continue
        elif difficulty == "Hard" and len(keyword) != 6:
            continue
        elif difficulty == "Outrageous" and not len(keyword) not in range(7, 10):
            continue
        break

    while True:
        starterWord = random.choice(context.wordList)
        if len(starterWord) != len(keyword):
            continue
        elif starterWord == keyword:
            continue

        keywordModified = keyword
             
        wordLength = len(starterWord)
        checker = ["×" for i in range(wordLength)]

        for letter in range(0, wordLength):
            if starterWord[letter] == keywordModified[letter]:
                checker[letter] = "!"
                keywordModified = keywordModified[:letter] + "0" + keywordModified[letter+1:]
        
        for letter in range(0, wordLength):
            if starterWord[letter] == keywordModified[letter]:
                continue
            elif starterWord[letter] == keyword[letter]:
                continue
            elif starterWord[letter] not in keywordModified:
                continue
            foundIndex = keywordModified.find(starterWord[letter])
            checker[letter] = "?"
            keywordModified = keywordModified[:foundIndex] + "0" + keywordModified[foundIndex+1:]

        if difficulty == "Easy" and checker.count("!") < 2:
            continue
        elif difficulty == "Medium" and checker.count("!") not in range(1, 3):
            continue
        elif difficulty == "Hard" and checker.count("?") != 1 and checker.count("!") != 0:
            continue
        elif difficulty == "Outrageous" and checker.count("?") != 0 and checker.count("!") != 0:
            continue
        break
    
    print("[×] = Not correct nor valid; [?] = Valid; [!] = Correct\n")

    keyword = keyword.upper()
    starterWord = starterWord.upper()

    guessNumber = 1
    answerList = [starterWord]
    checkerList = [''.join(checker)]
    totalGuesses = wordLength + 6

    print(
        f"You have {totalGuesses} guesses in total. Invalid words take away guesses, and correct letters give you extra.\n"
        "Enter the index-replacement combo (eg. 1A).\n"
        "Type /giveup to see the result, and /exit to end the game.\n"
        )

    print(answerList[0])
    print(checkerList[0])
    
    while True:
        keywordModified = keyword
        checker = ["×" for i in range(wordLength)]
        
        print(f"\n[ Guess {guessNumber}/{totalGuesses} ]")

        while True:
            userInput = str(input("> "))
            if not userInput: continue
            if userInput == "/exit":
                print("You've ended the game prematurely!")
                return
            elif userInput == "/giveup":
                print("You stopped the game!")
                break
            try:
                indexToReplace = int(userInput[0])-1
                letterToReplace = str(userInput[1]).upper()
            except Exception:
                print("Incorrect combo. Try again.")

            answer = answerList[-1]
            answer = ''.join([
                answer[i] if i != indexToReplace else
                letterToReplace for i in range(wordLength)
                ])
            break

        if userInput == "/giveup":
            break
        
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

        if checkerList[-1].count("!") > checkerList[-2].count("!") and answer.lower() in context.wordList:
            totalGuesses += 1
            print(f"Nice work! You got an extra guess (total: {totalGuesses}).")
        elif checkerList[-1].count("!") > checkerList[-2].count("!") and answer.lower() not in context.wordList:
            print(f"You found a correct letter, but the word is invalid! (total: {totalGuesses}).")
        elif answer.lower() not in context.wordList:
            totalGuesses -= 1
            print(f"'{answer}' does not exist in the selected dictionary! You've lost one guess (total: {totalGuesses}).")
    
        guessNumber += 1

        print()
        for guess in range(guessNumber):
            print(answerList[guess])
            print(checkerList[guess])
        
        if answer == keyword:
            print("\nYou guessed the word!")
            break
        elif guessNumber == totalGuesses + 1:
            print("\nYou're out of guesses!")
            break
        
    print(
        f"The word is {keyword}!\n"
        f"Your words: {', '.join(answerList)}\n"
        f"Number of guesses: {guessNumber-1}"
        )

    lines = {
        "Difficulty" : f"{difficulty}",
        "Solution & starter:" : f"{keyword}, {starterWord}",
        "Guesses" : f"({guessNumber-1}/{totalGuesses}) {', '.join(answerList)}",
    }
    writeHistory(context.history, lines)