from tqdm import trange
from dataclasses import dataclass
from typing import List, Tuple, Dict


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


Point = Tuple[int, int]

UNSOLVED = 0

EdgeVariant = int

HORIZONTAL = -1
VERTICAL = 1

EdgeDirection = int

UP = 1
DOWN = -1
LEFT = -1
RIGHT = 1

@dataclass
class Edge:
    order: int
    one: Point
    two: Point
    tiles: List[Point]
    variant: EdgeVariant
    direction: EdgeDirection

    def __str__(self) -> str:
        return f'\nOne: {self.one}\nTwo: {self.two}\nTiles: {self.tiles}\nVariant: {self.variant}\nDirection: {self.direction}\n'

def get_min_max(o: Point, t: Point) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    xs = min(o[0], t[0]), max(o[0], t[0])
    ys = min(o[1], t[1]), max(o[1], t[1])
    return xs, ys

def filled_between(o: Point, t: Point) -> List[Point]:
    max_min = get_min_max(o, t)
    x_min, x_max = max_min[0]
    y_min, y_max = max_min[1]
    return [(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1)]

def get_mid_point(edge: Edge) -> Point:
    return (edge.one[0] + edge.two[0]) // 2, (edge.one[1] + edge.two[1]) // 2

def are_edges_legal(possible: Edge, compared_to: Edge) -> bool:
    p_mp = get_mid_point(possible)
    c_mp = get_mid_point(compared_to)
    x_diff, y_diff = c_mp[0] - p_mp[0], c_mp[1] - p_mp[1]
    x_diff, y_diff = (x_diff // abs(x_diff)) if x_diff != 0 else 1, (y_diff // abs(y_diff)) if y_diff != 0 else 1
    direction = possible.direction
    if_value = y_diff if possible.variant == HORIZONTAL else x_diff
    return if_value == direction

def get_direction_for_edges(known: Edge, seeking: Edge) -> EdgeDirection:
    k_mp, s_mp = get_mid_point(known), get_mid_point(seeking)
    x = 0 if k_mp[0] > s_mp[0] else 1
    y = 0 if k_mp[1] > s_mp[1] else 1
    direction = known.direction
    if direction < 0:
        direction = 0
    k_values_grid = [[[-1, 1], [1, -1]],
                       [[1, -1], [-1, 1]], ]

    grid = k_values_grid[x][y]
    return grid[direction]

def get_edge(o: Point, t: Point) -> Edge:
    variant = UNSOLVED
    direction = UNSOLVED
    xs, ys = get_min_max(o, t)
    if xs[0] == xs[1]:
        variant = VERTICAL
    else:
        variant = HORIZONTAL
    return Edge(one=o, two=t, tiles=filled_between(o, t), variant=variant, direction=direction, order = -1)

def get_edges(tiles: List[Point]) -> List[Edge]:
    edges: List[Edge] = []

    for i in range(len(tiles) - 1):
        one, two = tiles[i], tiles[i + 1]
        edges.append(get_edge(one, two))
        edges[-1].order = i
    edges.append(get_edge(tiles[-1], tiles[0]))
    edges[-1].order = len(tiles) - 1

    vertical_edges = sorted([e for e in edges if e.variant == VERTICAL], key=lambda e: e.one[0])
    horizontal_edges = sorted([e for e in edges if e.variant == HORIZONTAL], key=lambda e: e.one[1])

    far_left, far_right = vertical_edges[0].one[0], vertical_edges[-1].one[0]
    far_top, far_bottom = horizontal_edges[0].one[1], horizontal_edges[-1].one[1]

    for i in range(len(edges)):
        edge = edges[i]
        if edge.variant == VERTICAL:
            if edge.one[0] == far_left:
                edges[i].direction = RIGHT
            elif edge.one[0] == far_right:
                edges[i].direction = LEFT
        elif edge.variant == HORIZONTAL:
            if edge.one[1] == far_top:
                edges[i].direction = DOWN
            elif edge.one[1] == far_bottom:
                edges[i].direction = UP

    while any(e.direction == UNSOLVED for e in edges):
        for i in range(len(edges)):
            edge = edges[i]

            direction = edge.direction

            if direction == UNSOLVED:
                continue

            variant = edge.variant

            indexes = [(i+1) % len(edges)]
            for index in indexes:
                e = edges[index]

                if e.direction != UNSOLVED:
                    continue

                if e.variant == variant:
                    edges[index].direction = direction
                else:
                    edges[index].direction = get_direction_for_edges(edge, e)

    return edges

def get_corners(o, t):
    xs, ys = get_min_max(o, t)
    return [(x, y) for x in xs for y in ys]

def print_test(edges: List[Edge]) -> None:
    tiles = [t for e in edges for t in e.tiles]
    mp_dir = [(get_mid_point(e), e.direction, e.variant) for e in edges]

    for x in range(10):
        for y in range(20):
            symbol = '#' if (y, x) in tiles else '.'
            matching_mp = [mpd for mpd in mp_dir if mpd[0] == (y, x)]
            if len(matching_mp) != 0:
                direction = matching_mp[0][1]
                variant = matching_mp[0][2]
                if variant == HORIZONTAL:
                    symbol = '^' if direction == UP else 'v' if direction == DOWN else 'X'
                else:
                    symbol = '<' if direction == LEFT else '>' if direction == RIGHT else 'X'


            print(symbol, end='')
        print()

def part2() -> None:
    ans = 0
    puzzle = get_input()

    tiles: List[Point] = [tuple(map(int, tile.split(','))) for tile in puzzle]

    edges = get_edges(tiles)

    print_test(edges)

    pairs: List[Tuple[Point, Point]] = list(
        set([(min(o, t), max(o, t)) for o in tiles for t in tiles if o != t and o[0] - t[0] != 0 and o[1] - t[1] != 0]))

    corner_to_edges: Dict[Point, List[Edge]] = {}
    for i in range(len(tiles)):
        tile = tiles[i]
        corner_to_edges[tile] = [edges[i - 1],edges[i]]
    for e in edges:
        for t in e.tiles:
            if t == e.one or t == e.two:
                continue
            corner_to_edges[t] = [e]

    for i in trange(len(pairs)):
        one, two = pairs[i]
        area = calc_rect_area(one, two)

        corners = sorted(get_corners(one, two))
        corners = corners[:2] + corners[-2:][::-1]

        pair_edges = get_edges(corners)

        is_ok = False

        for pair_edge in pair_edges:
            crossed_edges = [e for t in pair_edge.tiles if t in corner_to_edges for e in corner_to_edges[t]]
            same_variant = [e for e in crossed_edges if e.variant == pair_edge.variant]
            is_ok = all([e.direction == pair_edge.direction for e in same_variant if len(set(e.tiles) & set(pair_edge.tiles)) > 1])
            if not is_ok:
                break
            other_variant = [e for e in crossed_edges if e.variant != pair_edge.variant]
            is_ok = all([are_edges_legal(pair_edge, o) for o in other_variant])

        if is_ok:
            print(one, two, area)
            ans = max(ans, area)



    print(f'Part2: {ans}')

part1()
part2()


