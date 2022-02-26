from itertools import chain, combinations
weights = {'A':2, 'B':1, 'C':3, 'D':2, 'E':1}

def weight(A):
    return sum(weights[x] for x in A)

# def powerset(iterable):
#     "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
#     s = list(iterable)
#     return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def powerset(iterable):
    s = list(iterable)
    return combinations(iterable,4)

print(list(combinations(['a','b','c','d'],3)))
# for x in powerset({'A', 'B', 'C', 'D', 'E'}):
#     print(x)
# print(powerset({'A', 'B', 'C', 'D', 'E'}))
#print([x for x in powerset({'A', 'B', 'C', 'D', 'E'}) if weight(x) == 4])