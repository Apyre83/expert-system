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
