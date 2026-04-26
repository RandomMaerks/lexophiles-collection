### --------------- MODULES ---------------

from datetime import datetime
import random
from resources.word_finder import wordFinder

### --------------- INFO ---------------

name = "Combiner"
creator = "RandomMaerks"
description = "Find all words given a set of letters."
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
        "Mode: [1] Simple: Scramble letters from existing word, guaranteeing at least one valid solution\n"
        "      [2] Rogue: All letters random, may have no solutions\n"
        )
    print("* Choose mode (int):")
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
            print("\n--- MODE : SIMPLE ---\n")
            mode = "Simple"
        elif modeSelection == 2:
            print("\n--- MODE : ROGUE ---\n")
            mode = "Rogue"
        break

    if mode == "Simple":
        while True:
            randomWord = random.choice(context.wordList).upper()
            if len(randomWord) in range(3, 10): break
        letters = random.sample(randomWord, k=len(randomWord))
    elif mode == "Rogue":
        alphabet = [
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M'
            ]
        weights = [
            2, 5, 14, 10, 11, 5, 8, 10, 11, 5,
            12, 10, 9, 5, 6, 6, 2, 2, 8,
            2, 4, 7, 4, 5, 10, 7
            ]
        letters = random.choices(alphabet, weights, k=random.randrange(3, 10))

    allPossibleWords = wordFinder(
        context.wordList,
        wordLength = [3, len(letters)],
        restriction = [None, ''.join(letters).lower(), None],
        )
    allPossibleWords = [word.upper() for word in allPossibleWords]

    letterAmount = len(letters)
    placement = {
        3: [1, 6, 8],
        4: [1, 3, 5, 7],
        5: [0, 2, 3, 5, 7],
        6: [0, 2, 3, 5, 6, 8],
        7: [0, 1, 2, 3, 5, 7, 8],
        8: [0, 1, 2, 3, 5, 6, 7, 8],
        9: [0, 1, 2, 3, 4, 5, 6, 7, 8],
    }

    grid = [
        " ", " ", " ",
        " ", " ", " ",
        " ", " ", " ",
        ]
    for letter, spot in zip(letters, placement[letterAmount]):
        grid[spot] = letter

    answerUsed = []

    print(
        "Make a valid word using the given letters.\n"
        "You cannot use a letter more times than there are that letter, and your words must be 3 letters or longer.\n"
        "Type /shuffle to randomise the grid, /giveup to end and save progress, and /exit to end the game."
        )

    while True:
        print(f"\nWords: {len(answerUsed)}/{len(allPossibleWords)}")
        wordIndex = 0
        display = ["Used words:  "]
        maxLength = 0

        for word in answerUsed:
            if maxLength < len(word): maxLength = len(word)

        for wordIndex, word in enumerate(answerUsed):
            space = " " * (maxLength - len(word))
            if wordIndex % 4 == 3: display.append(f"{answerUsed[wordIndex]}{space}  \n             ")
            else: display.append(f"{answerUsed[wordIndex]}{space}  ")
        print(f"{''.join(display)}")

        print(
            f"⎡ {grid[0]}  {grid[1]}  {grid[2]} ⎤\n"
            f"⎢ {grid[3]}  {grid[4]}  {grid[5]} ⎥\n"
            f"⎣ {grid[6]}  {grid[7]}  {grid[8]} ⎦\n"
            )
        
        while True:
            answer = str(input("> "))
            if not answer: continue
            if answer == "/exit":
                print("You've ended the game prematurely!")
                return
            elif answer == "/giveup":
                print("You stopped the game!")
                break
            elif answer == "/shuffle":
                break
            answer = answer.upper()

            if any(answer.count(i) not in range(0, letters.count(i)+1) for i in answer):
                print(f"'{answer}' has an invalid letter! Try again.")
                continue
            if len(answer) < 3:
                print(f"Your word was too short! Try again.")
            if answer not in allPossibleWords:
                print(f"'{answer}' does not exist in the selected dictionary! Try again.")
                continue
            if answer in answerUsed:
                print(f"'{answer}' has already been used! Try again.")
                continue
            break

        if answer == "/giveup":
            break
        elif answer == "/shuffle":
            grid = baseGrid
            random.shuffle(letters)
            for letter, spot in zip(letters, placement):
                grid[spot] = letter
            continue

        answerUsed.append(answer)

        if len(answerUsed) == len(allPossibleWords):
            print("You've found all possible words!")
            break

    plural = "" if len(answerUsed) == 1 else "s"
    
    print(
        f"\nYou found: {len(answerUsed)}/{len(allPossibleWords)} word{plural}!\n"
        f"Your word{plural}: {', '.join(answerUsed)}\n"
        f"All words found in the dictionary: {', '.join(allPossibleWords)}"
        )

    lines = {
        "Mode" : f"{mode}",
        "Guesses" : f"({len(answerUsed)}) {', '.join(answerUsed)}",
        "All possible" : f"({len(allPossibleWords)}) {', '.join(allPossibleWords)}",
    }
    writeHistory(context.history, lines)
