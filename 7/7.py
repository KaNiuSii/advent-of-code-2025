
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
        hits_in_splitters = set(objects_idx) & set(splitters_idx)
        ans += len(hits_in_splitters)
        for hit in hits_in_splitters:
            left, right = hit - 1, hit + 1
            objects_idx.remove(hit)
            if left not in objects_idx:
                objects_idx.append(left)
            if right not in objects_idx:
                objects_idx.append(right)

    print(f'Part1: {ans}')

class ParticleNode:
    def __init__(self, y: int, x: int, parents: list | None):
        self.y = y
        self.x = x
        self.parents = parents
        self.left = None
        self.right = None
        self.splitted = False


def part2():
    ans = 0

    puzzle = get_input()
    puzzle_without_empty = [puzzle[i] for i in range(len(puzzle)) if i % 2 == 0]
    y = 0

    first_obj = puzzle_without_empty[0].index('S')

    objects_idx = [first_obj]
    nodes = [ParticleNode(y, first_obj, None)]

    for splitter_line in puzzle_without_empty[1:]:
        y += 1

        splitters_idx = [i for i in range(len(splitter_line)) if splitter_line[i] == '^']
        hits_in_splitters = set(objects_idx) & set(splitters_idx)

        for hit in hits_in_splitters:
            left, right = hit - 1, hit + 1
            objects_idx.remove(hit)
            if left not in objects_idx:
                objects_idx.append(left)
            if right not in objects_idx:
                objects_idx.append(right)


    print(f'Part2: {ans}')


part1()
part2()