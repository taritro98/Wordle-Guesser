wordlist = ["rapid","apple","zzuzz","aaron","aback"]
nw = []

bl_list = ["e","u"]
gl_list = ["a","d","i"]


for word in wordlist:
    if not any(bltr in word for bltr in bl_list) and all(gltr in word for gltr in gl_list):
        nw.append(word)

print(nw)