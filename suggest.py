"""Module providing word counters."""
from collections import Counter
import sys

WORDLIST = []   # List of words we can attempt

def reduce(matched=',,,,', misplaced=',,,,', wrong=''):
    """Function to reduce wordlist based on previous guesses."""
    matched = matched.split(',')
    misplaced = misplaced.split(',')

    # Use only words with matched letters
    for i in range( len(WORDLIST) -1, -1, -1):
        word = WORDLIST[i]
        for j in range(5):
            if matched[j] != '' and matched[j] != word[j]:
                WORDLIST.remove(word)
                break

    # Remove words with any wrong letter
    wrong_set = set(wrong)
    for i in range( len(WORDLIST) -1, -1, -1):
        if wrong_set.intersection(WORDLIST[i]) != set():
            WORDLIST.pop(i)

    # Remove words with letters in the misplaced position
    for i in range( len(WORDLIST) -1, -1, -1):
        word = WORDLIST[i]
        for j in range(5):
            for k in range(len(misplaced[j])):
                if word[j] == misplaced[j][k]:
                    WORDLIST.pop(i)
                    break

    # Remove words without misplaced letters
    must_have = set("")
    for i in range(5):
        must_have.update( misplaced[i] )
    if len(must_have) == 0:
        return
    for i in range( len(WORDLIST) -1, -1, -1):
        if must_have.intersection(WORDLIST[i]) == set():
            WORDLIST.pop(i)

def recommend():
    """Function to show the best next guess."""
    any1 = Counter()
    position = [Counter(), Counter(), Counter(), Counter(), Counter()]

    for word in WORDLIST:
        for i in range(5):
            letter = word[i]
            any1[letter] += 1
            position[i][letter] += 1

    for i in range(5):
        print("#", i, position[i])
    print("Total", any1)

    max_value = 0
    for word in WORDLIST:
        value = 0
        for i in range(5):
            value += position[i][word[i]]
        if max_value < value:
            max_value = value
            print(word, value)

def main():
    """Function to intake prior guesses."""

    global WORDLIST # Global as we iterate to reduce possible words

    # CORRECT (green) should have no more than one letter per position
    correct = ',,,,'
    # MISPLACED (yellow) include all letters at that position
    misplaced = ',,,,'
    # WRONG (black) just list them any order
    wrong = ''

    # If args provided override all previous settings
    args = sys.argv[1:]
    if len(args) == 6:
        # Assumed command format: python suggest.py -c ",,,," -m ",,,," -w ""
        correct = args[1]
        misplaced = args[3]
        wrong = args[5]

    with open(r"solution_words", 'r', encoding='UTF-8') as fp:
        WORDLIST = fp.readlines()
        print('Total words:', len(WORDLIST))

    reduce(correct,misplaced,wrong)
    recommend()

if __name__ == "__main__":
    main()
