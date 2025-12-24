def get_input():
    with open("1.txt", "r") as f:
        return f.read().strip().split()

def part2():
    dial_index = 50

    ans = 0

    for line in get_input():
        side = -1 if line[0] == 'L' else 1
        times = int(line[1:])

        for time in range(times):
            dial_index += side

            if dial_index == -1:
                dial_index = 99
            if dial_index == 100:
                dial_index = 0
            if dial_index == 0:
                ans += 1

    print(f'Answer: {ans}')

def part1():
    dial_index = 50

    ans = 0

    for line in get_input():
        side = -1 if line[0] == 'L' else 1
        times = int(line[1:])

        for time in range(times):
            dial_index += side

            if dial_index == -1:
                dial_index = 99
            if dial_index == 100:
                dial_index = 0

        if dial_index == 0:
            ans += 1

    print(f'Answer: {ans}')

part1()
part2()