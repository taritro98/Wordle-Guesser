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
from wordfreq import word_frequency
from collections import Counter
from itertools import combinations

# import matplotlib.pyplot as plt

g_corpos_dict = {}  # Correct position dict
g_gl_dict = {}  # Good letters dict
g_bl_set = set()  # Bad letters set
g_corpus = wordlist.copy()

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

    ## Call tree or entropy algo
    guess = get_next_guess(filtered_list)
    # guess = get_next_guess_entropy(filtered_list)

    return guess


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




def weight_sum_dict(lst, wt_dict):
    """
    Sorts dict by weighted sum desc order
    TODO: Check whether return in sorted descending order
    Returns list of lists of desc order sorted dict [[],[]]
    """
    wtsum_dict = {}
    for comb in lst:
        wtsum_dict[comb] = sum(wt_dict[elem] for elem in comb)
    wtsum_dict_sorted = dict(
        sorted(wtsum_dict.items(), key=lambda item: item[1], reverse=True)
    )
    wtsumlst = [
        list(wtsum_dict_sorted_tuple) for wtsum_dict_sorted_tuple in wtsum_dict_sorted
    ]
    return wtsumlst


def gen_comb(ltr_count_list):
    """
    Input : [(key,val)]
    Generate weighted combinations
    """
    max_len = 5
    comb_lst = []

    # Weight dictionary
    wt_dict = {k: v for k, v in ltr_count_list}

    # Run loop in desc order to gen combinations from maxlen to 1
    while max_len > 0:
        if max_len == 5:
            comb = [lset[0] for idx, lset in enumerate(ltr_count_list)]
            comb = ["".join(comb)]
        else:
            comb = [lset[0] for idx, lset in enumerate(ltr_count_list)]
            # Generate x length combinations and desc sort by weight
            wtsum_lst = weight_sum_dict(list(combinations(comb, max_len)), wt_dict)
            comb = list(map(lambda x: "".join(x), wtsum_lst))

        comb_lst.extend(comb)

        max_len -= 1

    return comb_lst


def entropy_calc(wordlist):
    """
    Input wordlist : list
    Returns highest to lowest word freq combinations : list of lists
    """
    rem_dup = list(map(lambda x: "".join(set(x)), wordlist))
    ltr_count_list = Counter("".join(rem_dup)).most_common(5)
    most_com_ltrcombs = gen_comb(ltr_count_list)
    return most_com_ltrcombs


def get_wrd_maxentropy(entropylst, filtered_list):
    """
    Iterates through filtered list and returns word with highest correlation with most occurring chars
    Input : Word freq combination list, filtered list
    Output : Highest entropy word
    """
    for comb in entropylst:
        # Iterate through list high to low entropy combinations
        for maxentropywrd in filtered_list:
            if all([combl in maxentropywrd for combl in list(comb)]):
                # Break and return on detecting entropy word
                return maxentropywrd


def get_next_guess_entropy(filtered_list):
    """
    Call entropy calc and get maxentropy word functions and return max entropy word guess, else return max occurring word
    """
    entropylst = entropy_calc(filtered_list)
    nextguess = get_wrd_maxentropy(entropylst, filtered_list)

    if nextguess:
        return nextguess

    # Else return highest occurring word
    return sorted(filtered_list, key=lambda a: word_frequency(a, "en"))[-1]


LAYERS_KEY = "LAYERS_"


def get_next_guess(filtered_list):
    # search wordlist for correct pos words and get the ones with maximum matches
    # TODO: Guess using either MRD or GEP strategy

    if len(filtered_list) == 1:
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
                -(len(p[1]) / p[1].get(LAYERS_KEY)),
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
            -(len(p[1]) / p[1].get(LAYERS_KEY)),
            -word_frequency(p[0], "en"),
        ),
    )[0]
    guess = branch[0]
    c_layers = branch[1][LAYERS_KEY]

    layer = build_tree(
        filtered_list,
        recurse=1,
        complete_wordlist=True,
    )
    greedy_branch = sorted(
        layer.items(),
        key=lambda p: (
            p[1].get(LAYERS_KEY),
            -(len(p[1]) / p[1].get(LAYERS_KEY)),
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
    # print("Output Stats ===> ", res)
    # print("Average attempts: " + str(float(sum(res) / len(res))))
    # plt.hist(res)
    # plt.title("Average attempts: " + str(float(sum(res) / len(res))))
    # plt.show()
    pass


if __name__ == "__main__":

    theWord = input("Enter word of the day: ").upper()
    while len(theWord) != 5 or (theWord not in wordlist):
        theWord = (input('"Please input a valid 5 letter word: ')).upper()
    for i in range(6):
        if i == 0:
            nextGuess = random.choice(["CRANE", "CRATE", "TRACE"])
        else:
            nextGuess = fn_Wordle_Player(
                intMatcher, g_corpus, g_gl_dict, g_bl_set, g_corpos_dict
            ).upper()

        if (
            nextGuess in wordlist and len(nextGuess) == 5
        ):  # wordlist defined by participant above
            if nextGuess == theWord:
                print(nextGuess)
                print("Word found on attempt ", i + 1)
                break
            else:
                intMatcher = fn_Matcher(theWord, nextGuess)
                print(nextGuess)
                print("Word does not match, Feedback pattern returned :", intMatcher)
        else:
            print(nextGuess, "Not a valid word")
            break
    else:
        print("Word not found. Correct word is", theWord)
