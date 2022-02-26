def vowel_count(str):
    count = 0
    vowel = set("aeiouAEIOU")
    for alphabet in str:
        if alphabet in vowel:
            count = count + 1
    return count

if __name__=='__main__':
    with open('eng_five.txt','r') as fr:
        wordlist = list(map(str.upper,fr.read().splitlines()))
    
    max_vowels = 0
    for word in wordlist:
        vow_count = vowel_count(word)
        if vow_count > max_vowels:
            max_vowels = vow_count
            print("word",word)
    
