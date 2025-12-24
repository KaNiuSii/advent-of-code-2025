def get_input():
    with open("4.txt", "r") as f:
        return f.read().strip().split()


def get_window(grid, mid_x, mid_y, size):
    window = []

    start_y = (mid_y - size // 2) if (mid_y - size // 2) > 0 else 0
    end_y = (mid_y + size // 2) if (mid_y + size // 2) < len(grid) else len(grid) - 1


    start_x = (mid_x - size // 2) if (mid_x - size // 2) > 0 else 0
    end_x = (mid_x + size // 2) if (mid_x + size // 2) < len(grid[0]) else len(grid[0]) - 1

    for y in range(start_y, end_y + 1):
        window.append(grid[y][start_x:end_x + 1])
    return window


def part1():
    grid = get_input()

    y = len(grid)
    x = len(grid[0])

    ans = 0

    for i in range(y):
        for j in range(x):
            window = get_window(grid, j,i, 3)
            flatten = [x for xs in window for x in xs]

            if grid[i][j] == '@' and flatten.count('@') < 5:
                ans += 1

    print(f'Part 1: {ans}')


def part2():
    grid = get_input()

    y = len(grid)
    x = len(grid[0])

    ans = 0
    removed = [(0,0)]

    while len(removed) != 0:
        removed = []
        for i in range(y):
            for j in range(x):
                window = get_window(grid, j, i, 3)
                flatten = [x for xs in window for x in xs]

                if grid[i][j] == '@' and flatten.count('@') < 5:
                    removed.append((i, j))
        ans += len(removed)
        for cords in removed:
            i, j = cords[0], cords[1]
            row_list = [x for x in grid[i]]
            row_list[j] = '.'
            grid[i] = ''.join(row_list)


    print(f'Part 2: {ans}')

part1()
part2()