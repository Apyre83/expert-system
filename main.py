#!/usr/bin/env python3

from typing import Tuple
from parse import check_file, parse_file, read_file
from parse import queries, global_dict
from interactive import interactive_mode
import argparse

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

def main():
    """
    The main function to run the expert system program. It starts by parsing arguments for the input file
    and the interactive mode. If an input file is provided, it reads and processes the file. If the interactive
    mode is specified, it enters an interactive session where the user can manipulate the parsed content.
    After processing the input file or the content from the interactive session, the program evaluates the
    logical queries and prints the results.
    The function first checks if the input file is provided. If not, it displays the help message. Then, it
    reads and processes the input file. If interactive mode is selected, it goes into an interactive session
    allowing the user to view, add, edit, remove, or execute parsed content. Finally, it evaluates the logical
    queries and prints the results to the console.
    The program requires either an input file path
    to run properly.
    """
    parser = argparse.ArgumentParser(
        description="This program analyzes and solves logical problems.")
    parser.add_argument("input_file", nargs='?',
                        help="Path to input file", default=None)
    parser.add_argument(
        "--interactive", help="Start in interactive mode", action="store_true")
    args = parser.parse_args()
    if args.input_file is None:
        parser.print_help()
        return
    check_file(args.input_file)
    parsed_content = read_file(args.input_file)

    if args.interactive:
        parsed_content = interactive_mode(parsed_content)
    parse_file(parsed_content)
    for query in queries:
        if query in global_dict:
            result = False
            for node in global_dict[query]:
                node_result = node.solve()
                result = result or node_result
                if (result):
                    break
            print(f"{query}: {result}")
        else:
            print(f"{query}: False")

    # print(f"final global_dict:\n{global_dict}")

if __name__ == "__main__":
    main()
    pass

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
    #    if variable in "!+^|":
    #        continue
    #    print(variable)
    #    for rule in global_dict[variable]:
    #        print_tree(rule)
    #        print()
    #    print("-------------------------------")

    # print(global_dict)

    # print("----------   SOLVING   ----------")
