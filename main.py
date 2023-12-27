#!/usr/bin/env python3

from typing import Tuple
from parse import check_file, parse_file, read_file
from parse import queries, global_dict
from interactive import interactive_mode
import argparse
from graphviz import Digraph



explain: bool = False

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


def draw_binary_tree(node, query, graph, is_root=True, added_nodes=set()):
    if graph is None:
        graph = Digraph()

    if is_root and node is not None:
        query_node_id = f"query_{query}"
        graph.node(query_node_id, label=f"Requête: {query}", shape="rectangle")
        added_nodes.add(query_node_id)

    if node is not None:
        node_id = f"{node.name}_{id(node)}"

        if node_id not in added_nodes:
            graph.node(node_id, label=f"{node.name}")
            added_nodes.add(node_id)

        if is_root:
            graph.edge(query_node_id, node_id)

        if node.left:
            left_id = f"{node.left.name}_{id(node.left)}"
            if left_id not in added_nodes:
                graph.node(left_id, label=f"{node.left.name}")
                added_nodes.add(left_id)
            graph.edge(node_id, left_id)
            draw_binary_tree(node.left, query, graph, is_root=False, added_nodes=added_nodes)

        if node.right:
            right_id = f"{node.right.name}_{id(node.right)}"
            if right_id not in added_nodes:
                graph.node(right_id, label=f"{node.right.name}")
                added_nodes.add(right_id)
            graph.edge(node_id, right_id)
            draw_binary_tree(node.right, query, graph, is_root=False, added_nodes=added_nodes)

    return graph


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
    parser.add_argument("--explain", help="Explain the reasoning", action="store_true", default=False)
    parser.add_argument("--graph", help="Draw the graph", action="store_true", default=False)
    args = parser.parse_args()
    if args.input_file is None:
        parser.print_help()
        return

    explain = args.explain

    check_file(args.input_file)
    parsed_content = read_file(args.input_file)

    if args.interactive:
        parsed_content = interactive_mode(parsed_content)




    parse_file(parsed_content)

    if args.graph:
        # Créer un seul graphique pour tous les arbres
        master_graph = Digraph()

        for variable in global_dict:
            if variable in "!+^|":
                continue
            for rule in global_dict[variable]:
                draw_binary_tree(rule, f"{variable}", master_graph)

        master_graph.render("master_graph", view=True)


    for query in queries:
        if explain:
            print(f"Essai de résolution de '{query}':")
        if query in global_dict:

            result = False
            all_explanations = []
            for node in global_dict[query]:
                node_result, explanations = node.solve(explain=explain)
                all_explanations.extend(explanations)
                result = result or node_result
                if result:
                    break
            if explain:
                for explanation in all_explanations:
                    print(explanation)
            print(f"{query}: {result}")
        else:
            if explain:
                print(f"{query}: False (pas de règle trouvée)")
            else:
                print(f"Il n'y a pas de règle pour '{query}'. Par conséquent, {query}: False")


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


    # print(global_dict)

    # print("----------   SOLVING   ----------")
