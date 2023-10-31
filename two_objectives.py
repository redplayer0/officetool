from pprint import pprint

from ortools.linear_solver import pywraplp

num_tasks = 12
num_people = 4
constraints = {
    0: [0, 1, 2, 3, 4],
    1: [0, 1, 4, 9],
    2: [0, 3, 7, 8],
    3: [0, 1, 5, 6, 9],
}
costs = [
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
limit = 3
x = {}


def run():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    for t in range(num_tasks):
        for p in range(num_people):
            if t not in constraints[p]:
                x[t, p] = solver.IntVar(0, 1, "")

    for t in range(num_tasks):
        solver.Add(
            solver.Sum([x[t, p] for p in range(num_people) if t not in constraints[p]])
            <= 1
        )

    for p in range(num_people):
        solver.Add(
            solver.Sum([x[t, p] for t in range(num_tasks) if t not in constraints[p]])
            <= 3
        )

    objectives = []
    objectives.append(-10 * solver.Sum(x.values()))

    for t in range(num_tasks):
        for p in range(num_people):
            if t not in constraints[p]:
                objectives.append(costs[p][t] * x[t, p])

    solver.Minimize(solver.Sum(objectives))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f"Total cost = {solver.Objective().Value()}\n")
        for t in range(num_tasks):
            not_assigned = True
            for p in range(num_people):
                if t not in constraints[p]:
                    if x[t, p].solution_value() > 0.5:
                        not_assigned = False
                        print(
                            f"Worker {p} assigned to task {t}."
                            + f" Cost: {costs[p][t]}"
                        )
            if not_assigned:
                print(f"task {t} not assigned")
    else:
        print("No solution found.")


if __name__ == "__main__":
    import sys

    run()

    # target = sys.argv[1]
    # output = sys.argv[2]
