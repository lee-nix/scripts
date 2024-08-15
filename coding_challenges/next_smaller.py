# https://www.codewars.com/kata/next-smaller-number-with-the-same-digits/train/python

def next_smaller(n):
    string_n = str(n)
    list_n = list(string_n)
    # catch the cases of single digit, all same digits, and already lowest value of digits without iteration
    if (n <= 10) or (len(set(string_n)) == 1) or (n == int(''.join(sorted(string_n)))):
        return -1
    else:
        # starting with the last digit, inspect from right to left, if current digit < inspected digit, move current to left of inspected and return
        for swap_from in range(len(list_n), 0, -1):
            for swap_to in range(len(list_n) - 1, 0, -1):
                swap_from_idx, swap_to_idx = swap_from - 1, swap_to - 1
                if int(list_n[swap_from_idx]) < int(list_n[swap_to_idx]):
                    # move element to left of first detected lower digit
                    list_n.insert(swap_to_idx, list_n.pop(swap_from_idx))
                    return int(''.join(list_n))

next_smaller(907) # 790

next_smaller(531) # 513

next_smaller(135) # -1

next_smaller(2071) # 2017

next_smaller(414) # 144

next_smaller(123456798) # 123456789

next_smaller(123456789) # -1

next_smaller(1234567908) # 1234567890

'''

The solution to a good algorithm is a clear logic. Your code uses the "hammers" that are present, spring to mind, and do a tiny bit more than needed. So start to find a logic first.

To get the next smaller number the most strict algorithm would be:

Example: 1253479

Start from the last digit to the first as long as the digits are decreasing or equal. 12[5]+increasing 3479, 5 > 3.
From the increasing tail pick the element just smaller (4), and reverse the tail. 12(4)+decreasing 97[5]3.
Result: 1249753

The math is relatively simple, and the algorithm linear to the length.

Test Passed
Test Passed
Test Passed
1207 should equal -1
Test Passed
Test Passed
Completed in 0.11ms
 Extended tests
 Short ones
Test Passed
Test Passed
135 should equal 153
Test Passed
Test Passed
10 should equal -1
Test Passed
1027 should equal 1072
Test Passed
Completed in 0.09ms
 Longer ones
Test Passed
20909 should equal 20990
Test Passed
Test Passed
59884848458359 should equal 59884848459853
1023456879 should equal -1
51226262565127 should equal 51226262627551
202233445656 should equal -1
506879 should equal -1
'''
