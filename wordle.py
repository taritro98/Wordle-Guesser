#!/usr/bin/env python

import random
import matplotlib.pyplot as plt
import numpy as np


def fn_Matcher(theWord, nextGuess):
    match = ""
    for i in range(5):
        if nextGuess[i] == theWord[i]:
            match += "1"
        elif nextGuess[i] in theWord:
            match += "2"
        else:
            match += "3"
    return match


def letter_filter(bl_list, gl_dict, wordlist):
    # Filter words with bad letters absent from wordlist
    # Filter out the words with incorrect good letter positioning - 2 ranked letters
    # Filter words with good letters present in wordlist
    nwordlist = []
    for word in wordlist:
        if (
            not any(bltr in word for bltr in bl_list)
            and not any(word[gl_idx] == gl_val for gl_idx, gl_val in gl_dict.items())
            and any(gltr in word for gltr in gl_dict.values())
        ):
            nwordlist.append(word)

    return nwordlist


# def gpos_unmatch(gl_dict, wordlist):
#   # Filter out the words with incorrect good letter positioning - 2 ranked letters
#   nwordlist = []
#   for word in wordlist:
#       if not any(word[gl_idx]==gl_val for gl_idx, gl_val in gl_dict.items()):
#           nwordlist.append(word)

#   return nwordlist


def corpos_match(corpos_dict, wordlist):
    # search wordlist for correct pos words and get the ones with maximum matches
    max_match = 0
    for wrd in wordlist:
        match = 0
        for cor_idx, cor_val in corpos_dict.items():
            if wrd[cor_idx] == cor_val:
                guess = wrd
                match += 1

        if match > max_match:
            max_match = match
            corpos_guess = guess

    return corpos_guess


def fn_Wordle_Player(intmatcher, wordlist, gl_dict, bl_list, corpos_dict):
    # Check for
    # 1. correct pos - 1 ,
    # 2. good words - 2 ,
    # 3. bad words - 3
    # and append into corresponding lists
    for ltr_idx, fdbk in enumerate(intMatcher):
        if fdbk == "1":
            corpos_dict[ltr_idx] = nextGuess[ltr_idx]
        elif fdbk == "2":
            gl_dict[ltr_idx] = nextGuess[ltr_idx]
        else:
            bl_list.append(nextGuess[ltr_idx])

    # Filter words with bad letters absent from wordlist
    if bl_list or gl_dict:
        print("bl_list", bl_list)
        print("gl dict", gl_dict)
        wordlist = letter_filter(bl_list, gl_dict, wordlist)

    # if gl_dict:
    #   wordlist = gpos_unmatch(gl_dict, wordlist)

    print("wordlist len", len(wordlist))

    # Guess first word from filtered wordlist as preliminary guess
    guess = wordlist[0]

    # If any correct positions guessed previously
    print("Correct pos dict is", corpos_dict)
    if corpos_dict:
        guess = corpos_match(corpos_dict, wordlist)

    return guess, wordlist, gl_dict, bl_list, corpos_dict


def input_gen(wordlist):
    return random.choice(wordlist)


def stat(res):
    print("Output Stats ===> ", res)
    # plt.hist(res)
    # plt.show()


if __name__ == "__main__":

    # Stat Results
    res = []

    with open("English.txt", "r") as fr:
        main_wordlist = list(
            map(str.upper, filter(lambda word: len(word) == 5, fr.read().splitlines()))
        )

    for _ in range(20):

        # Good letters dict
        gl_dict = {}
        # Bad letters list
        bl_list = []
        # Correct position dict
        corpos_dict = {}

        wordlist = main_wordlist.copy()
        # theWord=input('Enter word of the day: ').upper()
        theWord = input_gen(wordlist)
        print("Word of the Day is", theWord)

        while len(theWord) != 5 or (theWord not in wordlist):
            theWord = (input('"Please input a valid 5 letter word: ')).upper()
        for i in range(6):
            if i == 0:
                # TODO: Initialization Function
                nextGuess = random.choice(wordlist).upper()
            else:
                nextGuess, wordlist, gl_dict, bl_list, corpos_dict = fn_Wordle_Player(
                    intMatcher, wordlist, gl_dict, bl_list, corpos_dict
                )
                nextGuess = nextGuess.upper()
            if nextGuess in wordlist and len(nextGuess) == 5:
                if nextGuess == theWord:
                    print(nextGuess)
                    print("Word found on attempt ", i + 1)
                    res.append(i + 1)
                    break
                else:
                    intMatcher = fn_Matcher(theWord, nextGuess)
                    print(nextGuess)
                    print(
                        "Word does not match, Feedback pattern returned :", intMatcher
                    )

                    # Remove previously guessed word from wordlist
                    wordlist.remove(nextGuess)
            else:
                print(nextGuess, "Not a valid word")
                break
        else:
            print("Word not found. Correct word is", theWord)
            res.append(10)

    stat(res)
