from typing import List, Dict


known_variables: Dict[str, int] = {} # The variables and their values


def calculate_operand(operator: str, _operand1: str | int, _operand2: str | int = None) -> int:
    """
    Calculates the result of an operation between two operands.
    :param operator: the operator to use
    :param operand1: the first value / variable
    :param operand2: the second value / variable
    :return: the result of the operation or UNDEFINED if the operation could not be done
    """

    operand1: str = str(_operand1)
    operand2: str = str(_operand2)

    if (operator == "!"):
        if (operand1.isnumeric()): return int(not int(operand1)) # We have the value, hence we can do the calcul

        # Find the value of the operand
        for rule in rules:
            if operand1 in rule.output_variables:
                if (rule.solve() == Rule.UNDEFINED): continue # The rule could not be solved, hence we can't use it
                # Since it could solve the rule, it added the result to the known_variables and we can then use it
                return int(not known_variables[operand1])
        return Rule.UNDEFINED


    elif (operator == "+"): # AND: both operands must be True, hence known
        if (operand1.isnumeric() and operand2.isnumeric()): return int(operand1 and operand2)

        # Find the value of the operands
        for rule in rules:
            if operand1 in rule.output_variables or operand2 in rule.output_variables:
                rule.solve()

        if (not operand1 in known_variables or not operand2 in known_variables): return Rule.UNDEFINED
        return int(known_variables[operand1] and known_variables[operand2])


    elif (operator == "|"): # OR: one of the operands must be True, hence known
        if (operand1.isnumeric() and operand2.isnumeric()): return int(operand1 or operand2)

        # Find the value of the operands
        for rule in rules:
            if operand1 in rule.output_variables or operand2 in rule.output_variables:
                rule.solve()

        if (not operand1 in known_variables and not operand2 in known_variables): return Rule.UNDEFINED
        if (operand1 in known_variables and known_variables[operand1] == True) or \
           (operand2 in known_variables and known_variables[operand2] == True): return True
        if (operand1 in known_variables and known_variables[operand1] == False) and \
           (operand2 in known_variables and known_variables[operand2] == False): return False
        return Rule.UNDEFINED


    elif (operator == "^"): # XOR: one of the operands must be True, but not both, hence known
        if (operand1.isnumeric() and operand2.isnumeric()): return int(operand1 ^ operand2)

        # Find the value of the operands
        for rule in rules:
            if operand1 in rule.output_variables or operand2 in rule.output_variables:
                rule.solve()

        if (not operand1 in known_variables or not operand2 in known_variables): return Rule.UNDEFINED
        return int(known_variables[operand1] ^ known_variables[operand2])

    else: return Rule.UNDEFINED


class Rule:
    """
    A Rule is a logical expression that has a condition and a conclusion.
    The condition is a logical expression that must be true for the conclusion to be true.
    The conclusion is a logical expression that is true if the condition is true.
    The operator of the Rule is the implication operator (=>). (note that bonus would include <=>)
    """

    SUCCESS = 0
    UNDEFINED = -1

    operators: List[str] = ["!", "+", "|", "^"] # The operators that are used in the Rule. Not that there is also parenthesis, but they are not considered operators here.

    left_member_rpn: List[str] = []     # The condition of the Rule
    right_member_rpn: List[str] = []    # The conclusion of the Rule
    output_variables: List[str] = []    # The variables that are affected by the Rule
    input_variables: List[str] = []     # The variables that are used in the Rule

    def __init__(self, left_member_rpn: List[str], right_member_rpn: List[str], output_variables: List[str], input_variables: List[str]):
        self.left_member_rpn = left_member_rpn
        self.right_member_rpn = right_member_rpn
        self.output_variables = output_variables
        self.input_variables = input_variables


    def solve(self) -> int:
        """
        Solves the Rule by using the condition to solve the conclusion.
        Since the left member is an RPN, we can use a stack to solve it.
        We suppose that the left_member_rpn is valid

        :return: If the solve was successful or not using the constants SUCCESS and UNDEFINED
        """

        stack: List[str | int] = [] # The stack will contain operators and values. The value could either be a variable if it's not solved yet, or a number if it's solved.
        for token in self.left_member_rpn:
            if token in self.operators:
                if token == "!":
                    _tmp = calculate_operand(token, stack.pop())
                    if (_tmp == self.UNDEFINED): return self.UNDEFINED
                    stack.append(_tmp)
                else:
                    _var = stack.pop()
                    _tmp = calculate_operand(token, stack.pop(), _var)
                    if (_tmp == self.UNDEFINED): return self.UNDEFINED
                    stack.append(_tmp)

            elif token.isupper():
                stack.append(token)

            else: pass

        # The stack should now contain only one element, which is the result of the left member
        if (len(stack) != 1): return self.UNDEFINED
        if (stack[0] == self.UNDEFINED): return self.UNDEFINED
        known_variables[self.output_variables[0]] = stack[0]
        return self.SUCCESS


"""
A | B => C
D | E => F
C | F => G

=ABDE
?G
"""
rules = [
    Rule(["A", "B", "+"], ["C"], ["C"], ["A", "B"]),
    Rule(["D", "E", "+"], ["F"], ["F"], ["D", "E"]),
    Rule(["C", "!", "F", "!", "+"], ["G"], ["G"], ["C", "F"]),
]

known_variables["A"] = False
known_variables["B"] = True
known_variables["D"] = False
known_variables["E"] = True

if (rules[2].solve() == Rule.UNDEFINED): print("UNDEFINED")
else:
    print("SUCCESS, ", known_variables)