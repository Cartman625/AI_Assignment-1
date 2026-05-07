import search as search
import utils as utils

id = ["No numbers - I'm special!"]


class ElevatorsProblem(search.Problem):
    """This class implements an elevators problem"""

    def __init__(self, initial):
        search.Problem.__init__(self, initial)

    def successor(self, state):
        utils.raiseNotDefined()

    def goal_test(self, state):
        utils.raiseNotDefined()

    def h_astar(self, node):
        utils.raiseNotDefined()


def create_elevators_problem(game):
    print("<<create_elevators_problem")
    return ElevatorsProblem(game)


if __name__ == '__main__':
    import ex1_check
    ex1_check.main()
