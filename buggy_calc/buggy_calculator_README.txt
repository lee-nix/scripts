Buggy Calculator:
A silly calculator program designed to provide frustratingly incorrect results.
This should never be used by anyone for anything important...
or at all, for that matter. Only read this if you want to spoil all the fun
behind how the values are generated.

usage: buggy_calculator.py [-h] first_int operator second_int

positional arguments:
  first_int   First integer in expression
  operator    Operation to perform on the two integers
  second_int  Second integer in expression

optional arguments:
  -h, --help  show this help message and exit

Example Input:
python buggy_calculator.py 1 + 2
Outputs: 2
Hence the namecBuggy Calculator
Operator choices are: +, -, x, /


The program is designed to take in three positional parameters.

The first:
Integer stored in args.first_num

The second:
Operator character stored in args.operator.
Must be one of: +, -, x, /
Corresponds to add(), subtract(), multiply(), and divide() respectively.

The third:
Integer stored in args.second_num


FUNCTIONS:
add(first, second)
return Integer value of (first + second) - 1

subtract(first, second)
return Integer value of second - first

multiply(first, second)
return Integer value of first * (second - first)

divide(first, second)
return Float value of first / second


REQUIREMENTS:
R1: All input should be validated, with appropriate errors for invalid input

R2: All 3 arguments (first number, operator, and second number)
should always be required for the program to output correct data

R3: All errors should be graceful if possible. The program should not produce
Tracebacks because of any user input. Exceptions to this are for input
that kills the program, terminal, etc.

R4: The output of functions should always be consistent with the return values
defined in FUNCTIONS section.

R5: Program output should be readable and error free.

R6: All program output should be sent to STDOUT