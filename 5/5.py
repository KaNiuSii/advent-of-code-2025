from typing import List, Tuple


def get_input():
    with open("5.txt", "r") as f:
        return f.read().strip().split()


def get_range(range_str):
    params = range_str.split('-')
    return range(int(params[0]), int(params[1]) + 1)

def part1():
    ans = 0

    input_str = get_input()

    ranges_input, ids_input = [x for x in input_str if '-' in x], [x for x in input_str if '-' not in x]

    ranges, ids = [get_range(x) for x in ranges_input], [int(x) for x in ids_input]

    for r in ranges:
        fresh = [x for x in ids if x in r]
        ans += len(fresh)
        ids = [x for x in ids if x not in fresh]

    print(f'Part 1: {ans}')


def ranges_overlap(first, second):
    if len(second) == 0:
        return False
    return not (
            (second[0] <= second[1] < first[0] <= first[1])
                                or
            (first[0] <= first[1] < second[0] <= second[1])
    )

def merge_ranges(first, second):
    if len(second) == 0:
        return first

    merge = first + second
    bottom, top = min(merge), max(merge)
    return [bottom, top]

def part2():
    ans = 0

    input_str = get_input()

    ranges_input = [x for x in input_str if '-' in x]

    ranges_list = [
        [
            int(x.split('-')[0]),
            int(x.split('-')[1])
         ]
        for x in ranges_input
    ]
    ranges_merged: List[Tuple[List[int], List[int]]] = []

    def used():
        return [xx for x in ranges_merged for xx in x[0]]
    ranges_list = sorted(ranges_list)
    for i in range(len(ranges_list)):
        curr = ranges_list[i]
        entity: Tuple[List[int], List[int]] = ([i],[curr[0],curr[1]])
        if i in used():
            continue
        if i == len(ranges_list) - 1:
            ranges_merged.append(entity)
        for j in range(i + 1, len(ranges_list)):
            if j in used():
                continue
            next_range = ranges_list[j]
            if ranges_overlap(entity[1], next_range):
                entity = (entity[0] + [j],merge_ranges(entity[1], next_range))
        ranges_merged.append(entity)

    ans = sum([((merge[1][1] - merge[1][0]) + 1) for merge in ranges_merged])
    print(f'Part 2: {ans}')

part1()
part2()

