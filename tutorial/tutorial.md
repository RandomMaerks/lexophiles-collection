# How to make a game for Lexophile's Collection

This is a guide on how you can make your own word game that can be picked up and run by the Lexophile's Collection interface.

This guide assumes you know a little bit about Python and coding in general.

## Structure

Your game must be a Python module with the `.py` file extension and it must have a `run()` function (including `context` as an argument). If not, LC will ignore it entirely.

Generally, you can structure your module like this:

```py
name = ""
creator = ""
description = ""
version = ""

def run(context):
    # your whole game here
```

It should have the variables `name` for game name, `creator` for creator name, `description` for a small description of the game, and `version` for the game version. These things will be picked up and displayed by the interface.

Technically, you can kind of put anything in the `run()` function. You can put a script that runs Doom, or maybe one that is a virus and steals logins... maybe don't do that please. i'm just saying, be careful of what you download online.

Anyway, if you want something similar to games that I made, you can use this structure here, seen from `game.py`:

```py
### --------------- MODULES ---------------

from datetime import datetime

### --------------- INFO ---------------

name = ""
creator = ""
description = ""
version = ""

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

    # your whole game here

    lines = {
        "Title": "Information",
    }
    writeHistory(context.history, lines)
```

There are prebuilt functions that will display the information and save the game history in a specific way.

## Using the game context

The `context` argument seen in the `run()` function is a **Python class** with two things: the word list selected in the LC interface called `wordList`, and the directory for the history file called `history`.

`wordList` is a **Python list** of all the words seen in the selected dictionary. To use it, do `context.wordList`. For instance:

```py
import random

keyword = random.choice(context.wordList)
userInput = str(input("Guess the word: "))
if userInput == keyword: print("You guessed it right!")
```

If it bothers you that you have to include `context.` every time you want to use it, just assign it to a new variable, like:

```py
dictionary = context.wordList

keywords = random.choices(dictionary, k=3)
```

`history` is a string representing the relative directory of the game history file, which is `resources/gameHistory.txt`. To use it, do `context.history`. In the example structure, I use it in my prebuilt function:

```py
writeHistory(context.history, lines)
```

## `/giveup` and `/exit`

`/giveup` and `/exit` are two "commands" that allows the player to leave the game at their own will. `/giveup` will save the player's progress, and `/exit` will flat out leave without leaving a trace.

You can implement these commands whenever there's an input.

```py
userInput = str(input("> "))

if userInput == "/giveup":
    print("You gave up!")
    # some trigger to end the game and write to history
elif userInput == "/exit":
    print("You ended the game early!")
    # some other trigger to end the game and skip the writing to history part
```

If the command for user input is in the `run()` command, your `/exit` trigger can just be `return` (nothing after it).

These commands can actually be called whatever, but I name them like this in my games, and you should at least tell the players what they are and how they work if you want a different command name.

## Useful modules

There are many prebuilt Python modules you can use, such as:

- [`random`](https://docs.python.org/3/library/random.html): Generates pseudorandom numbers
    + `random.choice(seq)`: Choose a random element
    + `random.choices(population, k=)`: Choose k random elements
    + `random.shuffle(seq)`: Shuffle a sequence
- [`itertools`](https://docs.python.org/3/library/itertools.html): Creating iterators for efficient looping
    + `itertools.permutations(seq, r=)`
    + `itertools.combinations(seq, r=)`
- [`time`](https://docs.python.org/3/library/time.html): Time access and conversions
    + `time.time()`: Get current time in seconds since the epoch
    + `time.sleep(sec)`: Sleeps for sec

I've specifically picked these because I reckon they might be useful for word games, but there are a lot more you can choose. You don't need to install them, since these should come with your installation of Python.

You can also use other modules, but note that the players will need to install those modules / packages as well.