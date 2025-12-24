def get_input():
    with open("2.txt", "r") as f:
        return f.read().strip().split(',')

def part1():
    ans = 0

    for row in get_input():
        splitted = row.split('-')
        first_id, second_id = int(splitted[0]), int(splitted[1])

        for i in range(first_id, second_id + 1):
            i_string = str(i)
            length = len(i_string)
            half = length // 2
            # print(i_string, '-', i_string[:half], i_string[half:])
            if length % 2 == 0 and i_string[:half].strip() == i_string[half:].strip():
                # print(i_string)
                ans += int(i_string)

    print(f'Part 1: {ans}')




def part2():
    ans = 0

    for row in get_input():
        splitted = row.split('-')
        first_id, second_id = int(splitted[0]), int(splitted[1])

        for i in range(first_id, second_id + 1):
            i_string = str(i)
            if is_repeating(i_string):
                ans += int(i_string)

    print(f'Part 2: {ans}')

# 80 80 80
def is_repeating(i_string):
    for window in range(1,len(i_string) // 2 + 1):
        if i_string[:window] * (len(i_string) // window) == i_string:
            return True
    return False

part1()
part2()