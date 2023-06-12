import math

def handle_pp2d(items, values, inductions):
    i = int(items[3][1:])
    p1 = values[i] if items[3][0] == 'v' else inductions[i]
    i = int(items[4][1:])
    p2 = values[i] if items[4][0] == 'v' else inductions[i]

    assert p1[0] == 'p'
    assert p2[0] == 'p'
    assert p1[1] == items[2][0]
    assert p2[1] == items[2][1]

    d = 0
    if p2[3] == p1[3]:
        d = 0 if p2[2] > p1[2] else 180
    else:
        tanValue = float(p2[3] - p1[3]) / (p2[2] - p1[2])
        d = math.atan(tanValue) * 180 / math.pi
    return ('d', items[2], d)


def handle_d2d(items, values, inductions):
    i = int(items[3][1:])
    d1 = values[i] if items[3][0] == 'v' else inductions[i]
    i = int(items[4][1:])
    a2 = values[i] if items[4][0] == 'v' else inductions[i]

    assert d1[0] == 'd'
    assert a2[0] == 'a'
    assert d1[1][0] == a2[1][1]
    assert d1[1][0] == items[2][0]
    assert ((d1[1][1] == a2[1][0]) or (d1[1][1] == a2[1][2]))
    if d1[1][1] == a2[1][0]:
        assert a2[1][2] == items[2][1]
        return ('d', items[2], (360 + d1[2] - a2[2]) % 360)
    else: # d1[1][1] == a2[2][2]
        assert a2[1][0] == items[2][1]
        return ('d', items[2], (d1[2] + a2[2]) % 360)


def handle_pd2l(items, values, inductions):
    i = int(items[3][1:])
    p1 = values[i] if items[3][0] == 'v' else inductions[i]
    i = int(items[4][1:])
    d2 = values[i] if items[4][0] == 'v' else inductions[i]

    assert p1[0] == 'p'
    assert d2[0] == 'd'
    assert p1[1] == d2[1][0]
    assert items[2][0] == 'l'
    assert items[2][1:] == d2[1]

    a = math.tan(d2[2]*math.pi/180)
    b = p1[3] - a * p1[2]
    return ('l', items[2], a, b)


def handle_ll2p(items, values, inductions):
    i = int(items[3][1:])
    l1 = values[i] if items[3][0] == 'v' else inductions[i]
    i = int(items[4][1:])
    l2 = values[i] if items[4][0] == 'v' else inductions[i]

    assert l1[0] == 'l'
    assert l2[0] == 'l'
    assert l1[1][2] == l2[1][2]

    x = (l2[3] - l1[3]) / (l1[2] - l2[2])
    y = l1[2] * x + l1[3]

    return ('p', items[2], int(x), int(y))

def handle_pp2m(items, values, inductions):
    i = int(items[3][1:])
    p1 = values[i] if items[3][0] == 'v' else inductions[i]
    i = int(items[4][1:])
    p2 = values[i] if items[4][0] == 'v' else inductions[i]

    return ('m', items[2], math.sqrt((p1[2] - p2[2])**2 + (p1[3] - p2[3])**2))

def handle_lm2p(items, values, inductions):
    i = int(items[3][1:])
    d1 = values[i] if items[3][0] == 'v' else inductions[i]
    i = int(items[4][1:])
    p2 = values[i] if items[4][0] == 'v' else inductions[i]
    i = int(items[5][1:])
    m3 = values[i] if items[5][0] == 'v' else inductions[i]
    
    assert d1[0] == 'd'
    assert p2[0] == 'p'
    assert m3[0] == 'm'

    x = p2[2] + m3[2] * math.cos(math.pi * d1[2] / 180)
    y = p2[3] + m3[2] * math.sin(math.pi * d1[2] / 180)

    return ('p', items[2], int(x), int(y))

