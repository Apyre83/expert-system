from typing import Tuple
import re
import Rule

# global_dict est désormais un dictionnaire de listes de Node
global_dict = {}  # Key: variable, Value: List[Rule.Node]

# Queries declared variable in files
queries = set()

# List of rules
rules = []

def pre_process_rpn(rpn_expression):
    tokens = list(rpn_expression)
    processed_tokens = []
    skip_next = False

    for i, token in enumerate(tokens):
        if skip_next:
            skip_next = False
            continue

        if token == "!":
            if i + 1 < len(tokens):
                processed_tokens.append(tokens[i + 1])
                processed_tokens.append(token)
                skip_next = True
            else:
                raise ValueError("Expression RPN invalide: '!' à la fin de l'expression")
        else:
            processed_tokens.append(token)

    return ''.join(processed_tokens)

def construct_tree(rpn_expression):
    pre_rpn = pre_process_rpn(rpn_expression)
    tokens = list(pre_rpn)
    stack = []

    for token in tokens:
        if token in global_dict and token not in "+|^":
            # Si le token est déjà dans global_dict et n'est pas un opérateur, ajoutez-le au stack
            stack.append(Rule.Node(token, False))  # False => global_dict[token].solve()
            continue

        if token in "+|^":
            node = Rule.Node(token)
            node.right = stack.pop() if stack else None
            node.left = stack.pop() if stack else None
        elif token == "!":
            node = Rule.Node(token)
            node.right = stack.pop() if stack else None
        else:
            node = Rule.Node(token)  # Créer un nœud avec le nom du token

        # Ajouter le nœud à la liste correspondante dans global_dict
        if node.name not in global_dict:
            global_dict[node.name] = []  # Initialiser avec une liste vide si non existant
        global_dict[node.name].append(node)  # Ajouter le Node à la liste

        stack.append(node)

    return stack.pop() if stack else None

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
    precedence = {'!': 4, '+': 3, '|': 2, '^': 1, '(': 0, ')': 0}
    output = []
    stack = []

    i = 0
    while i < len(expression):
        char = expression[i]

        if char.isalpha() and char.isupper():
            output.append(char)
        elif char == '!':
            # Gérer le '!' comme opérateur unaire
            if i + 1 < len(expression) and expression[i + 1].isalpha() and expression[i + 1].isupper():
                output.append(char + expression[i + 1])
                i += 1  # Passer le caractère suivant (la variable après '!')
            else:
                return "Error: operator mismatch"
        elif char in ['+', '|', '^']:
            while stack and precedence[stack[-1]] >= precedence[char]:
                output.append(stack.pop())
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
            else:
                return "Error: parenthesis mismatch"
        else:
            return "Error: invalid character"

        i += 1

    while stack:
        if stack[-1] == '(':
            return "Error: parenthesis mismatch"
        output.append(stack.pop())

    return ''.join(output)




def fill_known_undefined_variables(parsed_content):
    """
    Fills the global_dict dictionary with undefined variables found in rules, setting their value to -1 (undefined).
    :param parsed_content: Parsed content containing types and contents including rules.
    """
    for line_type, content in parsed_content:
        if line_type == "rule":
            for char in content:
                if char.isupper() and char not in global_dict:
                    global_dict[char] = [Rule.Node(char, False)]


def divide_rule(left_side: str, right_side: str, relation: str) -> dict:
    """
    Divides a rule with a '+' operator into multiple rules, handling negations.
    :param left_side: The left side of the rule.
    :param right_side: The right side of the rule.
    :param relation: The relation of the rule.
    :return: A list of rules.
    """
    divided_rules = {}
    variables = re.findall(r'(!?[A-Z])', right_side)
    for variable in variables:
        divided_rules[variable] = construct_tree(left_side)
    return divided_rules

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
    if re.search(r'[|^]', right_side):
        raise ValueError(f"Error: Right side of rule must not contain any operator ({rule}).")

    if not is_valid_rpn(left_side) or not is_valid_rpn(right_side):
        raise ValueError(f"Error: Rule is not valid ({rule}).")


    if '+' in right_side:
        divided_rules = divide_rule(left_side, right_side, relation)
        for key, value in divided_rules.items():
            if key not in global_dict:
                global_dict[key] = []
            global_dict[key].append(value)
    else:
        if right_side not in global_dict:
            global_dict[right_side] = []
        global_dict[right_side].append(construct_tree(left_side))

    return True

def check_facts_in_rules(parsed_content):
    """
    Checks if all facts are present in at least one rule.
    :param parsed_content: Parsed content containing types and contents including rules.
    """
    facts = set()
    rules = []
    for line_type, content in parsed_content:
        if line_type == "fact":
            facts.update(content)
        elif line_type == "rule":
            rules.append(content)
    for fact in facts:
        if not any(fact in rule for rule in rules):
            print(f"Warning: Fact '{fact}' is not present in any rule.")

def validate_file(parsed_content):
    """
    Validates the contents of a parsed file, including rules, facts, and queries.
    :param parsed_content: The parsed content of the file.
    :raises ValueError: If any part of the file content is invalid.
    """
    has_rule, has_fact, has_query = False, False, False

    check_facts_in_rules(parsed_content)

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
                if fact not in global_dict or not any(node.value for node in global_dict[fact]):
                    # Ajouter le fait seulement s'il n'est pas déjà présent ou s'il n'est pas résolu
                    global_dict[fact] = [Rule.Node(fact, True)]


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
