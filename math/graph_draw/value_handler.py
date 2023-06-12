# p: point  : 'p', A, x, y      -> A = (x, y)
# a: angle  : 'a', ABC, a       -> <ABC = a degree
# l: line   : 'l', lAB, a, b    -> y = a * x + b
# d: dir    : 'd', AB, a        -> <BAx = a degree
# m: length : 'm', mAB, a       -> distance AB is a

def handle_value(items):
    if items[1] == 'p':
        return ('p', items[2], int(items[3]), int(items[4]))
    elif items[1] == 'a':
        return ('a', items[2], int(items[3]))


