import random
from datetime import datetime
from boggle import grid
from word_finder import wordFinder

wordList = []

## --------------- INITIALISE DICTIONARY --------------- 

def chooseDict():
    global wordList
    print(
        "\n"
        "----------------\n"
        "| Dictionaries |\n"
        "----------------\n"
        "[1] wlist_match1.txt (Composed by Keith Vertanen, contains 1517K words)\n"
        "[2] words_alpha.txt (Composed by dwyl, contains 370K words)\n"
        "[3] wordlist.txt (Composed by Florida State University, contains 300K words)\n"
        "[4] CSW21 - Collins Scrabble Words (Contains 219K words)\n"
        "[5] twl06.txt (Composed by Free Scrabble Dictionary, contains 177K words)\n"
        "[6] english_3000.txt (Composed by EF, contains 3K most common English words)"
        )

    dictDest = [
        "dictionaries/wlist_match1.txt",
        "dictionaries/words_alpha.txt",
        "dictionaries/wordlist.txt",
        "dictionaries/twl06.txt",
        "dictionaries/english.txt",
        "dictionaries/english_3000.txt"
        ]

    print("* Choose dictionary (int):")
    while True:
        try:
            indexDict = int(input("> "))
        except Exception:
            print("Invalid index. Try again.")
            continue
        
        if indexDict not in range(1, len(dictDest)+1):
            print("Not an option. Try again")
            continue
        
        dictionary = open(dictDest[indexDict-1], "r", encoding="utf8")
        break
            
    wordList = dictionary.read().split("\n")
    dictionary.close()

    menu()

## --------------- INITIALISE MENU --------------- 

def menu():
    print(
        "\n"
        "--------\n"
        "| Menu |\n"
        "--------\n"
        "Options: [1] History: Display game history\n"
        "         [2] Dictionary: Choose a dictionary\n"
        "Games: [3] Solobomber: Make a word using a letter combo (inspo: BombParty (JKLM), Word Bomb (OMG))\n"
        "       [4] Word Chain: Make a unique word using the last letter of the previous guess\n"
        "       [5] Wordle: NYT's Wordle with custom options\n"
        "       [6] Hangman: Guess the correct letters of a word\n"
        "       [7] Boggle: Find as many words as possible from a grid of letters\n"
        "       [8] Sleuth: Find all given words hidden inside a grid of letters\n"
        "       [9] Combiner: Find all words given a set of letters\n"
        "       [10] Unscramble: Guess the correct word from its jumbled-up letters\n"
        "       [11] Traceback: Find the original word from a set of word hints\n"
        )

    if not wordList:
        print("You currently have no dictionary selected. Go to mode [2] to choose.")

    print("* Choose mode (int):")
    while True:
        try:
            selection = int(input("> "))
        except Exception:
            print("Invalid mode. Try again.")
            continue

        if selection not in range(1, 12):
            print("Not an option. Try again.")
            continue

        if not wordList and selection not in [1, 2]:
            print("No dictionary selected. Go to mode [2] to choose.")
            continue

        if selection == 1: history()
        elif selection == 2: chooseDict()
        elif selection == 3: solobomber()
        elif selection == 4: wordChain()
        elif selection == 5: wordle()
        elif selection == 6: hangman()
        elif selection == 7: boggle()
        elif selection == 8: sleuth()
        elif selection == 9: combiner()
        elif selection == 10: unscramble()
        elif selection == 11: traceback()
        break

## --------------- PAST GAME HISTORY --------------- 
    
def history():
    print(
        "\n"
        "-----------\n"
        "| History |\n"
        "-----------\n"
        )
    with open("gameHistory.txt", "r", encoding="utf8") as file:
        data = file.read().split("\n")
        for line in data:
            print(line)

    menu()

## --------------- SOLOBOMBER --------------- 

def solobomber():
    print(
        "\n"
        "--------------\n"
        "| Solobomber |\n"
        "--------------\n"
        )
    
    prompts = open("resources/prompts.txt", "r", encoding="utf8")
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
            if answer == "/exit":
                print("You've ended the game prematurely!")
                menu()
            elif answer == "/giveup":
                print("You stopped the game!")
                break
            if combo not in answer:
                print(f"'{answer}' does not include '{combo}'! Try again.")
                continue
            elif answer not in wordList:
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

    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historyLines = [
        f"[{currentTime}] Solobomber",
        f"> Words: ({wordsUsed}) {', '.join(answerUsed)}",
        f"> Score: {score}\n\n"
        ]
    with open("gameHistory.txt", "a", encoding="utf8") as history:
        history.write('\n'.join(historyLines))
    
    menu()

## --------------- WORD CHAIN --------------- 

def wordChain():
    print(
        "\n"
        "--------------\n"
        "| Word Chain |\n"
        "--------------\n"
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
    
    wordToCheck = random.choice(wordList)
    answerUsed.append(wordToCheck)
    
    while tries != 0:
        print("* Write an English word containing the last letter of the word:", wordToCheck)

        while True:
            answer = str(input("> "))
            if answer == "/exit":
                print("You've ended the game prematurely!")
                menu()
            elif answer == "/giveup":
                print("You stopped the game!")
                break
            if answer not in wordList:
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
                while computerTries < len(wordList):
                    wordToCheck = random.choice(wordList)
                    if wordToCheck.startswith(answer[-1]):
                        print(f"The computer has chosen the word '{wordToCheck}'.")
                        answerUsed.append(wordToCheck)
                        break
                    elif computerTries > len(wordList):
                        print("The computer cannot find any valid word!")
                        break
                    computerTries += 1

    print("Game ended!\n")
                
    plural = "s" if wordsUsed > 1 else ""
    print(
        f"You have used {wordsUsed} word{plural}!\n"
        f"Your score: {score}"
        )

    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historyLines = [
        f"[{currentTime}] Word Chain - {mode}",
        f"> Words: ({wordsUsed}) {', '.join(answerUsed)}",
        f"> Score: {score}\n\n"
        ]
    with open("gameHistory.txt", "a", encoding="utf8") as history:
        history.write('\n'.join(historyLines))
    
    menu()

## --------------- WORDLE --------------- 

def wordle():
    print(
        "\n"
        "----------\n"
        "| Wordle |\n"
        "----------\n"
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
            keyword = random.choice(wordList)
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
            if answer == "/exit":
                print("You've ended the game prematurely!")
                menu()
            elif answer == "/giveup":
                print("You stopped the game!")
                break
            if len(answer) != wordLength:
                print("Invalid word! Try again.")
                continue
            elif answer not in wordList:
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

    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historyLines = [
        f"[{currentTime}] Wordle - {mode}",
        f"> Solution: {keyword.upper()}",
        f"> Guesses: ({guessNumber-1}/{totalGuesses}) {', '.join(answerList)}\n\n"
        ]
    with open("gameHistory.txt", "a", encoding="utf8") as history:
        history.write('\n'.join(historyLines))
    
    menu()

## --------------- HANGMAN --------------- 

def hangman():
    print(
        "\n"
        "-----------\n"
        "| Hangman |\n"
        "-----------\n"
        )

    row1 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
    row2 = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
    row3 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']

    toUse = ''.join(row1) + ''.join(row2) + ''.join(row3)
    while True:
        keyword = random.choice(wordList).upper()
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
            answer = str(input("> ")).upper()
            if answer == "/exit":
                print("You've ended the game prematurely!")
                break
            elif answer == "/giveup":
                print("You stopped the game!")
                break
            if len(answer) != 1 or answer not in toUse:
                print("That's not a letter! Try again.")
                continue
            elif answer in letterUsed:
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

    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historyLines = [
        f"[{currentTime}] Hangman",
        f"> Solution: {keyword}",
        f"> Guesses: ({guessNumber-1}) {' '.join(letterUsed)} ; {wrongGuess}/6 wrong guesses\n\n"
        ]
    with open("gameHistory.txt", "a", encoding="utf8") as history:
        history.write('\n'.join(historyLines))
        
    menu()

## --------------- BOGGLE --------------- 

def boggle():
    print(
        "\n"
        "----------\n"
        "| Boggle |\n"
        "----------\n"
        )

    print(
        "* Enter your filter [rows, columns, maxScore, maxWords, seed]\n"
        "(default: 4 4 100 -1 -1, -1 = inf or None):"
        )
    while True:
        userInput = str(input("> "))
        if not userInput:
            inputtedFilters = []
            break
        try:
            inputtedFilters = [int(x) for x in userInput.split(" ")]
        except Exception:
            print("Cannot process filters. Try again.")
            continue
        break
    
    defaultFilters = [4, 4, 100, -1, -1]
    filters = [
        int(inputtedFilters[i]) if i < len(inputtedFilters) else
        int(defaultFilters[i])
        for i in range(5)
        ]
    gridRows = filters[0]
    gridCols = filters[1]
    maxScore = filters[2] if filters[2] != -1 else 2147283648
    maxWords = filters[3] if filters[3] != -1 else 2147283648
    seed = filters[4] if filters[4] != -1 else random.getrandbits(64)

    boggleGrid = grid(wordList, gridRows, gridCols, seed)

    print(
        "To make a word, enter your row-column combos (row-column as one number).\n"
        "Type /giveup to see the result, and /exit to end the game.\n"
        )
    while True:
        boggleGrid.displayGrid()
        userInput = str(input("> "))
        if userInput == "/exit":
            print("You've ended the game prematurely!")
            menu()
        elif userInput == "/giveup":
            print("You stopped the game!")
            break
        print(boggleGrid.getWord(userInput.split(" ")))

        if boggleGrid.score >= maxScore:
            print("You've reached the max score!")
            break
        elif len(boggleGrid.history) >= maxWords:
            print("You've played all {maxWords} words!")
            break

    guessDisplay = ', '.join(
        [f"{boggleGrid.history[i]} ({boggleGrid.wordScore[i]})" for i in range(len(boggleGrid.history))]
        )
    
    print(
        f"Your score: {boggleGrid.score}\n"
        f"Your letters: ({gridRows}×{gridCols}, seed: {boggleGrid.setSeed}) {' '.join(boggleGrid.grid)}\n"
        f"Your guesses: (Total: {boggleGrid.score}) {guessDisplay}"
        )

    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historyLines = [
        f"[{currentTime}] Boggle",
        f"> Grid: ({gridRows}×{gridCols}, seed: {boggleGrid.setSeed}) {' '.join(boggleGrid.grid)}",
        f"> Guesses: (Total: {boggleGrid.score}) {guessDisplay}\n\n"
        ]
    with open("gameHistory.txt", "a", encoding="utf8") as history:
        history.write('\n'.join(historyLines))

    del boggleGrid
    
    menu()
    
## --------------- SLEUTH ---------------
    
def sleuth():
    menu()

## --------------- COMBINER ---------------
    
def combiner():
    print(
        "\n"
        "------------\n"
        "| Combiner |\n"
        "------------\n"
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
            randomWord = random.choice(wordList).upper()
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
        wordList, [0, 3, len(letters)], 0, 0, ["", ''.join(letters).lower(), ""], ["", "", "", ""], [""]
        )[0]
    allPossibleWords = allPossibleWords.upper().split() if allPossibleWords != "No words found\n\n" else []

    baseGrid = [
        " ", " ", " ",
        " ", " ", " ",
        " ", " ", " ",
        ]

    letterAmount = len(letters)
    if letterAmount == 3: placement = [1, 6, 8]
    elif letterAmount == 4: placement = [1, 3, 5, 7]
    elif letterAmount == 5: placement = [0, 2, 3, 5, 7]
    elif letterAmount == 6: placement = [0, 2, 3, 5, 6, 8]
    elif letterAmount == 7: placement = [0, 1, 2, 3, 5, 7, 8]
    elif letterAmount == 8: placement = [0, 1, 2, 3, 5, 6, 7, 8]
    elif letterAmount == 9: placement = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    grid = baseGrid
    for letter, spot in zip(letters, placement):
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
            space = ''.join([" " for x in range(len(word), maxLength)])
            if wordIndex % 4 == 3: display.append(f"{answerUsed[wordIndex]}{space}  \n             ")
            else: display.append(f"{answerUsed[wordIndex]}{space}  ")
        print(f"{''.join(display)}")

        display = ["\n"]
        leftSide = ["⎡", "⎢", "⎣"]
        rightSide = ["⎤", "⎥", "⎦"]
        for index, spot in enumerate(grid):
            if index in [0, 3, 6]:
                display.append(leftSide[int(index/3)])
            display.append(f"  {spot}  ")
            if index in [2, 5, 8]:
                display.append(rightSide[int((index-2)/3)] + "\n")
        print(''.join(display))            
        
        while True:
            answer = str(input("> "))
            if answer == "/exit":
                print("You've ended the game prematurely!")
                menu()
            elif answer == "/giveup":
                print("You stopped the game!")
                break
            elif answer == "/shuffle":
                break
            answer = answer.upper()
            if any(answer.count(i) not in range(0, letters.count(i)+1) for i in answer):
                print(f"'{answer}' has an invalid letter! Try again.")
                continue
            elif len(answer) < 3:
                print(f"Your word was too short! Try again.")
            elif answer not in allPossibleWords:
                print(f"'{answer}' does not exist in the selected dictionary! Try again.")
                continue
            elif answer in answerUsed:
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

    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historyLines = [
        f"[{currentTime}] Combiner - {mode}",
        f"> Guesses: ({len(answerUsed)}) {', '.join(answerUsed)}",
        f"> All possible: ({len(allPossibleWords)}) {', '.join(allPossibleWords)}\n\n"
        ]
    with open("gameHistory.txt", "a", encoding="utf8") as history:
        history.write('\n'.join(historyLines))
            
    menu()

## --------------- UNSCRAMBLE ---------------
    
def unscramble():
    print(
        "\n"
        "--------------\n"
        "| Unscramble |\n"
        "--------------\n"
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
        keyword = random.choice(wordList).upper()
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
            if answer == "/exit":
                print("You've ended the game prematurely!")
                menu()
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

    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historyLines = [
        f"[{currentTime}] Unscrambled - {difficulty}",
        f"> Solution{plural}: {', '.join(keywords)}",
        f"> Guesses: ({len(answerList)}/{len(answerUsed)} correct) {', '.join(answerUsed)}\n\n"
        ]
    with open("gameHistory.txt", "a", encoding="utf8") as history:
        history.write('\n'.join(historyLines))

    menu()

## --------------- TRACEBACK --------------- 

def traceback():
    print(
        "\n"
        "-------------\n"
        "| Traceback |\n"
        "-------------\n"
        "Difficulties: [1] Easy (4 letters, min 2 correct)\n"
        "              [2] Medium (5 letters, 1-2 correct)\n"
        "              [3] Hard (6 letters, 1 valid)\n"
        "              [4] Fucked (7-9, guaranteed no valid)\n"
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
            print("\n--- DIFFICULTY : FUCKED ---\n")
            difficulty = "Fucked"
        break

    while True:
        keyword = random.choice(wordList)
        if difficulty == "Easy" and len(keyword) != 4:
            continue
        elif difficulty == "Medium" and len(keyword) != 5:
            continue
        elif difficulty == "Hard" and len(keyword) != 6:
            continue
        elif difficulty == "Fucked" and not len(keyword) not in range(7, 10):
            continue
        break

    while True:
        starterWord = random.choice(wordList)
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
        elif difficulty == "Fucked" and checker.count("?") != 0 and checker.count("!") != 0:
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
            if userInput == "/exit":
                print("You've ended the game prematurely!")
                menu()
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

        if answer == "/giveup":
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

        if checkerList[-1].count("!") > checkerList[-2].count("!") and answer.lower() in wordList:
            totalGuesses += 1
            print(f"Nice work! You got an extra guess (total: {totalGuesses}).")
        elif checkerList[-1].count("!") > checkerList[-2].count("!") and answer.lower() not in wordList:
            print(f"You found a correct letter, but the word is invalid! (total: {totalGuesses}).")
        elif answer.lower() not in wordList:
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

    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historyLines = [
        f"[{currentTime}] Traceback - {difficulty}",
        f"> Solution & starter: {keyword}, {starterWord}",
        f"> Guesses: ({guessNumber-1}/{totalGuesses}) {', '.join(answerList)}\n\n"
        ]
    with open("gameHistory.txt", "a", encoding="utf8") as history:
        history.write('\n'.join(historyLines))
    
    menu()


# Initialise game

if __name__ == "__main__":
    menu()
