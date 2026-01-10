from tqdm import trange


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

def get_corners(o, t):
    xs, ys = get_max_min(o, t)
    return [(x, y) for x in xs for y in ys]

def get_legal_corners(tiles):
    border_tiles = set()

    for i in range(len(tiles) - 1):
        one, two = tiles[i], tiles[i + 1]
        border_tiles.update(filled_between(one, two))
    border_tiles.update(filled_between(tiles[-1], tiles[0]))  # Zamknięcie pętli

    all_corners = set()

    for one in tiles:
        for two in tiles:
            if one != two:
                all_corners.update(get_corners(one, two))

    return get_corners_from_border(border_tiles, tiles, all_corners)

def get_corners_from_border(border_tiles, puzzle_tiles, all_corners):
    res = set()

    def process_filling(o, t):
        corners = get_corners(o, t)
        if all(c in border_tiles for c in corners):
            return filled_between(o, t)
        return []

    pairs = list(set((min(puzzle_tiles[i], puzzle_tiles[j]), max(puzzle_tiles[i], puzzle_tiles[j]))
                for i in range(len(puzzle_tiles) - 1)
                for j in range(i + 1, len(puzzle_tiles))
                if puzzle_tiles[i] != puzzle_tiles[j]))

    for i in trange(len(pairs), desc='Corners'):
        one, two = pairs[i]
        filled = process_filling(one, two)
        matching = all_corners.intersection(filled)
        res.update(matching)

    return res

def print_test(tiles):
    for x in range(10):
        for y in range(20):
            print('#' if (y, x) in tiles else '.', end='')
        print()

def part2():
    ans = 0
    puzzle = get_input()

    tiles = [tuple(map(int, tile.split(','))) for tile in puzzle]

    legal_tiles = get_legal_corners(tiles)

    pairs = list(set((min(one, two), max(one, two)) for one in tiles for two in tiles if one != two))

    for i in trange(len(pairs)):
        one, two = pairs[i]
        area = calc_rect_area(one, two)
        corners = set(get_corners(one, two))

        if corners.issubset(legal_tiles):
            ans = max(ans, area)

    print(f'Part2: {ans}')

part1()
part2()
