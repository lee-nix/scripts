def next_bigger(n):
    from collections import Counter
    if n <= 11:
        return -1
    string_n = str(n)
    if len(set(string_n)) == 1:
        return -1
    max_val = int(''.join(sorted(string_n, reverse=True)))
    if n == max_val:
        return -1
    for x in range(n+1, max_val+1):
        if Counter(string_n) == Counter(str(x)):
            return x
    

n = [1,9,11,111,222,2017, 12, 513, 2017, 414, 144]
for x in n:
    print(next_bigger(x))