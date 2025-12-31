from idlelib.tree import TreeNode
from tree import SigmaTree, TreeNode

def get_input():
    with open("7test.txt", "r") as f:
        return f.read().split()


def part1():
    ans = 0

    puzzle = get_input()
    puzzle_without_empty = [puzzle[i] for i in range(len(puzzle)) if i % 2 == 0]

    objects_idx = [puzzle_without_empty[0].index('S')]

    for splitter_line in puzzle_without_empty[1:]:
        splitters_idx = [i for i in range(len(splitter_line)) if splitter_line[i] == '^']
        duplicates = set(objects_idx) & set(splitters_idx)
        for duplicate in duplicates:
            left, right = duplicate - 1, duplicate + 1
            objects_idx.remove(duplicate)
            if left not in objects_idx:
                objects_idx.append(left)
            if right not in objects_idx:
                objects_idx.append(right)
            ans += 1

    print(f'Part1: {ans}')

def part2():
    ans = 1

    puzzle = get_input()
    puzzle_without_empty = [puzzle[i] for i in range(len(puzzle)) if i % 2 == 0]
    puzzle_without_first = puzzle_without_empty[1:]

    first_objects_idx = puzzle_without_empty[0].index('S')
    objects_idx = [first_objects_idx]

    tree = SigmaTree(first_objects_idx)

    for splitter_line_id in range(len(puzzle_without_first)):
        splitter_line = puzzle_without_first[splitter_line_id]
        splitters_idx = [i for i in range(len(splitter_line)) if splitter_line[i] == '^']
        duplicates = set(objects_idx) & set(splitters_idx)
        for duplicate in duplicates:
            left, right = duplicate - 1, duplicate + 1
            objects_idx.remove(duplicate)
            if left not in objects_idx:
                objects_idx.append(left)
            if right not in objects_idx:
                objects_idx.append(right)
        # print(objects_idx)
        tree.add_range([TreeNode(x) for x in objects_idx])

    tree.print_tree()
    ans = tree.get_paths()

    print(f'Part2: {ans}')


part1()
part2()