import time
import ex1
import search as search
import utils as utils

def run_problem(func, targs=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)
    except Exception as e:
        result = (-3, e)
    return result


def solve_problems(problem):
    try:
        p = ex1.create_elevators_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None

    result = run_problem((lambda p: search.astar_search(p, p.h_astar)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print(len(solution), solution)
    else:
        print("no solution")


init_state_p1 = {
    "height": 6,
    "Elevators": {
        0: (0, (0, 1, 2, 3), 8),
        1: (4, (2, 4, 5, 6), 10)
    },
    "Persons": {
        10: (0, 3, 3),
        11: (2, 4, 6),
        12: (4, 5, 0)
    }
}

init_state_e1 = {
    "height": 5,
    "Elevators": {
        0: (0, (0, 1, 2, 3, 4, 5), 15),
        1: (5, (0, 1, 2, 3, 4, 5), 15)
    },
    "Persons": {
        10: (0, 3, 5),
        11: (5, 3, 0),
        12: (3, 3, 1)
    }
}

init_state_e2 = {
    "height": 6,
    "Elevators": {
        0: (0, (0, 1, 2, 3), 10),
        1: (6, (3, 4, 5, 6), 10)
    },
    "Persons": {
        10: (1, 3, 3),
        11: (5, 3, 4),
        12: (0, 3, 2)
    }
}

init_state_e3 = {
    "height": 6,
    "Elevators": {
        0: (0, (0, 1, 2, 3, 4), 10),
        1: (6, (2, 4, 5, 6), 10)
    },
    "Persons": {
        10: (0, 3, 5),
        11: (6, 3, 1),
        12: (3, 4, 6)
    }
}

init_state_e4 = {
    "height": 5,
    "Elevators": {
        0: (0, (0, 1, 2, 3, 4, 5), 7),
        1: (5, (0, 1, 2, 3, 4, 5), 7)
    },
    "Persons": {
        10: (0, 5, 5),
        11: (0, 5, 3),
        12: (5, 5, 0)
    }
}

init_state_e5 = {
    "height": 7,
    "Elevators": {
        0: (0, (0, 1, 2, 3, 4), 12),
        1: (7, (3, 4, 5, 6, 7), 12)
    },
    "Persons": {
        10: (1, 4, 3),
        11: (6, 4, 7),
        12: (0, 4, 7)
    }
}

init_state_m1 = {
    "height": 6,
    "Elevators": {
        0: (0, (0, 1, 2, 3,), 12),
        1: (6, (3, 4, 5, 6,), 12)
    },
    "Persons": {
        10: (0, 4, 5),
        11: (5, 4, 0),
        12: (2, 4, 6),
        13: (5, 4, 1)
    }
}

init_state_m2 = {
    "height": 8,
    "Elevators": {
        0: (0, (0, 1, 2, 3, 4), 10),
        1: (4, (2, 4, 6, 8), 10)
    },
    "Persons": {
        10: (0, 3, 8),
        11: (8, 3, 0),
        12: (2, 3, 6),
        13: (6, 3, 1)
    }
}

init_state_m3 = {
    "height": 8,
    "Elevators": {
        0: (0, (0, 1, 2, 3, 4), 10),
        1: (4, (2, 4, 6, 8), 10),
        2: (4, (7, 2), 10)
    },
    "Persons": {
        10: (0, 3, 8),
        11: (8, 3, 0),
        12: (2, 3, 7),
        13: (6, 3, 1)
    }
}

init_state_m4 = {
    "height": 6,
    "Elevators": {
        0: (0, (0, 1, 2, 3, 4, 5, 6), 8),
        1: (6, (0, 1, 2, 3, 4, 5, 6), 8)
    },
    "Persons": {
        10: (0, 5, 6),
        11: (0, 5, 4),
        12: (6, 5, 0),
        13: (6, 5, 2),
        14: (3, 5, 6)
    }
}

init_state_m5 = {
    "height": 8,
    "Elevators": {
        0: (0, (0, 1, 2, 3, 4), 10),
        1: (4, (4, 5, 6, 7, 8), 10)
    },
    "Persons": {
        10: (0, 6, 8),
        11: (0, 4, 5),
        12: (8, 6, 0),
        13: (8, 5, 3)
    }
}


def main():
    start = time.time()
    problems = [
        ("p1  (original)", init_state_p1),
        ("e1  (easy)",     init_state_e1),
        ("e2  (easy)",     init_state_e2),
        ("e3  (easy)",     init_state_e3),
        ("e4  (easy)",     init_state_e4),
        ("e5  (easy)",     init_state_e5),
        ("m1  (medium)",   init_state_m1),
        ("m2  (medium)",   init_state_m2),
        ("m3  (medium)",   init_state_m3),
        ("m4  (medium)",   init_state_m4),
        ("m5  (medium)",   init_state_m5),
    ]
    for name, p in problems:
        t0 = time.time()
        print(f"[{name}] ", end="")
        solve_problems(p)
        print(f"  ({time.time() - t0:.2f}s)")
    end = time.time()
    print('Submission took:', end - start, 'seconds.')


if __name__ == '__main__':
    main()
