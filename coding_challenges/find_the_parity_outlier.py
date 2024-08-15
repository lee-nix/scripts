# https://www.codewars.com/kata/find-the-parity-outlier/train/python

def find_outlier(integers):
    import re
    return min( ([ i for i in integers if re.compile(r'^-?\d*[13579]$').match(str(i)) ],  # match odds
                 [ i for i in integers if re.compile(r'^-?\d*[02468]$').match(str(i)) ]), # match evens
              key=lambda x: len(x))[0] # return the first element in the shorter of the two lists
test = [2, 4, 6, 8, 10, -3]
test2 = [-21, 3, 11, 2, 7, 13]
find_outlier(test)
find_outlier(test2)
