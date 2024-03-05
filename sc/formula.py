import re

NUM = re.compile(r"^[0-9]+$")
CELL = re.compile(r"^[a-zA-Z]+[0-9]+$")
ARITHMETIC = re.compile(r"^[a-zA-Z]*[0-9]+ *[\*\+\-\/] *[a-zA-Z]*[0-9]+$")


def eval_formula(db, formula):
    """Returns the result of the formula."""
    # print(f"Evaluating formula: {formula}")
    if valid_formula(formula):
        if NUM.match(formula):
            return int(formula)
        elif CELL.match(formula):
            return list(db.get_cell(formula).values())[0]  # Unpack JSON
        elif ARITHMETIC.match(formula):
            return eval_arithmetic(db, formula)
    return "Invalid formula"


def eval_arithmetic(db, formula):
    """Returns the result of the arithmetic formula."""
    operator = re.search(r"[\*\+\-\/]", formula).group()
    operands = formula.split(operator)
    operands = [operand.strip() for operand in operands]  # remove ws
    # print(f"Operands: {operands}")

    # Separate out the operands
    if CELL.match(operands[0]):
        operands[0] = list(db.get_cell(operands[0]).values())[0]  # Unpack JSON
    elif NUM.match(operands[0]):
        operands[0] = int(operands[0])
    if CELL.match(operands[1]):
        operands[1] = list(db.get_cell(operands[1]).values())[0]  # Unpack JSON
    elif NUM.match(operands[1]):
        operands[1] = int(operands[1])

    # Perform the operation
    if operator == "+":
        # print(f"Adding {operands[0]} and {operands[1]}")
        return int(operands[0]) + int(operands[1])
    elif operator == "-":
        return int(operands[0]) - int(operands[1])
    elif operator == "*":
        return int(operands[0]) * int(operands[1])
    elif operator == "/":
        return int(operands[0]) / int(operands[1])


def valid_formula(formula):
    """Returns True if the formula is a valid spreadsheet formula."""
    if NUM.match(formula) or CELL.match(formula) or ARITHMETIC.match(formula):
        return True
    return False


# def db.get_cell(cell):  # dummy
#    return 2
