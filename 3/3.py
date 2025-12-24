def get_input():
    with open("3.txt", "r") as f:
        return f.read().strip().split()

def part1():
    ans = 0

    for bank in get_input():
        batteries = []
        for i in range(len(bank)):
            batteries.append(int(bank[i]))

        first = max(batteries[:len(batteries) - 1])
        idx = batteries.index(first)
        second = max(batteries[idx + 1:])
        mx = f'{first}{second}'
        ans += int(mx)
    print(f'Part 1: {ans}')

def part2():
    ans = 0

    for bank in get_input():
        batteries = []
        for i in range(len(bank)):
            batteries.append(int(bank[i]))

        window = 11
        mx = ''
        idx = -1

        while len(mx) < 12:
            part = (batteries[idx + 1:len(batteries) - window])
            battery = max(part)
            idx = idx + part.index(battery) + 1
            window -= 1
            mx += str(battery)

        ans += int(mx)

    print(f'Part 2: {ans}')

part1()
part2()