### --------------- MODULES ---------------

# You can use this section to include your own modules.
# Please don't remove the datetime module unless you want to customise the game history.

from datetime import datetime

### --------------- INFO ---------------

# Include the details of your game here.
# The name, creator, and description will show up in the LC interface.

name = ""
creator = ""
description = ""
version = ""

### --------------- FUNCTIONS ---------------

# These are prebuilt functions.
# Again, don't remove or modify them unless you want to customise them.

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

# This is the function that gets called by LC.
# It must be named `run` and must have the `context` argument.
# `context` is a class that contains the word list (context.wordList)
# and the history file directory (context.history).
# The prebuilt functions are in there too.
# displayTitle() will display the game information and must be put on top.
# writeHistory() will write to the gameHistory.txt file and must be put at the bottom.

def run(context):
    # If you don't want to mess with anything, just leave it as is.
    displayTitle()

    # You can use `wordList = context.wordList` to avoid having to type `context.`
    # Remove if you want.

    wordList = context.wordList

    # ---
    # Your code goes here

    

    # ---


    # Use the dict `lines` to display important info to save to the history.
    # For example, lines = {"Mode": f"{mode}",} will write `> Mode: whatever_mode_it_is` as a separate line.
    # Please don't include one for the game title. The `writeHistory()` function already does that for you.
    lines = {
        "Title": "Information",
    }
    writeHistory(context.history, lines)