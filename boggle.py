import random
from itertools import permutations

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
            space = ''.join([" " for x in range(len(word), maxLength)])
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
            return "Repeated"
        elif len(userInput) < 3:
            return "Word too short"

        indices = []
        for x in userInput:
            index = [int(x[0]) - 1, int(x[1]) - 1]
            indices.append(index)

        for order in range(len(indices) - 1):
            rowCurrent = indices[order][0]
            colCurrent = indices[order][1]
            rowNext = indices[order+1][0]
            colNext = indices[order+1][1]
            if not abs(rowNext - rowCurrent) <= 1 and abs(colNext - colCurrent) <= 1:
                return "Indices are invalid"
        
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
            return f"{word} ({score}) already used"
        elif word.lower() not in self.wordList:
            return f"{word} (0) does not exist in dictionary"
        
        self.history.append(word)
        self.wordScore.append(score)
        self.score += score
        return f"{word} ({score}) ✔"

if __name__ == "__main__":
    with open("dictionaries/wordlist.txt", "r", encoding="utf8") as dictionary:
        wordList = dictionary.read().split("\n")
        
    gridRows = 4
    gridCols = 4

    grid = grid(wordList, gridRows, gridCols, 1690143142815829899)

    while True:
        grid.displayGrid()
        userInput = str(input("> "))
        print(grid.getWord(userInput.split(" ")))
