#!/usr/bin/env python3

from typing import List, Dict, Tuple, Set
import sys
from parse import check_file, parse_file
from parse import queries, rules, rpns, global_dict
import Rule




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
    #for key, value in known_variables.items():
    #    print(f"{key}: {value}")
    print("-----------------------------------")

    #for variable in known_variables:
    #    global_dict[variable] = Node(variable, known_variables[variable].value)

    for variable in global_dict:
        print(variable)
        print_tree(global_dict[variable])
        print("-------------------------------")

    print(global_dict)

    print("----------   SOLVING   ----------")

    for query in queries:
        if query in global_dict:
            print(f"{query}: {global_dict[query].solve()}")
        else:
            print(f"{query}: False")

if __name__ == "__main__":
    main()
    pass
