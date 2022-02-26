import random

def fn_Matcher(theWord, nextGuess):
	match=''
	for i in range(5):
		if nextGuess[i]==theWord[i]:
			match+='1'
		elif nextGuess[i] in theWord:
			match+='2'
		else:
			match+='3'
	return match

def rem_bad_words(bl_list,wordlist):
	# Remove bad letter words from global wordlist
	nwordlist = []
	for word in wordlist:
		if not any(bltr in word for bltr in bl_list):
			nwordlist.append(word)

	return nwordlist

def corpos_match(corpos_dict, wordlist):
	# search wordlist for correct pos words and get the ones with maximum matches
	max_match = 0
	for wrd in wordlist:
		match = 0
		for cor_idx, cor_val in corpos_dict.items():
			if wrd[cor_idx] == cor_val:
				guess = wrd
				match+=1
		
		if match > max_match:
			max_match = match
			corpos_guess = guess
	
	return corpos_guess

def fn_Wordle_Player(intmatcher, wordlist, bl_list, corpos_dict):
	# Check for 
	# 1. correct pos - 1 , 
	# 2. good words - 2 , 
	# 3. bad words - 3 
	# and append into corresponding lists
	for ltr_idx, fdbk in enumerate(intMatcher):
		if fdbk=='1':
			corpos_dict[ltr_idx] = nextGuess[ltr_idx]
		elif fdbk=='2':
			gw_dict[ltr_idx] = nextGuess[ltr_idx]
		else:
			bl_list.append(nextGuess[ltr_idx])
	
	# Remove bad letter words from global wordlist
	#print("bl_list",bl_list)
	if bl_list:
		wordlist = rem_bad_words(bl_list,wordlist)

	#print("wordlist len",len(wordlist))

	# Guess first word from wordlist as next guess
	guess = wordlist[0]

	#print("Correct pos dict is",corpos_dict)

	# If any correct positions guessed previously
	if corpos_dict:
		guess = corpos_match(corpos_dict, wordlist)
	
	return guess, wordlist, bl_list, corpos_dict

def input_gen(wordlist):
	return random.choice(wordlist)

def stat(res):
	print("Output Stats",res)


if __name__ == '__main__':
	res = []

	# Read wordlist file and store in list
	with open('eng_five.txt','r') as fr:
		main_wordlist = list(map(str.upper,fr.read().splitlines()))

	for _ in range(40):

		# Good words dict
		gw_dict = {}
		# Bad letters list
		bl_list = []
		# Correct position dict
		corpos_dict = {}

		wordlist = main_wordlist.copy()
		#theWord=input('Enter word of the day: ').upper()
		theWord = input_gen(wordlist)
		print("Word of the Day", theWord)

		while(len(theWord)!=5 or (theWord not in wordlist)):
			theWord=(input('"Please input a valid 5 letter word: ')).upper()
		for i in range(6):
			if i==0:
				nextGuess='adieu'.upper()
			else:
				nextGuess, wordlist, bl_list, corpos_dict = fn_Wordle_Player(intMatcher, wordlist, bl_list, corpos_dict)
				nextGuess = nextGuess.upper()
			if nextGuess in wordlist and len(nextGuess)==5:  #wordlist defined by participant above
				if nextGuess == theWord:
					print(nextGuess)
					print("Word found on attempt ",i+1)
					res.append(i+1)
					break
				else:
					intMatcher = fn_Matcher(theWord, nextGuess)
					#print(nextGuess)
					#print("Word does not match, Feedback pattern returned :",intMatcher)

					# Remove previously guessed word from wordlist
					wordlist.remove(nextGuess)
			else:
				print(nextGuess, "Not a valid word")
				break
		else:
			#print("Word not found. Correct word is",theWord)
			print("Word not found")
			res.append("X")
	
	stat(res)
