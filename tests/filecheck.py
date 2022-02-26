with open('English.txt') as fr:
    wordlist = fr.read().splitlines()

print(len(wordlist))

five_letter_wordlist = [wrd for wrd in wordlist if len(wrd)==5 and '\'' not in wrd]
print(five_letter_wordlist)

with open('eng_five.txt','w') as fw:
    for word in five_letter_wordlist:
        fw.write("{}\n".format(word))