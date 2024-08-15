""" def balanced_parens(n):
    def generate_permutations(paren_open, paren_close=None):
        if paren_close is None:
            paren_close = paren_open
        if paren_open == paren_close == 0:
            yield ''
        else:
            if paren_open > 0:
                for p in generate_permutations(paren_open - 1, paren_close):
                    yield '(' + p
            if paren_close > paren_open:
                for p in generate_permutations(paren_open, paren_close - 1):
                    yield ')' + p

    return [x for x in generate_permutations(n)]



print(timeit('balanced_parens(15)', setup='from __main__ import balanced_parens', number=1))
print(balanced_parens(3))
 """
from timeit import timeit
from functools import reduce
lst = [499942, 898102, 846073]
print(pow(lst[0]%10,reduce(lambda b,a:a**b,lst[:0:-1]) % 4,10))
#
#print(timeit('lambda N:eval("**".join(lst))%10', number=1, setup='from functools import reduce', globals=globals()))
#print(timeit('reduce(lambda x,y:y**x, lst[::-1]) % 10', number=1, setup='from functools import reduce', globals=globals()))
#print(reduce(lambda x,y:y**x, lst[::-1], 1) % 10)