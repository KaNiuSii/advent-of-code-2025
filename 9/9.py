from tqdm import trange
from dataclasses import dataclass
from typing import List, Tuple, Dict


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


Point = Tuple[int, int]

@dataclass
class Edge:
    one: Point
    two: Point
    tiles: List[Point]

    def __str__(self) -> str:
        return f'\nOne: {self.one}\nTwo: {self.two}\nTiles: {self.tiles}\n'

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


def is_point_inside_polygon(point: Point, edges: List[Edge]) -> bool:
    x, y = point
    intersections = 0

    for edge in edges:
        x1, y1 = edge.one
        x2, y2 = edge.two

        if y1 != y2:  # Vertical
            if min(y1, y2) < y <= max(y1, y2):
                intersect_x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)

                if intersect_x > x:
                    intersections += 1
        else:  # Horizontal edge
            if y == y1:
                if min(x1, x2) < x <= max(x1, x2):
                    return True

    return intersections % 2 == 1

def get_edge(o: Point, t: Point) -> Edge:
    return Edge(one=o, two=t, tiles=filled_between(o, t))

def get_edges(tiles: List[Point]) -> List[Edge]:
    edges: List[Edge] = []

    for i in range(len(tiles) - 1):
        one, two = tiles[i], tiles[i + 1]
        edges.append(get_edge(one, two))
    edges.append(get_edge(tiles[-1], tiles[0]))

    return edges

def get_corners(o, t):
    xs, ys = get_min_max(o, t)
    return [(x, y) for x in xs for y in ys]

def print_test(edges: List[Edge]) -> None:
    tiles = [t for e in edges for t in e.tiles]

    for x in range(10):
        for y in range(20):
            symbol = '#' if (y, x) in tiles else '.'
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

    pairs = sorted(pairs, key=lambda pair: calc_rect_area(pair[0], pair[1]), reverse=True)
    for i in trange(len(pairs)):
        one, two = pairs[i]
        area = calc_rect_area(one, two)

        corners = sorted(get_corners(one, two))
        corners = corners[:2] + corners[-2:][::-1]

        inside = True
        for c in corners:
            if not is_point_inside_polygon(c, edges):
                inside = False
                break
        if not inside:
            continue

        rect_tiles = set()
        for j in range(len(corners)):
            rect_tiles.update(filled_between(corners[j], corners[(j + 1) % len(corners)]))

        inside = True
        for rt in rect_tiles:
            if not is_point_inside_polygon(rt, edges):
                inside = False
                break

        if inside:
            ans = area
            break


    print(f'Part2: {ans}')

part1()
part2()


