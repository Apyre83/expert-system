# Expert System

The Expert System is a Python program designed for analyzing and solving logical problems. It reads rules, facts, and queries from a specific file format and evaluates these elements to draw logical conclusions. The program also offers an interactive mode where users can add, edit, remove, or execute parsed content directly from the command line.

----

## Installation

To use the Expert System, Python must be installed on your machine.

1. Clone the repository:
````
git clone https://github.com/jmbertin/expert-system.git
````

2. Navigate to the project directory:
````
cd expert-system
````

----

## Usage
To run the program, use the following command in the project directory:

````
python3 main.py path_to_input_file.txt
````

To start in interactive mode, use:
````
python3 main.py path_to_input_file.txt --interactive
````

### Interactive Mode
In interactive mode, you have the following options:

- **Show:** Displays the currently loaded rules, facts, and queries.
- **Add:** Add new rules, facts, or queries.
- **Edit:** Modify existing elements.
- **Remove:** Remove existing elements.
- **Execute:** Execute the expert system with the current content.
- **Exit:** Exit the interactive mode.

----

## Automated Testing
The Expert System includes an automated testing script test_script.sh that you can use to run various tests on the system. The script is designed to run error cases, optional cases, mandatory cases, or all cases, depending on the option you choose.

### Usage
To run the test script, use one of the following commands in your terminal:

````
./test_script.sh errors     # To run error tests
./test_script.sh optional   # To run optional tests
./test_script.sh mandatory  # To run mandatory tests
./test_script.sh all        # To run all tests
````

----

## Methodology

### Parsing and Processing
- **File Parsing**: The system reads and parses input files, converting rules into Reverse Polish Notation (RPN) for easier processing.
- **Tree Construction**: Logical rules are transformed into a tree structure, enabling complex logical operations.
- **Dynamic Evaluation**: Variables are evaluated dynamically, with the ability to resolve circular references and contradictory rules.

### Components
- **Node**: Represents the basic element of the logical tree, capable of being an operator or a variable.
- **Global Dictionary**: Maintains mappings of variables to their corresponding nodes in the logic tree.

----

**Authors are:**
- [Apyre / Leo Fresnay](https://github.com/Apyre83)
- [Jean-michel Bertin](https://github.com/jmbertin)
