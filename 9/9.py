def get_input():
    with open("9test.txt", "r") as f:
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

def get_min_max(o, t):
    xs = max(o[0], t[0]), min(o[0], t[0])
    ys = max(o[1], t[1]), min(o[1], t[1])
    return xs, ys

def filled_between(o, t):
    tiles = []

    min_max = get_min_max(o, t)

    x_max, x_min = min_max[0]
    y_max, y_min = min_max[1]

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            tiles.append((x, y))

    return tiles

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
        xs, ys = get_min_max(o, t)
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

    print_test(legal_tiles)

    for one in tiles:
        for two in tiles:
            candidate_tiles = filled_between(one, two)
            if all(ct in legal_tiles for ct in candidate_tiles):
                ans = max(ans, calc_rect_area(one, two))

    print(f'Part2: {ans}')

part1()
part2()
