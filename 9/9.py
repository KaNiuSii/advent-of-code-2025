def get_input():
    with open("9.txt", "r") as f:
        return f.read().split()


def calc_rect_area(one, two):
    x = max(one[0], two[0]) - min(one[0], two[0]) + 1
    y = max(one[1], two[1]) - min(one[1], two[1]) + 1
    return x * y

def part1():
    ans = 0

    puzzle = get_input()

    tiles = [list(map(int, tile.split(','))) for tile in puzzle]

    areas = [calc_rect_area(one, two) for one in tiles for two in tiles]

    ans = max(areas)

    print(f'Part1: {ans}')

def get_max_min(o, t):
    xs = max(o[0], t[0]), min(o[0], t[0])
    ys = max(o[1], t[1]), min(o[1], t[1])
    return xs, ys

def filled_between(o, t):
    max_min = get_max_min(o, t)

    x_max, x_min = max_min[0]
    y_max, y_min = max_min[1]

    return [(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1)]

def get_legal_tiles(tiles):
    res = tiles.copy()

    for i in range(len(tiles) - 1):
        one, two = tiles[i], tiles[i + 1]
        res += filled_between(one, two)
    res += filled_between(tiles[-1], tiles[0])

    res += get_filled_shape(res, tiles)

    return res

def get_filled_shape(border_tiles, puzzle_tiles):
    res = border_tiles.copy()

    def process_filling(o, t):
        xs, ys = get_max_min(o, t)
        corners = [(x, y) for x in xs for y in ys]
        if all(c in border_tiles for c in corners):
            return filled_between(o, t)
        return []

    for i in range(0, len(puzzle_tiles) - 1):
        for j in range(i + 1, len(puzzle_tiles)):
            one, two = puzzle_tiles[i], puzzle_tiles[j]
            res += process_filling(one, two)

    return res

def print_test(tiles):
    for x in range(10):
        for y in range(20):
            print('#' if (y,x) in tiles else '.', end='')
        print()

def part2():
    ans = 0

    puzzle = get_input()

    tiles = [tuple(map(int, tile.split(','))) for tile in puzzle]

    legal_tiles = get_legal_tiles(tiles)

    # print_test(legal_tiles)

    for one in tiles:
        for two in tiles:
            area = calc_rect_area(one, two)
            xs, ys = get_max_min(one, two)

            legal_in_bound = set([lt for lt in legal_tiles
                              if xs[0] >= lt[0] >= xs[1]
                              and ys[0] >= lt[1] >= ys[1]])
            # print(f'len lt: {len(legal_in_bound)} area: {area}, one: {one}, two: {two}, legals: {legal_in_bound}')
            if area <= len(legal_in_bound):
                ans = max(ans, area)

    print(f'Part2: {ans}')

part1()
part2()
