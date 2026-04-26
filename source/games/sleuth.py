### --------------- MODULES ---------------

from datetime import datetime
import random
from resources.word_finder import wordFinder

### --------------- INFO ---------------

name = "Sleuth"
creator = "RandomMaerks"
description = "Find all given words hidden inside a grid of letters."
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
        "* Enter your filter (AVOID IF POSSIBLE) [words, rows, columns, minLength, maxLength]\n"
        "(default: 10 -1 -1 -1 -1, -1 = not set or variable):"
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
    
    defaultFilters = [10, -1, -1, -1, -1]
    filters = [
        int(inputtedFilters[i]) if i < len(inputtedFilters) else
        int(defaultFilters[i])
        for i in range(5)
        ]
    words = filters[0] if filters[0] >= 1 else 10
    minLength = filters[3] if filters[3] != -1 else 1
    maxLength = filters[4] if filters[4] != -1 else 100
    
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
    directions = ["horizontal", "vertical", "diagonaldown", "diagonalup"]

    keywords = []
    while True:    
        keyword = random.choice(context.wordList).upper()
        if keyword in keywords:
            continue
        if len(keyword) < minLength or len(keyword) > maxLength:
            continue
        keywords.append(keyword)
        if len(keywords) == words:
            break
    foundIndicator = [" " for _ in keywords]
    
    maxLength = max([len(keyword) for keyword in keywords])
    if filters[1] == -1: rows = 10 if maxLength <= 8 else maxLength+2
    else: rows = filters[1]
    cols = rows if filters[2] == -1 else filters[2]
    
    grid = [
        ["_" for _ in range(cols)]
        for _ in range(rows)
        ]

    def printGrid(thisGrid: list):
        print()
        maxLengthRow = max([len(str(row)) for row in range(1, rows+1)])
        maxLengthCol = max([len(str(col)) for col in range(1, cols+1)])
        space1 = " " * (maxLengthRow)
        display = [f"{space1}  "]
        for col in range(cols):
            space2 = " " * (maxLengthCol - len(str(col+1)))
            display.append(f"{col+1}{space2} ")
        print(''.join(display))
        for row in range(rows):
            space3 = " " * (maxLengthRow - len(str(row+1)))
            print(f"{space3}{row+1}  " + "  ".join(thisGrid[row]))
        print()
    
    wordIndex = 0
    while wordIndex < len(keywords):
        keyword = keywords[wordIndex]
        wordLength = len(keyword)
        direction = random.choice(directions)
        
        while True:
            rowIndex = random.randrange(0, rows)
            colIndex = random.randrange(0, cols)
            if direction == "horizontal" and colIndex + wordLength > cols:
                continue
            elif direction == "vertical" and rowIndex + wordLength > rows:     
                continue
            elif direction == "diagonaldown" and (colIndex + wordLength > cols or rowIndex + wordLength > rows):
                continue
            elif direction == "diagonalup" and (colIndex + wordLength > cols or rowIndex - wordLength < 0):   
                continue
            break
        
        appropriateSpot = True        
        if direction == "horizontal":
            for colVar in range(colIndex, colIndex+wordLength):
                if grid[rowIndex][colVar] == "_": continue
                if grid[rowIndex][colVar] != keyword[colVar-colIndex]:
                    appropriateSpot = False
                    break
        elif direction == "vertical":
            for rowVar in range(rowIndex, rowIndex+wordLength):
                if grid[rowVar][colIndex] == "_": continue
                if grid[rowVar][colIndex] != keyword[rowVar-rowIndex]:
                    appropriateSpot = False
                    break
        elif direction == "diagonaldown":
            for colVar in range(colIndex, colIndex+wordLength):
                for rowVar in range(rowIndex, rowIndex+wordLength):
                    if colVar-colIndex != rowVar-rowIndex: continue
                    if grid[rowVar][colVar] == "_": continue
                    if grid[rowVar][colVar] != keyword[rowVar-rowIndex]:
                        appropriateSpot = False
                        break
        elif direction == "diagonalup":
            for colVar in range(colIndex, colIndex+wordLength):
                for rowVar in range(rowIndex, rowIndex+wordLength):
                    if colVar-colIndex != rowVar-rowIndex: continue
                    if grid[rowIndex+wordLength-rowVar+1][colVar] == "_": continue
                    if grid[rowIndex+wordLength-rowVar+1][colVar] != keyword[rowVar-rowIndex]:
                        appropriateSpot = False
                        break
        if not appropriateSpot:
            continue
                        
        if direction == "horizontal":
            for colVar in range(colIndex, colIndex+wordLength):
                grid[rowIndex][colVar] = keyword[colVar-colIndex]
        elif direction == "vertical":
            for rowVar in range(rowIndex, rowIndex+wordLength):
                grid[rowVar][colIndex] = keyword[rowVar-rowIndex]
        elif direction == "diagonaldown":
            for colVar in range(colIndex, colIndex+wordLength):
                for rowVar in range(rowIndex, rowIndex+wordLength):
                    if colVar-colIndex != rowVar-rowIndex: continue
                    grid[rowVar][colVar] = keyword[rowVar-rowIndex]
        elif direction == "diagonalup":
            for colVar in range(colIndex, colIndex+wordLength):
                for rowVar in range(rowIndex, rowIndex+wordLength):
                    if colVar-colIndex != rowVar-rowIndex: continue
                    grid[rowIndex+wordLength-rowVar+1][colVar] = keyword[rowVar-rowIndex]
        wordIndex += 1

    bareGrid = [row[:] for row in grid]

    for row in range(len(grid)):
        grid[row] = [
            random.choices(alphabet, weights, k=1)[0] if grid[row][j] == "_"
            else grid[row][j] for j in range(cols)
            ]

    def getWord(rowIndexStart, colIndexStart, rowIndexEnd, colIndexEnd):
        word = []

        flippedRow = False
        if rowIndexStart > rowIndexEnd:
            temp = rowIndexEnd
            rowIndexEnd = rowIndexStart
            rowIndexStart = temp
            flippedRow = True
            
        rowIndexes = [i for i in range(rowIndexStart, rowIndexEnd+1)]
        colIndexes = [i for i in range(colIndexStart, colIndexEnd+1)]

        maxBothIndexes = max(len(rowIndexes), len(colIndexes))
        if len(rowIndexes) < maxBothIndexes:
            rowIndexes = [rowIndexes[0] for _ in range(maxBothIndexes)]
        elif len(colIndexes) < maxBothIndexes:
            colIndexes = [colIndexes[0] for _ in range(maxBothIndexes)]

        if flippedRow:
            rowIndexes = [rowIndexes[maxBothIndexes-i-1] for i in range(maxBothIndexes)]

        for row, col in zip(rowIndexes, colIndexes):
            word.append(grid[row][col])

        return ''.join(word)
            

    foundWords = []
    plural = "" if words == 1 else "s"
    print(
        f"\nThere are {words} word{plural} hiding in this grid for you to find. Good luck!\n"
        f"Type two 'row.column' indexes to make a word (eg. 1.8 5.8 = {getWord(0, 7, 4, 7)}). Make sure the indexes are valid.\n"
        "Type /giveup to end and save progress, and /exit to end the game."
        )
    while True:
        printGrid(grid)
        display = ["Words to find: "]
        for index, keyword in enumerate(keywords):
            if index == 0:
                display.append(f"{keyword.upper()} {foundIndicator[index]}\n")
            else:
                display.append(f"               {keyword.upper()} {foundIndicator[index]}\n")
        print(''.join(display))

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
                bothIndexes = userInput.split(" ")
                start = str(bothIndexes[0]).split(".")
                end = str(bothIndexes[1]).split(".")
                
                rowIndexStart = int(start[0]) - 1
                colIndexStart = int(start[1]) - 1
                rowIndexEnd = int(end[0]) - 1
                colIndexEnd = int(end[1]) - 1
            except IndexError:
                print("Your indexes are incorrect. Try again.")
                continue
            except ValueError:
                print("Cannot read your indexes. Try again. (separate row and column indexes by a period/full-stop)")
                continue

            if colIndexStart > colIndexEnd:
                print("For the time being, you cannot select colStart > colEnd. Sorry! Try again.")
                continue
            if rowIndexStart != rowIndexEnd and colIndexStart != colIndexEnd:
                if abs(rowIndexEnd - rowIndexStart) != abs(colIndexStart - colIndexEnd):
                    print("Your indexes are incorrect! Try again.")
                    continue
            if rowIndexStart not in range(0, rows) or rowIndexEnd not in range(0, rows):
                print("Your row index is out of bound! Try again.")
                continue
            if colIndexStart not in range(0, cols) or colIndexEnd not in range(0, cols):
                print("You column index is out of bound! Try again.")
                continue
                
            answer = getWord(rowIndexStart, colIndexStart, rowIndexEnd, colIndexEnd)
            
            if answer in foundWords:
                print(f"'{answer}' has already been found! Try again.")
                continue
            if answer not in keywords and answer.lower() in context.wordList:
                print(f"'{answer}' is not meant to be found, but it is a valid word!")
                keywords.append(answer)
                foundIndicator.append(" ")
                break
            if answer not in keywords and answer not in context.wordList:
                print(f"'{answer}' is not one of the words to find! Try again.")
                continue

            print(f"Found '{answer}'!")
            break

        if userInput == "/giveup":
            break

        foundWords.append(answer)
        indexInKeywords = keywords.index(answer)
        foundIndicator[indexInKeywords] = "✓"

        if all(keyword in foundWords for keyword in keywords):
            print("Nice work! You found all the words!")
            break

    printGrid(bareGrid)
    print(
        f"\nYou found: {len(foundWords)}/{words} word{plural}!\n"
        f"Your word{plural}: {', '.join(foundWords)}\n"
        )

    boardDisplay = [f"({rows}×{cols}) "]
    space = " " * (len(boardDisplay))
    for index, i in enumerate(grid):
        if index == 0: boardDisplay.append(f"{' '.join(i)}")
        else: boardDisplay.append(f"\n{space}{' '.join(i)}")
    boardDisplay = ''.join(boardDisplay)
    lines = {
        "Board" : f"{boardDisplay}",
        "Guesses" : f"({len(foundWords)}/{words}) {', '.join(foundWords)}",
    }
    writeHistory(context.history, lines)