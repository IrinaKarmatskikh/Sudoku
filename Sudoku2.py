from pulp import *


def solve_sudoku(input_sudoku):
    prob = LpProblem("Sudoku_problem")

    rows = cols = boxes = range(0, 9)
    values = range(1, 10)

    cell_vars = LpVariable.dicts("cell_value", (rows, cols, values), cat='Binary')
    # print(cell_vars)

    objective = lpSum(0)
    prob.setObjective(objective)
    add_constraints(prob, input_sudoku, cell_vars, rows, cols, boxes, values)
    prob.solve()

    if LpStatus[prob.status] == 'Optimal':
        solution = extract_solution(cell_vars, rows, cols, values)
        print_solution(solution, rows, cols)
    else:
        print("FAIL: no optimal solution")


def add_constraints(prob, input_sudoku, cell_vars, rows, cols, boxes, values):
    # Constraint value for a cell
    for i in rows:
        for j in cols:
            prob.addConstraint(LpConstraint(e=lpSum([cell_vars[i][j][k] for k in values]),
                                            sense=LpConstraintEQ, rhs=1))

    # Constraint row
    for i in rows:
        for k in values:
            prob.addConstraint(LpConstraint(e=lpSum([cell_vars[i][j][k] * k for j in cols]),
                                            sense=LpConstraintEQ, rhs=k))

    # Constraint column
    for j in cols:
        for k in values:
            prob.addConstraint(LpConstraint(e=lpSum([cell_vars[i][j][k] * k for i in rows]),
                                            sense=LpConstraintEQ, rhs=k))

    # Constraint box 3x3
    for i in boxes:
        box_row = int(i / 3)
        box_col = int(i % 3)

        for k in values:
            prob.addConstraint(LpConstraint(e=lpSum(
                [cell_vars[box_row * 3 + row][box_col * 3 + col][k] * k for col in range(0, 3) for row in
                 range(0, 3)]), sense=LpConstraintEQ, rhs=k))

    # Constraint input
    for i in rows:
        for j in cols:
            if input_sudoku[i][j] != 0:
                prob.addConstraint(LpConstraint(e=lpSum([cell_vars[i][j][k]*k for k in values]),
                                                sense=LpConstraintEQ, rhs=input_sudoku[i][j]))


def extract_solution(cell_vars, rows, cols, values):
    solution = [[0 for i in cols] for j in rows]
    for i in rows:
        for j in cols:
            for k in values:
                if value(cell_vars[i][j][k]):
                    solution[i][j] = k
    return solution


def print_solution(solution, rows, cols):
    print(f"\nResult:")

    print("\n\n+ ----------- + ----------- + ----------- +", end="")
    for i in rows:
        print("\n", end="\n|  ")
        for j in cols:
            num_end = "  |  " if ((j + 1)%3 == 0) else "   "
            print(solution[i][j], end=num_end)

        if (i+1)%3 == 0:
            print("\n\n+ ----------- + ----------- + ----------- +", end="")


input = [
    [2, 0, 0, 0, 0, 5, 8, 9, 0],
    [0, 6, 0, 0, 9, 0, 7, 1, 0],
    [9, 0, 0, 7, 0, 0, 0, 0, 4],

    [0, 0, 0, 0, 6, 0, 0, 5, 8],
    [0, 0, 6, 0, 0, 0, 4, 0, 0],
    [5, 9, 0, 0, 3, 0, 0, 0, 0],

    [3, 0, 0, 0, 0, 8, 0, 0, 7],
    [0, 4, 9, 0, 2, 0, 0, 8, 0],
    [0, 8, 5, 1, 0, 0, 0, 0, 9]
]

solve_sudoku(input)
