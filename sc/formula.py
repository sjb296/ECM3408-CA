import re

flt_s = "[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)"
NUM = re.compile(rf"^{flt_s}$")
cell_s = "[a-zA-Z]+[0-9]+"
CELL = re.compile(rf"^{cell_s}$")
ARITHMETIC = re.compile(
    rf"^([a-zA-Z]+[0-9]+|{flt_s}) *[\*\+\-\/] *([a-zA-Z]+[0-9]+|{flt_s})$"
)


def eval_formula(db, formula):
    """Returns the result of the formula."""
    if valid_formula(formula):
        if NUM.match(formula):
            return float(formula)
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

    # Separate out the operands
    if CELL.match(operands[0]):
        operands[0] = db.get_cell(operands[0])["formula"]  # Unpack JSON
    elif NUM.match(operands[0]):
        operands[0] = float(operands[0])
    if CELL.match(operands[1]):
        operands[1] = db.get_cell(operands[1])["formula"]  # Unpack JSON
    elif NUM.match(operands[1]):
        operands[1] = float(operands[1])

    # Perform the operation
    if operator == "+":
        result = float(operands[0]) + float(operands[1])
    elif operator == "-":
        result = float(operands[0]) - float(operands[1])
    elif operator == "*":
        result = float(operands[0]) * float(operands[1])
    elif operator == "/":
        result = float(operands[0]) / float(operands[1])

    if result.is_integer():
        return int(result)


def valid_formula(formula):
    """Returns True if the formula is a valid spreadsheet formula."""
    if NUM.match(formula) or CELL.match(formula) or ARITHMETIC.match(formula):
        return True
    return False
