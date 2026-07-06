from itertools import permutations
import random

def wordFinder(
    wordList: list,
    longest: bool = False,
    wordLength: list[int, int] = None,
    order: str | None = None,
    unique: str | None = None,
    restriction: list[str, str, str] = None,
    pattern: list[str, str, str, str] = None,
    excluded: list = None
    ) -> list:
    """
    Returns a list of words filtered out by the requirements from the input word list.

    Arguments:
    - longest (bool): Only the longest words get returned
    - wordLength (list[int, int]): Minimum and maximum length of words
    - order (str | None): `None` for no order, `reversed` for reversed order, and anything else for alphabetical
    - unique (str | None): `None` for default, `unique` for no duplicate, `duplicate` for only duplicates
    - restriction (list[str, str, str]): Letters that can be included, letters that can ONLY be used, and letters to avoid
    - pattern (list[str, str, str, str]): Start, end, contain, and pattern (use `.` to denote wildcards)
    - excluded (list): List of words to ignore entirely
    """

    if wordLength is None: wordLength = [None, None]
    if restriction is None: restriction = [None, None, None]
    if pattern is None: pattern = [None, None, None, None]
    if excluded is None: excluded = []

    if len(wordList) < 1:
        return ["No dictionary selected, cannot find words\n\n", 0]
    
    foundWords = []
    longestWords = []
    longestWords_length = 0
    
    for word in wordList:
        # Word length: min, max
        if wordLength[0] is not None and len(word) < wordLength[0]:
            continue
        if wordLength[1] is not None and len(word) > wordLength[1]:
            continue
        
        # Alphabetical order: None = no order, 'reversed' = reversed order, anything else = default
        if order:
            if order != 'reversed':
                inOrder = all(l[i] <= l[i+1] for i in range(len(l) - 1))
            else:
                inOrder = all(l[i] >= l[i+1] for i in range(len(l) - 1))
            if inOrder != True:
                continue
        
        # Unique / duplicate: None = skipped
        if unique == "unique" and not all(word.count(char) == 1 for char in word):
            continue
        if unique == "duplicate" and not all(word.count(char) > 1 for char in word):
            continue
        
        # Letter restriction: [include, only include, avoid]
        if restriction[0] is not None and not all(restriction[0][i] in word for i in range(len(restriction[0]))):
            continue
        if restriction[1] is not None and any(word.count(char) not in range(0, restriction[1].count(char)+1) for char in word):
            continue
        if restriction[2] is not None and not all(restriction[2][i] not in word for i in range(len(restriction[2]))):
            continue
        
        # Pattern: [start with, end with, contain, pattern]
        if pattern[0] is not None and not word.startswith(pattern[0]):
            continue
        if pattern[1] is not None and not word.endswith(pattern[1]):
            continue
        if pattern[2] is not None and not pattern[2] in word:
            continue
        if pattern[3] is not None:
            if len(word) != len(pattern[3]):
                continue
            if not all(pattern[3][i] == word[i] for i in range(len(pattern[3])) if pattern[3][i] != "."):
                continue
        
        # Excluded
        if len(excluded) > 0 and not word not in excluded:
            continue
        
        if len(word) > longestWords_length:
            longestWords = [word]
            longestWords_length = len(word)
        elif len(word) == longestWords_length:
            longestWords.append(word)
        foundWords.append(word)

    if longest == True: return longestWords
    else: return foundWords