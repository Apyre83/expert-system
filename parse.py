from typing import Tuple
import re
import Rule

# Known variables and their values
# 0 = False, 1 = True, -1 = Undefined
known_variables = {}

# Queries declared variable in files
queries = set()

# List of rules
rules = []

def parse_line(line: str) -> Tuple[str, str]:
    """
    Analyzes a line of text and categorizes it as a comment, rule, fact, or query.
    :param line: A string representing a line from the file.
    :return: A tuple containing the type of the line and its content.
    """
    line = line.strip()
    line = re.sub(r'#.*$', '', line).strip()

    if line == "":
        return ("empty", line)
    if re.match(r'^[A-Z!+|^()=>< ]+=>', line) or re.match(r'^[A-Z!+|^()=>< ]+<=>', line):
        return ("rule", line)
    elif line.startswith("="):
        return ("fact", line[1:])
    elif line.startswith("?"):
        return ("query", line[1:])
    else:
        return ("unknown", line)

def is_valid_rpn(rpn_expression: str) -> bool:
    """
    Checks if a given RPN (Reverse Polish Notation) expression is valid.
    :param rpn_expression: The RPN expression to check.
    :return: True if the expression is valid, False otherwise.
    """
    stack = 0
    i = 0
    while i < len(rpn_expression):
        char = rpn_expression[i]

        if char.isalpha() and char.isupper():
            stack += 1
        elif char in ['+', '|', '^']:
            if stack < 2:
                return False
            stack -= 1
        elif char == '!':
            if i + 1 < len(rpn_expression) and rpn_expression[i + 1].isalpha() and rpn_expression[i + 1].isupper():
                stack += 1
                i += 1
            else:
                return False
        else:
            return False

        i += 1
    return stack == 1

def to_rpn(expression: str) -> str:
    """
    Converts a regular mathematical/logical expression to Reverse Polish Notation (RPN).
    :param expression: The expression to convert.
    :return: The converted RPN expression as a string.
    """
    precedence = {'!': 4, '^': 3, '|': 2, '+': 1, '(': 0, ')': 0}
    output = []
    stack = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isalpha() and char.isupper():
            output.append(char)
        elif char == '!':
            if i + 1 < len(expression) and expression[i + 1].isalpha() and expression[i + 1].isupper():
                output.append(char + expression[i + 1])
                i += 1
            else:
                return "Error: operator mismatch"
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
            else:
                return "Error: parenthesis mismatch"
            if i + 1 < len(expression) and expression[i + 1] not in ['^', '|', '+', ')', '']:
                return "Error: invalid character after parenthesis"
        else:
            while stack and precedence[char] <= precedence[stack[-1]]:
                output.append(stack.pop())
            stack.append(char)

        i += 1

    while stack:
        output.append(stack.pop())

    return ''.join(output)

def fill_known_undefined_variables(parsed_content):
    """
    Fills the known_variables dictionary with undefined variables found in rules, setting their value to -1 (undefined).
    :param parsed_content: Parsed content containing types and contents including rules.
    """
    for line_type, content in parsed_content:
        if line_type == "rule":
            for char in content:
                if char.isupper() and char not in known_variables:
                    known_variables[char] = -1

def validate_rule(rule: str) -> bool:
    """
    Validates a single rule, ensuring it adheres to the defined syntax and structure.
    :param rule: The rule to validate.
    :return: True if the rule is valid, raises a ValueError otherwise.
    """

    rule = rule.replace(" ", "")

    if not re.match(r'^[A-Z=!<>+|^() ]+$', rule):
        raise ValueError(f"Error: Invalid characters in rule ({rule}).")

    operators = re.findall(r'[<=>]+', rule)

    if len(operators) != 1 or operators[0] not in ['=>', '<=>']:
        raise ValueError(f"Error: Rule must contain exactly one valid implication operator : => or <=> ({rule}).")
    else :
        relation = operators[0]

    left_side, right_side = re.split(r'[<=>]+', rule, maxsplit=1)

    if not left_side.strip() or not right_side.strip():
        raise ValueError(f"Error: Rule must have at least one operand on each side ({rule}).")

    left_side = to_rpn(left_side)
    right_side = to_rpn(right_side)
    if not is_valid_rpn(left_side) or not is_valid_rpn(right_side):
        raise ValueError(f"Error: Rule is not valid ({rule}).")
    rules.append(Rule.Rule(left_side, right_side, relation))

    return True

def validate_file(parsed_content):
    """
    Validates the contents of a parsed file, including rules, facts, and queries.
    :param parsed_content: The parsed content of the file.
    :raises ValueError: If any part of the file content is invalid.
    """
    has_rule, has_fact, has_query = False, False, False

    for line_type, content in parsed_content:
        if line_type == "unknown":
            raise ValueError(f"Error: Unknown line type detected ({content}).")

        if line_type == "rule":
            try:
                validate_rule(content)
                has_rule = True
            except ValueError as e:
                print(e)
                exit(1)

        if line_type == "fact":
            has_fact = True
            if not re.match(r'^[A-Z]*$', content):
                raise ValueError(f"Error: Invalid characters in facts ({content}).")
            for fact in content:
                if fact in known_variables:
                    raise ValueError(f"Error: Duplicate fact detected ({fact}).")
                known_variables[fact] = True

        if line_type == "query":
            has_query = True
            if not re.match(r'^[A-Z]+$', content):
                raise ValueError(f"Error: Invalid characters in query or query is empty ({content}).")
            for query in content:
                if query in queries:
                    raise ValueError(f"Error: Duplicate query detected ({query}).")
                queries.add(query)

    if not has_rule:
        raise ValueError("Error: Missing rules.")
    elif not has_fact:
        raise ValueError("Error: Missing facts. Even if there are no facts, there must be an empty fact section, beginning with \"=\".")
    elif not has_query:
        raise ValueError("Error: Missing queries.")

def parse_file(file_path: str) -> bool:
    """
    Parses the content of a file and validates it.
    :param file_path: Path to the file to be parsed.
    :return: True if the file content is valid, False otherwise.
    """
    parsed_content = []
    with open(file_path, "r") as file:
        for line in file:
            parsed_content.append(parse_line(line))
    try:
        validate_file(parsed_content)
    except ValueError as error:
        print(error)
        exit(1)
    fill_known_undefined_variables(parsed_content)

def check_file(file_path: str) -> bool:
    """
    Verifies if a file exists and can be opened.
    :param file_path: Path to the file to be checked.
    :return: True if the file is accessible, False otherwise.
    """
    try:
        with open(file_path, 'r') as file:
            return True
    except (IOError, FileNotFoundError):
        print(f"Error: Cannot access the file {file_path}.")
        return False
