#!/usr/bin/env python3

from typing import List, Dict, Tuple, Set
import sys
from parse import check_file, parse_file
from parse import queries, known_variables, rules, rpns
import Rule



class Node:

    TYPES: Set[str] = {
            "OPERATOR",
            "VARIABLE"
            }

    def __init__(self, name: str, value: bool = False):
        self.name = name
        self.value = value
        self.hasBeenSolved = value
        self.left = None
        self.right = None
        self.type = "OPERATOR" if name in "+|^!" else "VARIABLE"

    def solve(self):
        #print(f"solve() with {self.name}")
        if self.type == "VARIABLE":
            if self.hasBeenSolved:
                return self.value
            else:
                if (id(self) == id(global_dict[self.name])):
                    return self.value

                self.value = global_dict[self.name].solve()
                self.hasBeenSolved = True
                return self.value

        if self.name == "!":
            self.value = not self.right.solve()
            self.hasBeenSolved = True
            return self.value

        if self.name == "+":
            self.value = self.left.solve() and self.right.solve()
            self.hasBeenSolved = True
            return self.value

        if self.name == "|":
            self.value = self.left.solve() or self.right.solve()
            self.hasBeenSolved = True
            return self.value

        if self.name == "^":
            self.value = self.left.solve() != self.right.solve()
            self.hasBeenSolved = True
            return self.value

    def __str__(self):
        return f"{self.name} (.{self.value}., .{self.hasBeenSolved}.)\n"

    def __repr__(self):
        return str(self)

def construct_tree(rpn_expression):
    tokens = list(rpn_expression)
    stack = []

    for token in tokens:
        if token in global_dict:
            stack.append(Node(token, False)) # False => global_dict[token].solve()
            continue

        if token in "+|^":
            node = Node(token)
            node.right = stack.pop() if stack else None
            node.left = stack.pop() if stack else None
        elif token == "!":
            node = Node(token)
            node.right = stack.pop() if stack else None
        else:
            node = Node(token)  # Créer un nœud avec le nom du token

        global_dict[node.name] = node  # Stocker le nœud dans le dictionnaire global
        stack.append(node)

    return stack.pop()

def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        status = "Resolved" if node.hasBeenSolved else "Unresolved"
        print(' ' * 4 * level + f'-> {node.name} ({node.value}, {status})')
        print_tree(node.left, level + 1)

def extract_variable_fron_RPN(rpn_expression: str) -> Tuple[str, str]:
    variable: str = rpn_expression[-3]
    rpn_expression = rpn_expression[:-3]
    return variable, rpn_expression

global_dict: Dict[str, Node] = {}

#rpn_expressions = ["AB+C=>", "DE|F=>", "FF^G=>"]
#for rpn_expression in rpn_expressions:
#    variable, rpn_expression = extract_variable_fron_RPN(rpn_expression)
#    global_dict[variable] = construct_tree(rpn_expression)
#    print("variable: ", variable)
#    print_tree(global_dict[variable])
#    print("-------------------------------")

def main():
    """
    Main function to run the program.
    Checks for the correct number of arguments, validates the file, and processes it.
    """
    if (len(sys.argv) != 2):
        print("Error: Invalid number of arguments.")
        print("Usage: python3 main.py [input_file_path]")
        return
    file_path = sys.argv[1]
    check_file(file_path)
    parse_file(file_path)

    # Debug :
    print("-----------------------------------")
    print("Rules (RPN format):")
    for rule in rules:
        print(rule)
    print("-----------------------------------")
    print("Queries:")
    for query in queries:
        print(query)
    print("-----------------------------------")
    print("Known variables:")
    for key, value in known_variables.items():
        print(f"{key}: {value}")
    print("-----------------------------------")

    for variable in known_variables:
        global_dict[variable] = Node(variable, known_variables[variable].value)

    for tmp_rpn in rpns:
        variable, rpn = extract_variable_fron_RPN(tmp_rpn)
        print(f"var: {variable} rpn: {rpn}")
        global_dict[variable] = construct_tree(rpn)
        print_tree(global_dict[variable])
        print("-------------------------------")

    for query in queries:
        if query in global_dict:
            print(f"{query}: {global_dict[query].solve()}")
        else:
            print(f"{query}: False")

if __name__ == "__main__":
    main()
    pass
