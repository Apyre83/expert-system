from typing import List, Dict, Tuple
import sys
from parse import check_file, parse_file
from parse import queries, known_variables, rules
import Rule


def solve(query: str) -> None:
    """
    Solves the query and prints the result.
    """

    # Check if query is already known
    if query in known_variables and known_variables[query] == True:
        print(f"{query} = True")
        return

    for rule in rules:
        if query in rule.output_variables:
            val = rule.solve()
            if (val != Rule.Rule.UNDEFINED):
                print(f"{query} = {known_variables[query]}")
                return

    print(f"Could not solve {query} with {known_variables}")

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


    # Solve queries
    for query in queries:
        solve(query)

if __name__ == "__main__":
    main()
