def get_input():
    with open("9.txt", "r") as f:
        return f.read().split()


def calc_rect_area(one, two):
    x = max(one[0], two[0]) - min(one[0], two[0]) + 1
    y = max(one[1], two[1]) - min(one[1], two[1]) + 1
    return x * y

def part1():
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
    tiles = set()

    min_max = get_min_max(o, t)

    x_max, x_min = min_max[0]
    y_max, y_min = min_max[1]

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            tiles.update((x, y))

    return tiles

def get_legal_tiles(tiles):
    res = set(tiles)

    tmp = {}
    for i in range(len(tiles) - 1):
        tile = (one, two) = tiles[i], tiles[i + 1]
        tmp[tile] = filled_between(one, two)
    last_to_first = (tiles[-1], tiles[0])
    tmp[last_to_first] = filled_between(last_to_first[0], last_to_first[1])

    for (one, two), filled in tmp.items():
        res.update(filled)

    res.update(get_filled_shape(res, tiles))

    return res

def get_filled_shape(border_tiles, puzzle_tiles):
    bt_set = set(border_tiles)
    res = set(border_tiles)

    min_max_dic = {}
    for one in puzzle_tiles:
        for two in puzzle_tiles:
            min_max_dic[(one, two)] = get_min_max(one, two)

    def process_filling(o, t):
        xs, ys = min_max_dic[(o, t)]
        corners = set([(x, y) for x in xs for y in ys])
        if corners.issubset(bt_set):
            return filled_between(o, t)
        return []

    for i in range(0, len(puzzle_tiles) - 1):
        for j in range(i + 1, len(puzzle_tiles)):
            one, two = puzzle_tiles[i], puzzle_tiles[j]
            processed = process_filling(one, two)
            res.update(processed)
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

    candidates = set([(one, two) for one in tiles for two in tiles if one != two])

    print(f'made candidates: {len(candidates)}')

    candidate_tiles = {
        (one, two): filled_between(one, two) for one, two in candidates
    }

    print('made candidates tiles')

    for one in tiles:
        for two in tiles:
            if (one, two) not in candidate_tiles.keys():
                continue
            cts = candidate_tiles[(one, two)]
            if any(ct not in legal_tiles for ct in cts):
                ans = max(ans, calc_rect_area(one, two))

    print(f'Part2: {ans}')

part1()
part2()
