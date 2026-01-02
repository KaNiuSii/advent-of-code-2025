from typing import List


def get_input():
    with open("7.txt", "r") as f:
        return f.read().split()


def part1():
    ans = 0

    draw_lines = True

    puzzle = get_input()
    puzzle_without_empty = [puzzle[i] for i in range(len(puzzle)) if i % 2 == 0]

    start_id = puzzle_without_empty[0].index('S')
    particles_idx = [start_id]

    if draw_lines:
        puzzle[1] = puzzle[1][: start_id] + '|' + puzzle[1][start_id + 1:]

    for splitter_line in puzzle_without_empty[1:]:
        splitters_idx = [i for i in range(len(splitter_line)) if splitter_line[i] == '^']
        hits_in_splitters = set(particles_idx) & set(splitters_idx)

        ans += len(hits_in_splitters)

        for hit in hits_in_splitters:
            left, right = hit - 1, hit + 1
            particles_idx.remove(hit)
            if left not in particles_idx:
                particles_idx.append(left)
            if right not in particles_idx:
                particles_idx.append(right)

        if draw_lines:
            i = puzzle.index(splitter_line)
            for obj in particles_idx:
                puzzle[i + 1] = puzzle[i + 1][: obj] + '|' + puzzle[i + 1][obj + 1:]
                puzzle[i] = puzzle[i][: obj] + '|' + puzzle[i][obj + 1:]

    if draw_lines:
        for line in puzzle:
            print(line)

    print(f'Part1: {ans}')


def part2():
    ans = 0

    puzzle = get_input()
    puzzle_without_empty = [puzzle[i] for i in range(len(puzzle)) if i % 2 == 0]

    start_id = puzzle_without_empty[0].index('S')
    particles = {start_id: 1}

    for splitter_line in puzzle_without_empty[1:]:
        splitters_idx = [i for i in range(len(splitter_line)) if splitter_line[i] == '^']
        tmp = {}
        for k, v in particles.items():
            if k in splitters_idx:
                left, right = k - 1, k + 1
                tmp[k] = -v if k not in tmp.keys() else tmp[k] - v
                tmp[left] = v if left not in tmp.keys() else tmp[left] + v
                tmp[right] = v if right not in tmp.keys() else tmp[right] + v

        for k, v in tmp.items():
            particles[k] = v if k not in particles.keys() else particles[k] + v

    ans += sum([v for v in particles.values()])

    print(f'Part2: {ans}')


part1()
part2()