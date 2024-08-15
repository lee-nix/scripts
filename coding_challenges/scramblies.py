# https://www.codewars.com/kata/scramblies/train/python

def scramble(s1, s2):
    import re
    from collections import Counter
    s2_counter = Counter(s2) # reduce iterations if s2 contains duplicates and give us char counts
    for key in s2_counter:
        if len(re.findall(f'{key}', s1)) < s2_counter[key]: # compare char counts
            return False # fail fast
    return True