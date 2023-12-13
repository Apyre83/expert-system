import parse
from typing import List, Set

class Rule:

    operators = ["+", "|", "^", "!"]
    SUCCESS = 0
    UNKNOWN = -1
    UNDEFINED = -1

    def __init__(self, left_operand_rpn, right_operand_rpn, relation):
        self.left_operand_rpn = left_operand_rpn
        self.right_operand_rpn = right_operand_rpn
        self.relation = relation
        self.input_variables = self.extract_variables(left_operand_rpn)
        self.output_variables = self.extract_variables(right_operand_rpn)

    def __str__(self):
        return f"{self.left_operand_rpn} {self.relation} {self.right_operand_rpn} | In{self.input_variables} / Out{self.output_variables}"

    def extract_variables(self, rpn_expression):
        return tuple(set([char for char in rpn_expression if char.isalpha() and char.isupper()]))

    def solve(self) -> int:
        """
        Solves the Rule by using the condition to solve the conclusion.
        Since the left member is an RPN, we can use a stack to solve it.
        We suppose that the left_member_rpn is valid

        :return: If the solve was successful or not using the constants SUCCESS and UNDEFINED
        """

        stack: List[str | int] = [] # The stack will contain operators and values. The value could either be a variable if it's not solved yet, or a number if it's solved.
        for token in self.left_operand_rpn:
            if token in self.operators:
                if token == "!":
                    _tmp = self.calculate_operand(token, stack.pop())
                    if (_tmp == self.UNDEFINED): return self.UNDEFINED
                    stack.append(_tmp)
                else:
                    _var = stack.pop()
                    _tmp = self.calculate_operand(token, stack.pop(), _var)
                    if (_tmp == self.UNDEFINED): return self.UNDEFINED
                    stack.append(_tmp)

            elif token.isupper():
                stack.append(token)

            else: pass

        # The stack should now contain only one element, which is the result of the left member
        if (len(stack) != 1): return self.UNDEFINED
        if (stack[0] == self.UNDEFINED): return self.UNDEFINED
        parse.known_variables[self.output_variables[0]] = stack[0]
        return self.SUCCESS



    def calculate_operand(self, operator: str, _operand1: str | int, _operand2: str | int = None) -> int:
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
            for rule in parse.rules:
                if operand1 in rule.output_variables:
                    if (rule.solve() == Rule.UNDEFINED): continue # The rule could not be solved, hence we can't use it
                    # Since it could solve the rule, it added the result to the parse.known_variables and we can then use it
                    return int(not parse.known_variables[operand1])
            return Rule.UNDEFINED

        if (operand1.isnumeric() and operand2.isnumeric()): # We have the values, hence we can do the calcul
            if (operator == "+"): return int(operand1 and operand2)
            elif (operator == "|"): return int(operand1 or operand2)
            elif (operator == "^"): return int(operand1 ^ operand2)

        if operand1 in parse.known_variables and operand2 in parse.known_variables: # We have the values, hence we can do the calcul

            if parse.known_variables[operand1] == Rule.UNDEFINED or parse.known_variables[operand2] == Rule.UNDEFINED: pass

            elif (operator == "+"): return int(parse.known_variables[operand1] and parse.known_variables[operand2])
            elif (operator == "|"): return int(parse.known_variables[operand1] or parse.known_variables[operand2])
            elif (operator == "^"): return int(parse.known_variables[operand1] ^ parse.known_variables[operand2])

        if (operator == "+"): # AND: both operands must be True, hence known

            # Find the value of the operands
            for rule in parse.rules:
                if operand1 in rule.output_variables or operand2 in rule.output_variables:
                    rule.solve()

            if (not operand1 in parse.known_variables or not operand2 in parse.known_variables): return Rule.UNDEFINED
            return int(parse.known_variables[operand1] and parse.known_variables[operand2])


        elif (operator == "|"): # OR: one of the operands must be True, hence known

            # Find the value of the operands
            for rule in parse.rules:
                if operand1 in rule.output_variables or operand2 in rule.output_variables:
                    rule.solve()

            if (not operand1 in parse.known_variables and not operand2 in parse.known_variables): return Rule.UNDEFINED
            if (operand1 in parse.known_variables and parse.known_variables[operand1] == True) or \
               (operand2 in parse.known_variables and parse.known_variables[operand2] == True): return True
            if (operand1 in parse.known_variables and parse.known_variables[operand1] == False) and \
               (operand2 in parse.known_variables and parse.known_variables[operand2] == False): return False
            return Rule.UNDEFINED


        elif (operator == "^"): # XOR: one of the operands must be True, but not both, hence known
            if (operand1.isnumeric() and operand2.isnumeric()): return int(operand1 ^ operand2)

            # Find the value of the operands
            for rule in parse.rules:
                if operand1 in rule.output_variables or operand2 in rule.output_variables:
                    rule.solve()

            if (not operand1 in parse.known_variables or not operand2 in parse.known_variables): return Rule.UNDEFINED
            return int(parse.known_variables[operand1] ^ parse.known_variables[operand2])

        else: return Rule.UNDEFINED
