#!/usr/bin/env python
# Define your word list here with variable as wordlist
with open("English.txt", "r") as fr:
    wordlist = list(
        map(
            str.upper,
            filter(
                lambda word: len(word) == 5 and "'" not in word, fr.read().splitlines()
            ),
        )
    )

# Code Block 1
import random
from math import log
import matplotlib.pyplot as plt
import json
from wordfreq import word_frequency
from entropy_calc import entropy_calc

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

    print("filter_list size", len(filtered_list))

    guess = get_next_guess(filtered_list)

    return guess, filtered_list, gl_dict, bl_set, corpos_dict


def letter_filter(wordlist, bl_set={}, gl_dict={}, corpos_dict={}):
    # Filter words with bad letters absent from wordlist
    # Filter out the words with incorrect good letter positioning - 2 ranked letters
    # Filter words with good letters present in wordlist

    filtered_wordlist = wordlist

    if bl_set:
        filtered_wordlist = filter(
            lambda w: all(bltr not in w for bltr in bl_set), filtered_wordlist
        )

    if gl_dict:

        filtered_wordlist = filter(
            lambda w: all(gltr in w for gltr in gl_dict.values()),
            filtered_wordlist,
        )

        filtered_wordlist = filter(
            lambda w: all(w[gl_idx] != gl_val for gl_idx, gl_val in gl_dict.items()),
            filtered_wordlist,
        )

    if corpos_dict:
        filtered_wordlist = filter(
            lambda w: all(w[idx] == l for idx, l in corpos_dict.items()),
            filtered_wordlist,
        )

    return list(filtered_wordlist)


def get_wrd_maxentropy(entropylst, filtered_list):
    # TODO Complete this function

    for comb in entropylst:
        maxentropywrd = filter(
            lambda w: all(list(comb) for comb in entropylst), filtered_list
        )

    return maxentropywrd


LAYERS_KEY = "LAYERS_"


def get_next_guess(filtered_list):
    # search wordlist for correct pos words and get the ones with maximum matches
    # TODO: Guess using either MRD or GEP strategy

    # print(filtered_list)
    if len(set(filtered_list)) == 1:
        return filtered_list[0]

    lookahead_feasible = len(filtered_list) < 50

    if not lookahead_feasible:
        layer = build_tree(
            filtered_list,
            recurse=0,
            complete_wordlist=True,
        )
        greedy_branch = sorted(
            layer.items(),
            key=lambda p: (
                p[1].get(LAYERS_KEY),
                -(len(p[1])/p[1].get(LAYERS_KEY)),
                -word_frequency(p[0], "en"),
            ),
        )[0]
        greedy_word = greedy_branch[0]
        # max_layers = greedy_branch[1][LAYERS_KEY]
        return greedy_word

    layer = build_tree(
        filtered_list,
        recurse=5 if len(filtered_list) < 25 else 3,
        complete_wordlist=False,
    )
    branch = sorted(
        layer.items(),
        key=lambda p: (
            p[1][LAYERS_KEY],
            -(len(p[1])/p[1].get(LAYERS_KEY)),
            -word_frequency(p[0], "en"),
        ),
    )[0]
    guess = branch[0]
    c_layers = branch[1][LAYERS_KEY]
    # print(f"Layers : {layers}")

    layer = build_tree(
        filtered_list,
        recurse=1,
        complete_wordlist=True,
    )
    greedy_branch = sorted(
        layer.items(),
        key=lambda p: (
            p[1].get(LAYERS_KEY),
            -(len(p[1])/p[1].get(LAYERS_KEY)),
            word_frequency(p[0], "en"),
        ),
    )[0]

    greedy_word = greedy_branch[0]
    wl_layers = greedy_branch[1][LAYERS_KEY]

    return (
        guess
        if (c_layers <= wl_layers)
        else guess
        if len(filtered_list) < 4
        else greedy_word
    )


def build_tree(corpus, recurse=2, complete_wordlist=False):
    # TODO: we are only trying to look at corpus for further guesses. Maybe
    # check with the whole dictionary?
    if len(corpus) == 1:
        return {LAYERS_KEY: 0}
    tree_layer = {}
    guesses = (
        filter(lambda word: len(set(word)) == 5, wordlist)
        if complete_wordlist
        else corpus
    )
    for guess in guesses:
        tree_node = {}
        if recurse:
            for word in corpus:
                matcher = fn_Matcher(word, guess)
                if matcher not in tree_node:
                    tree_node[matcher] = [word]
                else:
                    tree_node[matcher].append(word)
        else:
            for word in corpus:
                matcher = fn_Matcher(word, guess)
                if matcher not in tree_node:
                    tree_node[matcher] = {"COUNTS_": 1}
                else:
                    tree_node[matcher]["COUNTS_"] += 1

            # guesstimating the number of layers here based on num of nodes left
            layer_counts = []
            for matcher in tree_node:
                c = tree_node[matcher]["COUNTS_"]
                # layer_counts.append(c)
                # print(tree_node)
                layer_counts.append(c * log(c, len(tree_node) + 1))
            tree_node[LAYERS_KEY] = max(layer_counts) + 1

        # Recursion here
        if recurse:
            layers_counts = []
            for key in tree_node:
                tree_node[key] = build_tree(
                    tree_node[key],
                    recurse=(recurse - 1),
                    complete_wordlist=False,
                )
                if LAYERS_KEY in tree_node[key]:
                    layers_counts.append(tree_node[key][LAYERS_KEY] + 1)
                elif isinstance(tree_node[key], dict):
                    for v in tree_node[key].values():
                        layers_counts.append(v.get(LAYERS_KEY) + 1)

            tree_node[LAYERS_KEY] = max(layers_counts)
        tree_layer[guess] = tree_node
    return tree_layer


def input_gen(wordlist):
    return random.choice(wordlist).upper()


def stat(res):
    print("Output Stats ===> ", res)
    print("Average attempts: " + str(float(sum(res) / len(res))))
    plt.hist(res)
    plt.title("Average attempts: " + str(float(sum(res) / len(res))))
    plt.show()


# Custom Main function
if __name__ == "__main__":

    # Stat Results
    res = []

    # with open("English.txt", "r") as fr:
    #     wordlist = list(
    #         map(str.upper, filter(lambda word: len(word) == 5, fr.read().splitlines()))
    #     )

    for _ in range(20):

        corpos_dict = {}  # Correct position dict
        gl_dict = {}  # Good letters dict
        bl_set = set()  # Bad letters set
        corpus = wordlist.copy()

        theWord = input_gen(wordlist)
        print("Word of the Day is", theWord)

        while len(theWord) != 5 or (theWord not in wordlist):
            theWord = (input('"Please input a valid 5 letter word: ')).upper()
        for i in range(60):
            if i == 0:
                nextGuess = random.choice(["CRANE", "CRATE", "TRACE"])
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

# Main (Single)
# corpos_dict = {}  # Correct position dict
# gl_dict = {}  # Good letters dict
# bl_set = set()  # Bad letters set
# corpus = wordlist.copy()

# if __name__ == "__main__":
#     theWord = "BEARS"
#     # theWord = input_gen(wordlist)
#     for i in range(6):
#         if i == 0:
#             nextGuess = "AROSE"
#         else:
#             nextGuess, corpus, gl_dict, bl_set, corpos_dict = fn_Wordle_Player(
#                 intMatcher, corpus, gl_dict, bl_set, corpos_dict
#             )
#             nextGuess = nextGuess.upper()
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
