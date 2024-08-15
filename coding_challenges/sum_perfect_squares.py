def sum_of_squares(n):
    import math
    
    def is_square(n):
        sqrt_n = math.sqrt(n)
        return (sqrt_n - math.floor(sqrt_n)) == 0
        
    sqrt_n = int(math.sqrt(n))
    def two_square_check(n):
        for x in range(1,sqrt_n):
            if is_square(n - x*x):
                return True
        return False
        
    def three_square_check(n):
        x = n
        while not x & 3:
            x = x>>2
        return (x+1)%8 != 0
    
    if is_square(n):
        return 1
    if two_square_check(n):
        return 2
    if three_square_check(n):
        return 3
    else:
        return 4