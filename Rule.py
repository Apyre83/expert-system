from calculate import calculate_operand

class Rule:
    def __init__(self, left_operand_rpn, right_operand_rpn, relation):
        self.left_operand_rpn = left_operand_rpn
        self.right_operand_rpn = right_operand_rpn
        self.relation = relation
        self.input_variables = self.extract_variables(left_operand_rpn)
        self.output_variables = self.extract_variables(right_operand_rpn)

    def __str__(self):
        return f"{self.left_operand_rpn} {self.relation} {self.right_operand_rpn} | In{self.input_variables} / {self.output_variables}"

    def extract_variables(self, rpn_expression):
        return set([char for char in rpn_expression if char.isalpha() and char.isupper()])

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
