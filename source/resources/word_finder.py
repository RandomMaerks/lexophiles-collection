from itertools import permutations
import random

def wordFinder(
    wordList,
    longest = False,
    wordLength = [None, None],
    order = None,
    unique = None,
    restriction = [None, None, None],
    pattern = [None, None, None, None],
    excluded = []
    ):

    if len(wordList) < 1:
        return ["No dictionary selected, cannot find words\n\n", 0]
    
    foundWords = []
    longestWords = [""]
    
    for word in wordList:
        # Word length: min, max
        if wordLength[0] is not None and len(word) < wordLength[0]:
            continue
        if wordLength[1] is not None and len(word) > wordLength[1]:
            continue
        
        # Alphabetical order: None = no order, 'reversed' = reversed order, anything else = default
        if order:
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            if order == "reversed": alphabet = ''.join([alphabet[25-i] for i, x in enumerate(alphabet)])
            ref = alphabet
            inOrder = True
            for char in word:
                if char in ref:
                    index = ref.find(char)
                    ref = ref[index:]
                else:
                    inOrder = False
                    break
            if inOrder != True:
                continue
        
        # Unique / duplicate: None = skipped
        if unique == "unique":
            isUnique = True
            for charIndex, char in enumerate(word):
                removed = word[:charIndex] + word[charIndex+1:]
                if char in removed:
                    isUnique = False
                    break
            if isUnique != True:
                continue
        if unique == "duplicate":
            isDuplicate = True
            for charIndex, char in enumerate(word):
                removed = word[:charIndex] + word[charIndex+1:]
                if char not in removed:
                    isDuplicate = False
                    break
            if isDuplicate != True:
                continue
        
        # Letter restriction: [include, only include, avoid]
        if restriction[0] is not None and not all(restriction[0][i] in word for i in range(len(restriction[0]))):
            continue
        if restriction[1] is not None and any(word.count(i) not in range(0, restriction[1].count(i)+1) for i in word):
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
        
        if all(len(longestWords[i]) < len(word) for i in range(len(longestWords))):
            longestWords = []
            longestWords.append(word)
        elif any(len(longestWords[i]) == len(word) for i in range(len(longestWords))):
            longestWords.append(word)
        foundWords.append(word)

    if len(foundWords) > 0:
        if longest == True: return longestWords
        else: return foundWords
    else:
        return []