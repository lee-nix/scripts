#https://www.codewars.com/kata/vowel-recognition/train/python
s = 'baceb oijheofijw ;ailj;awilgj ewifgjwoiefjoiwj OIJO IJO:IFJW OFIJWOIEFJ OEIFJ IJF EOW;IJF OWIJEF W'
def f(s):
    substrings = []
    vowel_count = 0
    for start, _ in enumerate(s):
        stop = start + 1
    while stop <= len(s):
        substrings.append(map(s[start:stop].lower().count, 'aeiou'))
        stop += 1
    for sub in substrings:
        vowel_count += sum([vowels for vowels in sub])
    return vowel_count

from timeit import timeit
timeit(print(f(s)), setup='s = "baceb oijheofijw ;ailj;awilgj ewifgjwoiefjoiwj OIJO IJO:IFJW OFIJWOIEFJ OEIFJ IJF EOW;IJF OWIJEF W"')
vc = f(s)
print(vc)
