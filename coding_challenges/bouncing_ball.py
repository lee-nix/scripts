'''
Bouncing Balls
https://www.codewars.com/kata/5544c7a5cb454edb3c000047/train/python
Author: Lee Nix
Version: 0.1

Conditions:
Float parameter "h" in meters must be greater than 0
Float parameter "bounce" must be greater than 0 and less than 1
Float parameter "window" must be less than h
If all three conditions above are fulfilled, return a positive integer, otherwise return -1

Testing:
from bouncing_ball import bouncingBall
bouncingBall(5, 0.99, 1)
bouncingBall(3, 0.66, 1.5) == 3
bouncingBall(30, 0.66, 1.5) == 15
'''

def bouncingBall(h, bounce, window):
    if h <= 0 or not 0 < bounce < 1 or not 0 < window < h:
        return -1
    else:
        bounce_count = 0
        while h > window:
            h = h * bounce
            bounce_count = bounce_count + 2 if h > window else bounce_count + 1
        return bounce_count