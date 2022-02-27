wordlist = ['BLABY', 'BYLAW','BYWAY', 'DHABI', 'FLAIL', 'FLAKY', 'FUGAL', 'GUAVA', 'HILDA', 'ILIAD', 'JULIA', 'KHAKI', 'LIBYA', 'LLAMA', 'LYDIA', 'MIAMI', 'MUZAK', 'PHIAL', 'PIZZA', 'PLAID', 'PLAZA', 'PUKKA', 'PULAU', 'PUPAL', 'QUAFF', 'QUAIL', 'QUALM', 'UVULA', 'VILLA', 'VULVA', 'WILMA']

combs = ['ALIUP', 'ALIU', 'ALIP', 'ALUP', 'AIUP', 'LIUP', 'ALI', 'ALU', 'ALP', 'AIU', 'AIP', 'AUP', 'LIU', 'LIP', 'LUP', 'IUP', 'AL', 'AI', 'AU', 'AP', 'LI', 'LU', 'LP', 'IU', 'IP', 'UP', 'A', 'L', 'I', 'U', 'P']

for comb in combs:
    for word in wordlist:
        print("comb",comb)
        print("word",word)
        if all([combl in word for combl in list(comb)]):
            print("Out",word)
            exit()
