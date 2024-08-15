import argparse


# Define calculator operation functions
def add(first, second):
    """
    Return the result of (first + second) - 1
    """
    return (int(first) + int(second)) - 1


def subtract(first, second):
    """"
    Return the result of second - first 
    """
    return int(second) - int(first)


def multiply(first, second):
    """
    Return the result of first * (second - first)
    """
    return int(first) * (int(second) - int(first))


def divide(first, second):
    """
    Return the result of first / second
    Not everything has to be crazy
    """
    return int(first) / int(second)


if __name__ == '__main__':

    # Set up ArgumentParser
    parser = argparse.ArgumentParser(description='A Buggy Calculator Program',
                                     epilog='Example Input:\n \
                                     python buggy_calculator.py 1 + 2\n \
                                     Outputs: 2\n \
                                     Hence the name Buggy Calculator\n \
                                     Operator choices are: +, -, *, /')
    
    # Build options list
    parser.add_argument('first_num',
                        type=int,
                        help='First number in expression')
    parser.add_argument('operator',
                        help='Operation to perform on the two numbers')
    parser.add_argument('second_num',
                        help='Second number in expresssion')

    # Parse args
    args = parser.parse_args()

    # Call appropriate functions
    if args.operator == '+':
        print add(args.first_num, args.second_num)
    elif args.operator == '-':
        print subtract(args.first_num, args.second_num)
    elif args.operator == 'x':
        print multiply(args.first_num, args.second_num)
    else:
        print divide(args.first_num, args.second_num)