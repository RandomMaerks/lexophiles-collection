# 🧩🔠 Lexophile's Collection

A simple collection of word games you can play on whatever terminal or console you prefer!

Largely coded in Python (the only language I know to an intermediate level).

Small warning: The game occasionally uses box drawing characters which may not always be supported by a monospaced font, so make
sure you use one that does. I use [Iosevka](https://github.com/be5invis/Iosevka) (SS14, Extended) and I found 
[Cascadia Code](https://github.com/microsoft/cascadia-code) which also support these characters.

## How to run

Download everything in the source code (pls) and run the `LexophilesCollection.py` file. Simple as that!

## Functionality

Upon running the script, you will be met with the Menu screen, which will be your main navigation point.

<img width="823" height="317" alt="image" src="https://github.com/user-attachments/assets/a5db9698-e0bd-41c3-b0a0-b5edea0ddfe7" />

There are currently **11 modes**:

- The first 2 modes are reserved for the *Game history* and the *Choose dictionary* modes.
- The following modes are portals to games that you can play.

During the game, you can either type the required input, such as a word or an index, or you can use one of the two commands:
- The `/exit` command: End the game "prematurely" (for some reason I called it that) and return to the menu
- The `/giveup` command: Stop the game, but also show your progress and answers (if there are any) before returning to the menu

When you finish a game by either having achieved an end goal or activated the `/giveup` command, the game will automatically
append your result to the game history (saved in the `gameHistory.txt` file). Doing the `/exit` command won't save your result.

## Word games

There are **9 game concepts**:

| Mode | Game name | Description |
| :---: | --- | --- |
| 3 | Solobomber | Make a word using a letter combo or prompt.|
| 4 | Word Chain | Make a unique word using the last letter of the previous guess. |
| 5 | Wordle     | The New York Times Wordle, but with custom word length. |
| 6 | Hangman    | Find the word by guessing the correct letters. |
| 7 | Boggle     | Find as many words as possible from a grid of letters. |
| 8 | Sleuth     | Find all given words hidden inside a grid of letters. |
| 9 | Combiner   | Find all words given a set of letters. |
| 10 | Unscramble | Guess the correct word(s) from a jumbled set of letters. |
| 11 | Traceback | Find the original word from a set of word hints. |

### 1. Solobomber

In a game of Solobomber, you're given a series of letter combinations called "prompts". For each prompt, you must create a word
that can satisfy the following conditions:
- The word must contain the prompt, whether at the start, at the end or among other letters
- The word must be unique, meaning you cannot use it multiple times
- The word must exist in the selected dictionary

Additionally, you're given a maximum of 3 tries. You lose one try if you reuse a word.

The game simply ends when you run out of tries or you activate a command.

<img width="684" height="419" alt="image" src="https://github.com/user-attachments/assets/b20e45aa-e5d2-43db-9aa7-b872a621b5e4" />

Solobomber is inspired by JKLM's BombParty and OMG's Word Bomb from Roblox.

### 2. Word Chain

Word Chain is a game where you create a series of words by connecting the last letter of a previous word to the first letter of
the next word to make a "chain".

The conditions for making a word are similar to that of Solobomber:
- The new word must start with the last letter of the previous word
- The word is unique
- The word exists in the selected dictionary

And, just like Solobomber, you have a maximum of 3 tries. However, aside from reusing a word, making a word that doesn't start 
with the correct letter will also take away one try.

One unique thing about this game (compared to basically every other game) is that you can either play with yourself, or you can
battle a computer. There is a very miniscule chance the computer will not be able to find a word, so for the most part, you're 
guaranteed to lose at some point.

<img width="667" height="458" alt="image" src="https://github.com/user-attachments/assets/c06876f0-cd87-4a7f-9496-24d7f357e3b8" />

### 3. Wordle

If you've played TNYT Wordle, you're probably already familiar with how the game works. You get 6 tries, and you have to guess
the correct 5-letter word to win. Each guess will reveal which letter is invalid, which one is in the word but is in the wrong
place, and which one is correct and in the right place.

LC's implementation of this game is basically the same, except you have two modes:
- Classic: The answers are TNYT Wordle's past solutions, which limits the word length to 5 letters
- Custom: The answers are taken from the selected dictionary, allowing for words of any length

When you play Custom mode, the number of guesses grows with the length of the solution. Or, to be precise:
- totalGuesses = 6 if 1 ≤ wordLength ≤ 5
- else totalGuesses = wordLength + 1

If you selected a word whose length is greater than 15, the game nicely asks if you'd actually want to guess a word of that
length. You can take this moment to rethink your decision; but if you're feeling adventurous and a little bit brave, there's a
fat chance the game will either keep giving you the same set of words, or it will fall into an infinite loop.

<img width="387" height="343" alt="image" src="https://github.com/user-attachments/assets/051ddef2-53f8-4bfe-bbfa-3e8595ed3542" />

### 4. Hangman

Hangman is a remorseless simulation of a life-or-death situation where you try to find the correct word by guessing individual
letters.

<img width="672" height="422" alt="image" src="https://github.com/user-attachments/assets/eded86f4-3758-40fd-89f8-ee0cd417b9ba" />

By design of the hangman, you get a maximum of 6 guesses that corresponds to each segment of the man. For every wrong guess,
one of his body parts appears on the display.

If you get lucky, you will see him standing on the ground, arms raising above his head, celebrating, for you have saved his
life. Otherwise, you will be witnessing the painful scene of a man whose identity you may never know leave this plane of existence
right before your eyes.

<img width="342" height="132" alt="image" src="https://github.com/user-attachments/assets/8ac89f6c-f7d1-42f6-a511-48ace29a488a" />

You can also `/giveup` and leave half a man on the hanger and act like you never created a sentient being.

### 5. Boggle

This game gives you a 4×4 grid of random letters (by default). If the stars align correctly, you may be able to make a few
words by connecting some letters in the grid together.

However, you have to follow these specific rules:
- When you select a letter, you have to continue with the letters that surround it. For example, you can't start with a
letter on the top right and jump all the way to the bottom left to connect the letters
- You cannot select the same block of letter more than once
- You cannot make a word with only 1 or 2 letters

LC's implementation gives you a set of filters at the start of each game: Number of rows, columns, max score, max number of
words, and seed. The default option will be 4 rows, 4 columns, max score 100, infinite words, and no set seed.

When you end the game, you can actually see the game seed, and it will be saved in the game history. You can use this seed to
regenerate the grid.

One more thing: considering the only way to do anything is by typing strings of characters and command into the input field,
the user experience is a little bit janky. You have to type in the row-column index of a block of letter to "select" it.
Luckily, the grid display will show you the indexes, so you don't have to think much about them.

<img width="650" height="331" alt="image" src="https://github.com/user-attachments/assets/2e050d08-5ab5-4081-8171-5d5776edb097" />

### 6. Sleuth

Sleuth gives you a grid of random letters and a couple of words that you need to find inside the grid. Unlike Boggle, the words
are placed linearly, though they can be placed horizontally, vertically, and diagonally.

LC's implementation currently only has 4 directions: horizontal, vertical, diagonal up, and diagonal down. The words are never
placed in reverse order.

Like Boggle, there are a few filters you can use to get a specific board, but I would highly recommend against it since there is
a fat chance the game will fall into an infinite loop.

To select a word, you must type in two row-column indexes, with each pair of row and column number joined by a dot `.`. For example:
`1.10 5.10` selects vertically from row 1 to row 5 of column 10; `4.6 6.4` selects diagonally.

Sometimes, you might find a word that exists in the selected dictionary but is not a part of the intended word list. You'll actually
get to keep that word as a bonus.

<img width="442" height="608" alt="image" src="https://github.com/user-attachments/assets/d5139537-7378-4e30-9d0f-04cec4fccf1b" />

### 7. Combiner

In this game, you're given a set of letters with somewhere from 3 to 9 letters. You can make a word by picking out a few letters
and arrange them in a way that will form a valid word.

However, you must consider a few things:
- The number of letters used must not be more than the number of letters that is present in the letter set
- The words must have a minimum length of 3
- The words must be in the selected dictionary
- The words must be unique

LC's implementation has two modes you can choose:
- Simple: The randomiser takes a word from the dictionary and shuffles its letter, guaranteeing at least one valid solution
- Rogue: The randomiser takes letters at random, which might result in a game with no valid solutions

Also, this game uses a script to find all possible words in the dictionary, so you'll be able to see how many words you can
make. The game ends when you do find all of them.

<img width="443" height="231" alt="image" src="https://github.com/user-attachments/assets/e21bbdf9-b37a-438f-9f2b-4e882f5c22fb" />

### 8. Unscramble

Hopefully the name is self-explanatory. You get a word but it gets shuffled to hell, and you have to guess what the word is.

Lexophile's Collection takes a step further and gives you three levels of difficulty:
- Easy: One word gets shuffled
- Hard: Two words get mixed into each other, and you have to guess both of them
- Mess: There's a third one joining

You can only end the game once you've managed to guess all the words (or you can just use the commands).

<img width="506" height="523" alt="image" src="https://github.com/user-attachments/assets/c9aef867-d671-41f4-8c9f-16d4ae3868e7" />

### 9. Traceback

Traceback is a combination of two games: Word ladder & Wordle.

In Word ladder, (I think) you're given a start word and an end word. You try to turn one into the other by slowly replacing one
letter at a time, ensuring every word you make is a valid word. Wordle is explained above.

Traceback combines these two games by hiding the end word, and you're supposed to guess based on the indicator for each letter.
If a letter doesn't belong, it's gray. If it exists, it's yellow. If it's in the correct spot as well, it's green.

I don't fully take credit because I don't know if anyone has also done this before, but I'd like to say I thought of this all by
myself before I realise it's a combination of these two games.

LC's implementation gives you four levels of difficulty:
- Easy: The words are 4 letters long, and you get 2 valid letters in their correct spot
- Medium: The words are 5 letters long, and you get 1 to 2 valid letters in their correct spot
- Hard: The words are 6 letters long, and you get 1 valid letter MADE SURE NOT TO BE IN ITS CORRECT SPOT
- F*cked: The word length can be 7 to 9 letters, and you get NOTHING

To make a change, you type in an index-replacement combo. For example, you can turn HOLE into POLE by typing 1P (1: letter index,
P: letter replacement).

You get a total of (wordLength + 6) guesses before the game ends. Due to the nature of this game, it's pretty hard to make a
word that exists in the dictionary, so instead of not allowing you to continue, the game simply does this:
- Takes away one guess if you make a word that doesn't exist
- Gives you one guess if you manage to get one letter in its correct spot

<img width="799" height="550" alt="image" src="https://github.com/user-attachments/assets/2b351335-e458-4815-b09d-72dcb1a58ba4" />

## Dictionaries

I didn't make these dictionaries. Let's just make that clear.

These are the dictionaries / word lists I've included for the game:

### `wlist_match1.txt`
- Author: Keith Vertanen
- Words: 1516998
- Link: https://www.keithv.com/software/wlist/

### `words_alpha.txt`
- Author: dwyl
- Words: 370105
- Link: https://github.com/dwyl/english-words

### `wordlist.txt`
- Author: Florida State University
- Words: 300394
- Link: i forgot

### Collins Scrabble Words (CSW21) / `csw21.txt`
- Author: Collins
- Words: 279077
- Link (unofficial): https://www.reddit.com/r/scrabble/comments/my5tie/the_419_words_erased_from_csw/
https://dn710002.ca.archive.org/0/items/csw21/CSW21.txt

### `twl06.txt`
- Author: Free Scrabble Dictionary
- Words: 178691
- Link: https://www.freescrabbledictionary.com/twl06/download/twl06.txt

### `english_3000.txt`
- Author: EF
- Words: 3000
- Link: https://www.ef.com/wwen/english-resources/english-vocabulary/top-3000-words/

## Contribution

If you find any bugs, have any game suggestions, or want to improve some code, please make an issue or discussion and let me know!
