from audioop import reverse
from collections import Counter, OrderedDict
from itertools import combinations

def weight_sum_dict(lst,wt_dict):
    '''
    Sorts dict by weighted sum desc order
    TODO: Check whether return in sorted descending order
    Returns list of lists of desc order sorted dict [[],[]]
    '''
    wtsum_dict = {}
    for comb in lst:
        wtsum_dict[comb] = sum(wt_dict[elem] for elem in comb)
    wtsum_dict_sorted = dict(sorted(wtsum_dict.items(), key=lambda item: item[1], reverse=True))
    wtsumlst = [list(wtsum_dict_sorted_tuple) for wtsum_dict_sorted_tuple in wtsum_dict_sorted]
    #print(list(wtsum_dict_sorted.keys()))
    return wtsumlst

def gen_comb(ltr_count_list):
    '''
    Input : [(key,val)]
    Generate weighted combinations
    '''
    max_len=5
    comb_lst=[]

    # Weight dictionary
    wt_dict = {k:v for k,v in ltr_count_list}
    
    # Run loop in desc order to gen combinations from maxlen to 1
    while(max_len>0):
        if max_len==5:
            comb = [lset[0] for idx, lset in enumerate(ltr_count_list)]
            comb = ["".join(comb)]
        else:
            comb = [lset[0] for idx, lset in enumerate(ltr_count_list)]
            # Generate x length combinations and desc sort by weight
            wtsum_lst = weight_sum_dict(list(combinations(comb,max_len)),wt_dict)
            comb = list(map(lambda x: "".join(x),wtsum_lst))
            
        comb_lst.extend(comb)

        print(comb_lst)
        max_len-=1
    
    return comb_lst

def entropy_calc(wordlist):
    '''
    Input wordlist : list
    Returns highest to lowest word freq combinations : list of lists
    '''
    rem_dup = list(map(lambda x:"".join(set(x)),wordlist))
    ltr_count_list = Counter("".join(rem_dup)).most_common(5)
    most_com_ltrcombs = gen_comb(ltr_count_list)
    return most_com_ltrcombs

if __name__=='__main__':
    wordlist = ['BLABY', 'BYLAW', 'BYWAY', 'DHABI', 'FLAIL', 'FLAKY', 'FUGAL', 'GUAVA', 'HILDA', 'ILIAD', 'JULIA', 'KHAKI', 'LIBYA', 'LLAMA', 'LYDIA', 'MIAMI', 'MUZAK', 'PHIAL', 'PIZZA', 'PLAID', 'PLAZA', 'PUKKA', 'PULAU', 'PUPAL', 'QUAFF', 'QUAIL', 'QUALM', 'UVULA', 'VILLA', 'VULVA', 'WILMA']

    res = entropy_calc(wordlist)
    print(res)