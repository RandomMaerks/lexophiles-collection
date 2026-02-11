from itertools import permutations
import random
import dictionary_selector

def wordFinder(wordList, wordLength, order, unique, restriction, pattern, excluded):
    # list[strings], list[index, int, int], index, index, list [string x3], list[string x 4], list[strings]
    if len(wordList) < 1:
        return ["No dictionary selected, cannot find words\n\n", 0]
    
    foundWords = []
    longestWords = [""]
    for word in wordList:
        # Word length
        if wordLength[1] != -1 and len(word) < wordLength[1]:
            continue
        if wordLength[2] != -1 and len(word) > wordLength[2]:
            continue
        
        # Alphabetical order
        if order != 0:
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            if order == 2: alphabet = ''.join([alphabet[25-i] for i, x in enumerate(alphabet)])
            ref = alphabet
            inAlpOrder = True
            for char in word:
                if char in ref:
                    index = ref.find(char)
                    ref = ref[index:]
                else:
                    inAlpOrder = False
                    break
            if inAlpOrder != True:
                continue
        
        # Unique / duplicate
        if unique == 1:
            isUnique = True
            for charIndex, char in enumerate(word):
                removed = word[:charIndex] + word[charIndex+1:]
                if char in removed:
                    isUnique = False
                    break
            if isUnique != True:
                continue
        if unique == 2:
            isDuplicate = True
            for charIndex, char in enumerate(word):
                removed = word[:charIndex] + word[charIndex+1:]
                if char not in removed:
                    isDuplicate = False
                    break
            if isDuplicate != True:
                continue
        
        # Letter restriction
        if restriction[0] != "" and not all(restriction[0][i] in word for i in range(len(restriction[0]))):
            continue
        #if restriction[1] != "" and not all(word[i] in restriction[1] for i in range(len(word))):
        if restriction[1] != "" and any(word.count(i) not in range(0, restriction[1].count(i)+1) for i in word):
            continue
        if restriction[2] != "" and not all(restriction[2][i] not in word for i in range(len(restriction[2]))):
            continue
        
        # Pattern
        if pattern[0] != "" and not word.startswith(pattern[0]):
            continue
        if pattern[1] != "" and not word.endswith(pattern[1]):
            continue
        if pattern[2] != "" and not pattern[2] in word:
            continue
        if pattern[3] != "":
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
        if wordLength[0] == 0: return ['\n'.join(foundWords) + "\n\n", len(foundWords)]
        elif wordLength[0] == 1: return ['\n'.join(longestWords) + "\n\n", len(longestWords)]
    else:
        return ["No words found\n\n", 0]
    

def randomiseWord(wordList, excluded):
    # list [strings], list [strings]
    if len(wordList) == 0:
        return "No word in word list, cannot randomise\n\n"
    if all(wordList[i] in excluded for i in range(len(wordList))):
        return "All words in the word list are excluded, cannot randomise\n\n"
    while True:
        word = random.choice(wordList)
        if word in excluded:
            continue
        else:
            return word + "\n\n"

def main():
    pass

if __name__ == "__main__":
    main()
