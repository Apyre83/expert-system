#!/usr/bin/env python3

from typing import List, Dict, Tuple, Set
import sys
from parse import check_file, parse_file
from parse import queries, rules, global_dict
import Rule

def print_tree(node, level=0):
    """
    Recursively prints the tree structure of logical rules starting from a given node.
    The function traverses the tree in a post-order fashion, first visiting the right child,
    then the current node, and finally the left child. Each node is printed with its name,
    value, and resolution status. The output is indented to reflect the depth of each node
    in the tree.
    Args:    node: The starting node of the tree (or subtree) to be printed.
             level: The initial level of depth in the tree, used for indentation. Defaults to 0.
    Returns: None
    """
    if node is not None:
        print_tree(node.right, level + 1)
        status = "Resolved" if node.hasBeenSolved else "Unresolved"
        print(' ' * 4 * level + f'-> {node.name} ({node.value}, {status})')
        print_tree(node.left, level + 1)

def extract_variable_fron_RPN(rpn_expression: str) -> Tuple[str, str]:
    """
    Extracts the variable and the remaining RPN expression from a given RPN string.
    This function is specifically designed to work with RPN expressions that end
    with a variable followed by its operator. It separates the last three characters
    (assumed to be the variable and its operator) from the rest of the expression.
    Args:    rpn_expression: A string representing the RPN expression.
    Returns: A tuple containing the extracted variable and the modified RPN expression.
    """
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
    # print("-----------------------------------")
    # print("Rules (RPN format):")
    # for rule in rules:
    #     print(rule)
    # print("-----------------------------------")
    # print("Queries:")
    # for query in queries:
    #     print(query)
    # print("-----------------------------------")
    # print("Known variables:")
    # for variable in global_dict:
    #     print(variable)
    # print("-----------------------------------")

    # for variable in global_dict:
    #     print(variable)
    #     print_tree(global_dict[variable])
    #     print("-------------------------------")

    # print(global_dict)

    # print("----------   SOLVING   ----------")

    for query in queries:
        if query in global_dict:
            print(f"{query}: {global_dict[query].solve()}")
        else:
            print(f"{query}: False")

if __name__ == "__main__":
    main()
    pass
