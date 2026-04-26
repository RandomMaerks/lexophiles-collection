### --------------- MODULES ---------------

from datetime import datetime
import random

### --------------- INFO ---------------

name = "Boggle"
creator = "RandomMaerks"
description = "Find as many words as possible from a grid of letters."
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

class grid():
    def __init__(self, wordList, rows, cols, setSeed):
        self.rows = rows
        self.cols = cols
        self.wordList = wordList
        self.allowedLetters = [
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M'
            ]

        self.weights = [
            2, 5, 14, 10, 11, 5, 8, 10, 11, 5,
            12, 10, 9, 5, 6, 6, 2, 2, 8,
            2, 4, 7, 4, 5, 10, 7
            ]

        self.letterScores = [
            13, 10, 1, 5, 4, 10, 7, 5, 4, 10,
            3, 5, 6, 10, 9, 9, 13, 13, 7,
            13, 11, 8, 11, 10, 5, 8
            ]

        self.setSeed = setSeed
        self.grid = self.createGrid()
        self.history = []
        self.score = 0
        self.wordScore = []

    def createGrid(self):
        random.seed(self.setSeed)
        letters = random.choices(
            self.allowedLetters,
            self.weights,
            k=self.cols * self.rows
            )
        return letters

    def displayGrid(self):
        print(f"\nScore: {self.score}  |  Words: {len(self.history)}")
        wordIndex = 0
        display = ["Used words:  "]
        maxLength = 0
        for word in self.history:
            if maxLength < len(word): maxLength = len(word)
        for wordIndex, word in enumerate(self.history):
            space = " " * (maxLength - len(word))
            if wordIndex % 4 == 3: display.append(f"{self.history[wordIndex]}{space}  \n             ")
            else: display.append(f"{self.history[wordIndex]}{space}  ")
        print(f"{''.join(display)}")
        display = '  '.join([str(col+1) for col in range(self.cols)])
        print(f"\n   {display}")
        for row in range(self.rows):
            display = ']['.join(
                [self.grid[x] for x in range(row*self.cols, row*self.cols + self.cols)]
                )
            print(f"{row+1} [{display}]")
        print()

    def getWord(self, userInput):
        if any(userInput.count(x) != 1 for x in userInput):
            return "Some of your indexes are repeated! Try again."
        if len(userInput) < 3:
            return "Not enough indexes! Try again."

        indices = []
        for x in userInput:
            index = [int(x[0]) - 1, int(x[1]) - 1]
            indices.append(index)

        for order in range(len(indices)):
            row = indices[order][0]
            col = indices[order][1]
            if row not in range(0, self.rows) or col not in range(0, self.cols):
                return "Indexes are out of bound! Try again."

        for order in range(len(indices) - 1):
            rowCurrent = indices[order][0]
            colCurrent = indices[order][1]
            rowNext = indices[order+1][0]
            colNext = indices[order+1][1]
            if not (abs(rowNext - rowCurrent) <= 1 and abs(colNext - colCurrent) <= 1):
                return "Indexes are invalid! Try again."
        
        word = []
        score = 0
        for index in indices:
            row = index[0]
            col = index[1]
            letter = self.grid[row*self.cols + col]
            score += self.letterScores[self.allowedLetters.index(letter)]
            word.append(letter)
        word = ''.join(word)
            
        if word in self.history:
            return f"{word} ({score}) has already been used! Try again."
        if word.lower() not in self.wordList:
            return f"{word} (0) does not exist in the selected dictionary! Try again."
        
        self.history.append(word)
        self.wordScore.append(score)
        self.score += score
        return f"Found {word} ({score}) ✓"

def run(context):
    displayTitle()

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
    maxScore = filters[2] if filters[2] != -1 else 2147283647
    maxWords = filters[3] if filters[3] != -1 else 2147283647
    seed = filters[4] if filters[4] != -1 else random.getrandbits(64)

    boggleGrid = grid(context.wordList, gridRows, gridCols, seed)

    print(
        "To make a word, enter your row-column combos (row-column as one number).\n"
        "Type /giveup to see the result, and /exit to end the game.\n"
        )
    boggleGrid.displayGrid()
    while True:
        userInput = str(input("> "))
        if not userInput: continue
        if userInput == "/exit":
            print("You've ended the game prematurely!")
            return
        elif userInput == "/giveup":
            print("You stopped the game!")
            break
        message = boggleGrid.getWord(userInput.split(" "))
        print(message)
        if "✓" not in message: continue

        if boggleGrid.score >= maxScore:
            print("You've reached the max score!")
            break
        if len(boggleGrid.history) >= maxWords:
            print("You've played all {maxWords} words!")
            break

        boggleGrid.displayGrid()

    guessDisplay = ', '.join(
        [f"{boggleGrid.history[i]} ({boggleGrid.wordScore[i]})" for i in range(len(boggleGrid.history))]
        )
    
    print(
        f"Your score: {boggleGrid.score}\n"
        f"Your letters: ({gridRows}×{gridCols}, seed: {boggleGrid.setSeed}) {' '.join(boggleGrid.grid)}\n"
        f"Your guesses: (Total: {boggleGrid.score}) {guessDisplay}"
        )

    lines = {
        "Grid" : f"({gridRows}×{gridCols}, seed: {boggleGrid.setSeed}) {' '.join(boggleGrid.grid)}",
        "Guesses" : f"(Total: {boggleGrid.score}) {guessDisplay}",
    }
    writeHistory(context.history, lines)