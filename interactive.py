import os

def add_content(parsed_content):
    """
    Adds new content (rule, fact, or query) to the parsed content.
    The function allows the user to select the type of content to add and then enter the details for it.
    If the user chooses to cancel, the function returns without making any changes.
    Args:    parsed_content (list): The current list of parsed content, which may include rules, facts, and queries.
    Returns: None: The function directly modifies the parsed_content list and does not return a value.
    """
    clear_terminal()
    print("Expert System Interactive Mode")
    print("\nAdd Content")
    print("\nTypes: [1] Rule [2] Fact [3] Query [0] Cancel")
    type_choice = input("Choose the type of content to add: ")
    if type_choice == "0":
        return
    elif type_choice == "1":
        rules = [item for item in parsed_content if item[0] == 'rule']
        if rules:
            print("Actual Rules:")
            for rule in rules:
                print(f" {rule[1]}")
        new_rule = input("Enter the new rule: ")
        parsed_content.append(('rule', new_rule))
    elif type_choice == "2":
        facts = [item for item in parsed_content if item[0] == 'fact']
        if facts:
            print("Actual Facts:")
            for fact in facts:
                print(f" {fact[1]}")
        new_fact = input("Enter the new fact: ")
        parsed_content.append(('fact', new_fact))
    elif type_choice == "3":
        queries = [item for item in parsed_content if item[0] == 'query']
        if queries:
            print("Actual Queries:")
            for query in queries:
                print(f" {query[1]}")
        new_query = input("Enter the new query: ")
        parsed_content.append(('query', new_query))
    else:
        print("Invalid choice. Please try again.")

def display_content(parsed_content, should_wait=True):
    """
    Displays the parsed content in a formatted manner, with each item (rule, fact, query) numbered sequentially.
    The function optionally waits for the user to press enter before returning, based on the should_wait parameter.
    Args:    parsed_content (list): The list of parsed content to display.
             should_wait (bool, optional): If True, the function waits for user input before returning. Defaults to True.
    Returns: None
    """
    counter = 1
    clear_terminal()
    rules = [item for item in parsed_content if item[0] == 'rule']
    if rules:
        print("Rules:")
        for rule in rules:
            print(f"  {counter}: {rule[1]}")
            counter += 1
        print()

    facts = [item for item in parsed_content if item[0] == 'fact']
    if facts:
        print("Facts:")
        for fact in facts:
            print(f"  {counter}: {fact[1]}")
            counter += 1
        print()

    queries = [item for item in parsed_content if item[0] == 'query']
    if queries:
        print("Queries:")
        for query in queries:
            print(f"  {counter}: {query[1]}")
            counter += 1
        print()

    if should_wait:
        input("Press enter to continue...")

def remove_content(parsed_content):
    """
    Removes an item from the parsed content. The function displays the current content and prompts the user to choose
    an item number to remove. If the chosen number is valid, the corresponding item is removed from the list.
    Args:    parsed_content (list): The list of parsed content from which an item will be removed.
    Returns: None: The function directly modifies the parsed_content list and does not return a value.
    """
    display_content(parsed_content, False)
    try:
        choice = int(input("\nChoose the item number to delete: ")) - 1
        if 0 <= choice < len(parsed_content):
            del parsed_content[choice]
            print("Item deleted successfully.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def edit_content(parsed_content):
    """
    Edits an existing item in the parsed content. The function displays the current content and prompts the user
    to choose an item number to edit. The user then enters the new content for the selected item.
    Args:    parsed_content (list): The list of parsed content where an item will be edited.
    Returns: None: The function directly modifies the parsed_content list and does not return a value.
    """
    display_content(parsed_content, False)
    try:
        choice = int(input("\nChoose the item number to edit: ")) - 1
        if 0 <= choice < len(parsed_content):
            new_content = input(f"Enter the new content (current : {parsed_content[choice][1]}) : ")
            parsed_content[choice] = (parsed_content[choice][0], new_content)
            print("Item edited successfully.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

def remove_empty_lines(parsed_content):
    """
    Filters out any 'empty' items from the parsed content. The function creates and returns a new list that
    includes all items except those marked as 'empty'.
    Args:    parsed_content (list): The list of parsed content to be filtered.
    Returns: list: A new list containing all items from parsed_content except those marked as 'empty'.
    """
    return [item for item in parsed_content if item[0] != "empty"]

def clear_terminal():
    """
    Clears the terminal screen.
    Args:    None
    Returns: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def interactive_mode(parsed_content):
    """
    Initiates an interactive mode for the expert system. In this mode, the user can view, add, edit, remove, or execute
    parsed content, and exit the program. The function continuously prompts the user to choose an option until they decide to exit.
    Args:    parsed_content (list): The list of parsed content that can be manipulated in the interactive mode.
    Returns: None or list: Returns the modified parsed_content if the user chooses to execute, otherwise does not return a value.
    """
    parsed_content = remove_empty_lines(parsed_content)
    while True:
        clear_terminal()
        print("Expert System Interactive Mode")
        print("\nOptions:\n\t[1] Show\n\t[2] Add\n\t[3] Edit\n\t[4] Remove\n\t[5] Execute\n\t[6] Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            display_content(parsed_content)
        elif choice == "2":
            add_content(parsed_content)
        elif choice == "3":
            edit_content(parsed_content)
        elif choice == "4":
            remove_content(parsed_content)
        elif choice == "5":
            clear_terminal()
            print("Expert System Results:")
            return parsed_content
        elif choice == "6":
            exit(0)
        else:
            print("Invalid choice. Please try again.")
