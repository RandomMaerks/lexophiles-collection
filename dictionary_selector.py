dictionaryRef = [
    "",
    "dictionaries/wlist_match1.txt",
    "dictionaries/words_alpha.txt",
    "dictionaries/wordlist.txt",
    "dictionaries/twl06.txt",
    "dictionaries/english.txt",
    "dictionaries/english_3000.txt"
    ]

def dictionarySelector(indexDict):
    if indexDict == 0:
        return []
    else:
        with open(dictionaryRef[indexDict], "r", encoding="utf8") as file:
            wordList = file.read().split("\n")
        return wordList
