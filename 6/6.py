from typing import List


def get_input():
    with open("6test.txt", "r") as f:
        return f.read()

def rewrite(grid):
    rewritten = []
    for col in range(len(grid[0])):
        rewritten.append([])
        for row in range(len(grid)):
            rewritten[col].append(grid[row][col])
    return rewritten

def part1():
    ans = 0

    grid = [x.split() for x in get_input().split("\n")]
    grid = rewrite(grid)

    for row in grid:
        nums, operation = row[:-1], row[::-1][0]
        evaluation = ''.join([nums[0]] + [operation + nums[x] for x in range(len(nums)) if x != 0])
        ans += int(eval(evaluation))

    print(f'Part 1: {ans}')


def fill_whitespace(grid: List[List[str]]):
    copy = grid.copy()
    for row in range(len(copy)):
        sequence = copy[row]
        longest = max([len(x) for x in sequence])
        for col in range(len(copy[row])):
            element = copy[row][col]
            if element == sequence[-1]:
                continue
            prefix = (' ' * (longest - len(element)))
            filled = ''.join([prefix, element])
            copy[row][col] = filled

    return copy

def part2():
    ans = 0

    input_lines = get_input().split('\n')
    last_line = input_lines[-1]

    idx_operators = [x for x in range(len(last_line)) if last_line[x] != ' ']

    grid = []
    for line in input_lines[:-1]:
        row = []
        for i in range(len(idx_operators)):
            idx = idx_operators[i]

            if i < len(idx_operators) - 1:
                next_idx = idx_operators[i + 1]
                part = line[idx:next_idx]
            else:
                part = line[idx:]
            row.append(part)
        grid.append(row)
    print(grid)
    # grid = rewrite(grid)
    # grid = fill_whitespace(grid)
    #
    # num_count = len(grid[0][0])
    #
    # for row in grid:
    #     old_nums, operation = row[:-1], row[::-1][0]
    #     new_nums = []
    #     for num_idx in range(num_count):
    #         new_nums.append(''.join([x[num_idx] for x in old_nums if x[num_idx] != ' ']))
    #     new_nums = new_nums[::-1]
    #     evaluation = ''.join([new_nums[0]] + [operation + new_nums[x] for x in range(len(new_nums)) if x != 0])
    #     ans += int(eval(evaluation))
    #     print(f'{old_nums} {evaluation} = {int(eval(evaluation))}')

    print(f'Part 2: {ans}')

part1()
part2()