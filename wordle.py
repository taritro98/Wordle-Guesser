#!/usr/bin/env python
# Define your word list here with variable as wordlist
with open("English.txt", "r") as fr:
    wordlist = list(
        map(str.upper, filter(lambda word: len(word) == 5, fr.read().splitlines()))
    )

# Code Block 1
import random
import matplotlib.pyplot as plt
import numpy as np
from wordfreq import word_frequency


# Matcher Function returns number code
# 1 - Letter exists and is in the right position
# 2 - Letter exists but is in the wrong position
# 3 - Letter is not present in the word


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


def fn_Wordle_Player(intmatcher, corpus, gl_dict, bl_set, corpos_dict):
    # participant logic for new guess
    # Code Block 2

    # Check for
    # 1. correct pos - 1 ,
    # 2. good words - 2 ,
    # 3. bad words - 3
    # and append into corresponding lists
    for ltr_idx, fdbk in enumerate(intmatcher):
        if fdbk == "1":
            corpos_dict[ltr_idx] = nextGuess[ltr_idx]
        elif fdbk == "2":
            gl_dict[ltr_idx] = nextGuess[ltr_idx]
        else:
            bl_set.add(nextGuess[ltr_idx])

    # Filter words with bad letters absent from wordlist
    filtered_list = letter_filter(
        corpus, bl_set=bl_set, gl_dict=gl_dict, corpos_dict=corpos_dict
    )
    print("length of filtered_list: ", len(filtered_list))


    guess = get_next_guess(corpos_dict, filtered_list)

    return guess, filtered_list, gl_dict, bl_set, corpos_dict


def letter_filter(wordlist, bl_set={}, gl_dict={}, corpos_dict={}):
    # Filter words with bad letters absent from wordlist
    # Filter out the words with incorrect good letter positioning - 2 ranked letters
    # Filter words with good letters present in wordlist

    filtered_wordlist = []

    if bl_set:
        filtered_wordlist = filter(
            lambda w: not any(bltr in w for bltr in bl_set), wordlist
        )

    if gl_dict:
        filtered_wordlist = filter(
            lambda w: not any(
                w[gl_idx] == gl_val for gl_idx, gl_val in gl_dict.items()
            ),
            filtered_wordlist,
        )

        filtered_wordlist = filter(
            lambda w: any(gltr in w for gltr in gl_dict.values()),
            filtered_wordlist,
        )

    if corpos_dict:
        filtered_wordlist = filter(
            lambda w: all(w[idx] == l for idx, l in corpos_dict.items()),
            filtered_wordlist,
        )

    return list(filtered_wordlist)


def get_next_guess(corpos_dict, filtered_list):
    # search wordlist for correct pos words and get the ones with maximum matches
    # TODO: Guess using either MRD or GEP strategy
    # word_list = list( filter( filter_using_alphabets, words))
    # hist = Counter( "".join(word_list) )

    
    return sorted(filtered_list, key=lambda a : word_frequency(a, 'en'))[-1]
    # return wordlist[0]
    # return random.choice(filtered_list)


def input_gen(wordlist):
    return random.choice(wordlist).upper()


def stat(res):
    print("Output Stats ===> ", res)
    plt.hist(res)
    plt.title("Average attempts: "+ str(float(sum(res)/len(res))))
    plt.show()


# Custom Main function
if __name__ == "__main__":

    # Stat Results
    res = []

    # with open("English.txt", "r") as fr:
    #     wordlist = list(
    #         map(str.upper, filter(lambda word: len(word) == 5, fr.read().splitlines()))
    #     )

    for _ in range(500):

        corpos_dict = {}    # Correct position dict
        gl_dict     = {}    # Good letters dict
        bl_set      = set() # Bad letters set
        corpus      = wordlist.copy()

        # wordlist = wordlist.copy()
        # theWord=input('Enter word of the day: ').upper()
        theWord = input_gen(wordlist)
        print("Word of the Day is", theWord)

        while len(theWord) != 5 or (theWord not in wordlist):
            theWord = (input('"Please input a valid 5 letter word: ')).upper()
        for i in range(6):
            if i == 0:
                # TODO: Initialization Function
                # nextGuess = random.choice(wordlist).upper()
                nextGuess = random.choice(["RESAT", "AROSE"])
            else:
                nextGuess, corpus, gl_dict, bl_set, corpos_dict = fn_Wordle_Player(
                    intMatcher, corpus, gl_dict, bl_set, corpos_dict
                )
                nextGuess = nextGuess.upper()

            if nextGuess in wordlist and len(nextGuess) == 5:
                if nextGuess == theWord:
                    print(f"Word {nextGuess} found on attempt ", i + 1)
                    res.append(i + 1)
                    break
                else:
                    intMatcher = fn_Matcher(theWord, nextGuess)
                    print(nextGuess)
                    print(
                        "Word does not match, Feedback pattern returned :", intMatcher
                    )
            else:
                print(nextGuess, "Not a valid word")
                break
        else:
            print("Word not found. Correct word is", theWord)
            res.append(10)

        print("")
        print("")
        print("")

    stat(res)

# Original Main
# if __name__ == "__main__":
#     theWord = input("Enter word of the day: ").upper()
#     while len(theWord) != 5 or (theWord not in wordlist):
#         theWord = (input('"Please input a valid 5 letter word: ')).upper()
#     for i in range(6):
#         if i == 0:
#             nextGuess = (
#                 "<firstguess>".upper()
#             )  # hardcode first guess or modify to generate guess  #Code Block 3
#         else:
#             nextGuess = fn_Wordle_Player(intMatcher).upper()
#         if (
#             nextGuess in wordlist and len(nextGuess) == 5
#         ):  # wordlist defined by participant above
#             if nextGuess == theWord:
#                 print(nextGuess)
#                 print("Word found on attempt ", i + 1)
#                 break
#             else:
#                 intMatcher = fn_Matcher(theWord, nextGuess)
#                 print(nextGuess)
#                 print("Word does not match, Feedback pattern returned :", intMatcher)
#         else:
#             print(nextGuess, "Not a valid word")
#             break
#     else:
#         print("Word not found. Correct word is", theWord)
