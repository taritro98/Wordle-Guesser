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
import itertools
import matplotlib.pyplot as plt
import numpy as np
import json
from wordfreq import word_frequency
from string import ascii_uppercase
from statistics import median
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

	## Call tree or entropy algo
    #guess = get_next_guess(filtered_list)
    guess = get_next_guess_entropy(filtered_list)

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
	'''
	Iterates through filtered list and returns word with highest correlation with most occurring chars
	Input : Word freq combination list, filtered list
	Output : Highest entropy word
	'''
	for comb in entropylst:
		# Iterate through list high to low entropy combinations
		for maxentropywrd in filtered_list:
			if all([combl in maxentropywrd for combl in list(comb)]):
				# Break and return on detecting entropy word
				return maxentropywrd

def get_next_guess_entropy(filtered_list):
	'''
	Call entropy calc and get maxentropy word functions and return max entropy word guess, else return max occurring word 
	'''
	print("Filtered list", filtered_list)
	entropylst = entropy_calc(filtered_list)
	nextguess = get_wrd_maxentropy(entropylst, filtered_list)

	if nextguess:
		return nextguess
	
	# Else return highest occurring word
	return sorted(filtered_list, key=lambda a : word_frequency(a, 'en'))[-1]

LAYERS_KEY = "LAYERS_"


def get_next_guess(filtered_list):
    # search wordlist for correct pos words and get the ones with maximum matches
    # TODO: Guess using either MRD or GEP strategy
    
    # hist = Counter( "".join(word_list) )
    if len(filtered_list) == 1:
        return filtered_list[0]

    if len(filtered_list) < 500:
        layer = build_tree(filtered_list, recurse=5 if len(filtered_list) < 25 else 1)
        branches = sorted(
            layer.items(),
            key=lambda p: (
                p[1].get(LAYERS_KEY, 99),
                -len(p[1]),
                word_frequency(p[0], "en"),
            ),
        )
        # print("BRANCHES: ", json.dumps(branches, indent=4))
        return branches[0][0]
        # print(json.dumps(layer, indent=4))

    print("Filtered list", filtered_list)

    # Guess highest occuring word
    nextguess = sorted(filtered_list, key=lambda a : word_frequency(a, 'en'))[-1]
    # return wordlist[0]
    # return random.choice(filtered_list)
    
    return nextguess
    
def random_words_from_list():
    # print(random.sample(list(filter(lambda w: 'H' in w.upper(), wordlist)), 5))
    return list(
        itertools.chain.from_iterable(
            map(
                lambda x: random.sample(
                    (list(filter(lambda w: x in w.upper(), wordlist))), 2
                ),
                ascii_uppercase,
            )
        )
    )


alphabet_wordlist = list(
    itertools.chain.from_iterable(
        map(
            lambda x: random.sample(
                (list(filter(lambda w: x in w.upper(), wordlist))), 1
            ),
            ascii_uppercase,
        )
    )
)


def build_tree(corpus, recurse=2):
    # TODO: we are only trying to look at corpus for further guesses. Maybe
    # check with the whole dictionary?
    if len(corpus) == 1:
        return {LAYERS_KEY: 0}
    tree_layer = {}
    for word in corpus:
        tree_node = {}
        for guess in corpus + (alphabet_wordlist if len(corpus) > 20 else []):
            val = fn_Matcher(word, guess)
            if val not in tree_node:
                tree_node[val] = [guess]
            else:
                tree_node[val].append(guess)
        # Recursion here
        if recurse:
            layers_counts = []
            for key in tree_node:
                tree_node[key] = build_tree(tree_node[key], recurse=(recurse - 1))
                # print("KKEY: ", key)
                if LAYERS_KEY in tree_node[key]:
                    layers_counts.append(tree_node[key][LAYERS_KEY] + 1)
                elif isinstance(tree_node[key], dict):
                    for k, v in tree_node[key].items():
                        # print(v.get(LAYERS_KEY, 99))
                        layers_counts.append(v.get(LAYERS_KEY, 99) + 1)
                        # for d in v.values():
                        #     print( d[LAYERS_KEY] )
                else:
                    layers_counts.append(99)

            tree_node[LAYERS_KEY] = median(layers_counts)
        tree_layer[word] = tree_node

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

    for _ in range(100):

        corpos_dict = {}  # Correct position dict
        gl_dict = {}  # Good letters dict
        bl_set = set()  # Bad letters set
        corpus = wordlist.copy()

        # wordlist = wordlist.copy()
        # theWord=input('Enter word of the day: ').upper()
        theWord = input_gen(wordlist)
        print("Word of the Day is", theWord)

        while len(theWord) != 5 or (theWord not in wordlist):
            theWord = (input('"Please input a valid 5 letter word: ')).upper()
        for i in range(60):
            if i == 0:
                # TODO: Initialization Function
                # nextGuess = random.choice(wordlist).upper()
                nextGuess = random.choice(["AROSE"])
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
#     theWord = "HOODS"
#     # theWord = input_gen(wordlist)
#     for i in range(6):
#         if i == 0:
#             nextGuess = "RESAT"
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
