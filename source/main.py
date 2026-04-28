import importlib
import pkgutil

wordList = []
running = True

### --------------- GAME CONTEXT ---------------

class GameContext:
    def __init__(self, wordList):
        self.wordList = wordList
        self.history = "resources/gameHistory.txt"
    
### --------------- LOADING GAMES ---------------

def loadGames():
    games = []

    package_name = "games"
    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        if hasattr(module, "run"):
            games.append(module)

    return games

### ---------------  MENU --------------- 

def menu():
    global wordList
    global running

    if not wordList:
        wordList = chooseDict(indexDict = 2)

    print(
        "\n"
        "++------------------------------------------++\n"
        "||          LEXOPHILE'S COLLECTION          ||\n"
        "||                                          ||\n"
        "||          > Version: 2.0.0                ||\n"
        "++------------------------------------------++\n"
        "[1] Play      : Choose a game to play         \n"
        "[2] Dictionary: Choose a dictionary           \n"
        "[3] History   : View game history             \n"
        "[4] About     : View game details and credits \n"
        "[5] Exit      : Exit game                     \n"
        )

    print("* Choose mode (int):")
    while True:
        try:
            selection = int(input("> "))
        except Exception:
            print("Invalid input. Try again.")
            continue

        if selection not in range(1, 6):
            print("Not an option. Try again.")
            continue

        break

    if selection == 1: play()
    elif selection == 2: wordList = chooseDict()
    elif selection == 3: history()
    elif selection == 4: about()
    elif selection == 5: running = False

### --------------- PLAY ---------------

def play():
    global context

    print(
        "\n"
        "+------+\n"
        "| Play |\n"
        "+------+"
        )

    context.wordList = wordList
    games = loadGames()

    if len(games) == 0:
        print(
            "No games loaded.\n"
            "(Your custom game is in the '/games' folder? "
            "It needs a run() function to be found.)"
            )

        return

    plural = "s" if len(games) != 1 else ""
    print(f"Loaded {len(games)} game{plural}:\n")

    for i, game in enumerate(games):
        indexDisplay = str(i+1)
        print(
            f"[{indexDisplay}] "
            f"{getattr(game, 'name', 'Unnamed')} "
            f"(version: {getattr(game, 'version', '1')}) "
            f"(creator: {getattr(game, 'creator', 'Unknown')})\n"
            f"{' '*len(indexDisplay)}   {getattr(game, 'description', '')}\n"
            )

    print("* Choose game (int):")
    while True:
        try:
            choice = int(input("> ")) - 1
        except Exception:
            print("Invalid input. Try again.")
            continue

        if choice not in range(0, len(games)):
            print("Invalid game index. Try again.")
            continue

        break
    
    try:
        games[choice].run(context)
    except Exception as e:
        print(
            f"{getattr(games[choice], 'name', 'Unnamed')} has crashed!\n"
            f"{repr(e)}"
        )

### --------------- DICTIONARY --------------- 

def chooseDict(indexDict = None):
    dictionaries = {
        1: "dictionaries/wlist_match1.txt",
        2: "dictionaries/words_alpha.txt",
        3: "dictionaries/csw21.txt",
        4: "dictionaries/english_3000.txt",
        }

    if indexDict is not None:
        with open(dictionaries[indexDict], "r", encoding="utf8") as dictionary:
            wordList = dictionary.read().split("\n")

        return wordList

    print(
        "\n"
        "+--------------+\n"
        "| Dictionaries |\n"
        "+--------------+\n"
        "[1] wlist_match1.txt (Composed by Keith Vertanen, contains 1517K unfiltered words)\n"
        "[2] words_alpha.txt (Composed by dwyl, contains 370K unfiltered words)\n"
        "[3] CSW21 - Collins Scrabble Words (Contains 219K words)\n"
        "[4] english_3000.txt (Composed by EF, contains 3K most common English words)")

    print("* Choose dictionary (int):")
    while True:
        try:
            indexDict = int(input("> "))
        except Exception:
            print("Invalid index. Try again.")
            continue
        
        if indexDict not in range(1, len(dictionaries)+1):
            print("Not an option. Try again")
            continue

        break
        
    with open(dictionaries[indexDict], "r", encoding="utf8") as dictionary:
        wordList = dictionary.read().split("\n")

    return wordList

### --------------- PAST GAME HISTORY --------------- 
    
def history():
    print(
        "\n"
        "+---------+\n"
        "| History |\n"
        "+---------+\n"
        )

    with open(context.history, "r", encoding="utf8") as file:
        data = file.read().split("\n")
        for line in data:
            print(line)

### --------------- ABOUT SECTION --------------- 

def about():
    print(
        "\n"
        "+-------+\n"
        "| About |\n"
        "+-------+\n"
        "\n"
        "A simple collection of word games you can play\n"
        "on the terminal, now functioning as an inter- \n"
        "face for loading Python modules as word games!\n"
        "\n"
        "To import a game, place the .py file in the   \n"
        "'/games' folder. It should have global varia- \n"
        "bles named 'name' and 'description' to be dis-\n"
        "played nicely, and it must have a run() module\n"
        "to be able to load. For more information,     \n"
        "check the GitHub repository, link below.      \n"
        "\n"
        "Author: RandomMaerks (github.com/RandomMaerks)\n"
        "Version: 2.0.0                                \n"
        "Minimum requirements: Python 3.9              \n"
        "\n"
        "Dictionaries:                                 \n"
        "[1] wlist_match1.txt, 1.5M    (Keith Vertanen)\n"
        "[2] words_alpha.txt, 370K               (dwyl)\n"
        "[3] CSW21, 279K                      (Collins)\n"
        "[4] english_3000.txt, 3000                (EF)\n"
        "\n"
        "Repository:                                   \n"
        "github.com/RandomMaerks/lexophiles-collection \n"
    )

### --------------- MAIN --------------- 

def main():
    global context
    context = GameContext(wordList)

    while running:
        menu()

if __name__ == "__main__":
    main()
