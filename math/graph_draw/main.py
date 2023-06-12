import math
import argparse
import re
import induction_handler
import value_handler

letters = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
    'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K':10, 'L':11,
    'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, 'R':17,
    'S':18, 'T':19, 'U':20, 'V':21, 'W':22, 'X':23,
    'Y':24, 'Z':25,
}


# type pp2d: get line direction by two points
# type d2d:  direction to direction by angle
# type pd2l: get line expression by point and direction
# type ll2p: get intersection point of two lines

def parse_args():
    parser = argparse.ArgumentParser(description='Math Arguments: ')
    parser.add_argument('--inductions', type=str)
    parser.add_argument('--values', type=str)
    parser.add_argument('--lines', type=str)
    parser.add_argument('--dot_lines', type=str)
    parser.add_argument('--margin', type=int)
    args, unknown = parser.parse_known_args()
    return args


def handle_max(values, inductions, dm):
    maxX = 0
    maxY = 0
    for value in values:
        if value[0] == 'p':
            maxX = max(maxX, value[2] + dm)
            maxY = max(maxY, value[3] + dm)
    for induction in inductions:
        if induction[0] == 'p':
            maxX = max(maxX, induction[2] + dm)
            maxY = max(maxY, induction[3] + dm)

    return (maxX, maxY)


def handle_induction(items, values, inductions):
    if items[1] == 'pp2d':
        return induction_handler.handle_pp2d(items, values, inductions)
    elif items[1] == 'd2d':
        return induction_handler.handle_d2d(items, values, inductions)
    elif items[1] == 'pd2l':
        return induction_handler.handle_pd2l(items, values, inductions)
    elif items[1] == 'll2p':
        return induction_handler.handle_ll2p(items, values, inductions)
    elif items[1] == 'pp2m':
        return induction_handler.handle_pp2m(items, values, inductions)
    elif items[1] == 'lm2p':
        return induction_handler.handle_lm2p(items, values, inductions)


def handle_graph(lines, dot_lines, values, inductions, maxX, maxY, margin):
    print(f'<svg height="{maxY}" width="{maxX}">')
    points = dict()
    for value in values:
        if value[0] == 'p':
            points[value[1]] = value
    for induction in inductions:
        if induction[0] == 'p':
            points[induction[1]] = induction

    for (p, point) in points.items():
        x = point[2] + margin
        y = point[3]
        if y >= maxY / 2 + margin:
            y += margin + 5
        print(f'  <text x="{x}" y="{maxY-y}" fill="red">{point[1]}</text>')
        
    for line in lines:
        (x1, y1) = (points[line[0]][2] + margin, maxY - points[line[0]][3] - margin)
        (x2, y2) = (points[line[1]][2] + margin, maxY - points[line[1]][3] - margin)
        print(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:rgb(0,0,0);stroke-width:1" />')

    for line in dot_lines:
        (x1, y1) = (points[line[0]][2] + margin, maxY - points[line[0]][3] - margin)
        (x2, y2) = (points[line[1]][2] + margin, maxY - points[line[1]][3] - margin)
        print(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:rgb(0,0,0);stroke-width:1;stroke-dasharray:4" />')

    print('</svg>')


if __name__ == '__main__':
    args = parse_args()

    values = list()
    for value in args.values.split(','):
        items = re.split(' |\.', value)
        values.append(value_handler.handle_value(items))

    inductions = list()
    for induction in args.inductions.split(','):
        items = re.split(' |\.', induction)
        inductions.append(handle_induction(items, values, inductions))

    (maxX, maxY) = handle_max(values, inductions, args.margin * 2)

    handle_graph(args.lines.split(' '),
                 args.dot_lines.split(' '),
                 values,
                 inductions,
                 maxX,
                 maxY,
                 args.margin)

