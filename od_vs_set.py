import cProfile
import random
import timeit
import uuid

from functools import partial
from pprint import pprint

from collections import OrderedDict


def generate_data(
    node_random_fill=False,
    list_length=10000,
    duplicate_chance=50,
):
    data = []

    while list_length > 0:
        node = str(uuid.uuid4())

        if random.randint(0, 101) < duplicate_chance and list_length != 1:
            data += [node, node]
            list_length -= 2
        else:
            data.append(node)
            list_length -= 1

    return data


def perform_od(data):
    return OrderedDict.fromkeys(data)


def perform_set(data):
    return set(data)


def measure():
    results = {
        'od': {
            'timeit': 0,
            'cprof': 0,
        },
        'set': {
            'timeit': 0,
            'cprof': 0,
        },
    }

    count = 0

    for list_length in range(1000, 10001, 1000):
        for duplicate_chance in range(101):
            data = generate_data(
                list_length=list_length,
                duplicate_chance=duplicate_chance,
            )

            results['od']['timeit'] += timeit.Timer(
                partial(perform_od, data)
            ).timeit(0)

            results['set']['timeit'] += timeit.Timer(
                partial(perform_set, data)
            ).timeit(0)

            pr = cProfile.Profile()

            pr.runcall(perform_od, data)

            results['od']['cprof'] = pr.getstats()[0].totaltime

            pr.clear()

            pr.runcall(perform_set, data)

            results['set']['cprof'] = pr.getstats()[0].totaltime

            count += 1

    for strct, _ in results.items():
        for test, sec in results[strct].items():
            results[strct][test] = sec / count * 1000 * 100

    return results


def main():
    pprint(measure())

if __name__ == '__main__':
    main()
