import math


def get_input():
    with open("8.txt", "r") as f:
        return f.read().split()

def calc_3d_distance(one, two):
    return math.sqrt((one[0] - two[0]) ** 2 + (one[1] - two[1]) ** 2 + (one[2] - two[2]) ** 2)

def part1():
    ans = 1

    make_pairs = 1000

    puzzle = get_input()

    jboxes = []
    for line in puzzle:
        xyz = [int(v) for v in line.split(',')]
        jboxes.append((xyz[0], xyz[1], xyz[2]))

    circuits = []

    distances_by_pair = [(sorted([one, two]), calc_3d_distance(one, two)) for one in jboxes for two in jboxes if one != two]
    closest_pairs = sorted(set([(x[0][0], x[0][1], x[1]) for x in distances_by_pair]), key=lambda x: x[2])

    for i in range(make_pairs):
        one, two = closest_pairs[i][0], closest_pairs[i][1]
        matching_circuit = [c for c in circuits if one in c or two in c]
        if len(matching_circuit) == 0:
            circuits.append([one, two])
        elif len(matching_circuit) == 1:
            c = matching_circuit[0]
            if one in c and two in c:
                continue
            c.append(one if one not in c else two)
        else:
            merged_circuit = matching_circuit[0] + matching_circuit[1]
            for c in matching_circuit:
                circuits.remove(c)
            circuits.append(merged_circuit)


    for c in sorted(circuits, key=lambda x: len(x), reverse=True)[:3]:
        ans *= len(c)

    print(f'Part1: {ans}')

def part2():
    ans = 1

    puzzle = get_input()

    jboxes = []
    for line in puzzle:
        xyz = [int(v) for v in line.split(',')]
        jboxes.append((xyz[0], xyz[1], xyz[2]))

    circuits = []

    distances_by_pair = [(sorted([one, two]), calc_3d_distance(one, two)) for one in jboxes for two in jboxes if
                         one != two]
    closest_pairs = sorted(set([(x[0][0], x[0][1], x[1]) for x in distances_by_pair]), key=lambda x: x[2])

    def jbox_in_any_circuit(jbox):
        return jbox in [jb for c in circuits for jb in c]

    for pair in closest_pairs:
        one, two = pair[0], pair[1]
        matching_circuit = [c for c in circuits if one in c or two in c]
        if len(matching_circuit) == 0:
            circuits.append([one, two])
        elif len(matching_circuit) == 1:
            c = matching_circuit[0]
            if one not in c or two not in c:
                c.append(one if one not in c else two)
        else:
            merged_circuit = matching_circuit[0] + matching_circuit[1]
            for c in matching_circuit:
                circuits.remove(c)
            circuits.append(merged_circuit)
        if len(circuits) == 1 and all([jbox_in_any_circuit(jb) for jb in jboxes]):
            ans = one[0] * two[0]
            break

    print(f'Part2: {ans}')

part1()
part2()