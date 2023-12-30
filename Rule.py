import parse
from typing import List, Set

class Node:
    """
    Represents a node in a logical tree, which can be either a variable or an operator.
    Attributes:
        name (str): The name of the node, which is either a logical operator or a variable.
        value (bool): The logical value of the node.
        hasBeenSolved (bool): Indicates whether the node's value has been resolved.
        left (Node): The left child node in the tree.
        right (Node): The right child node in the tree.
        type (str): The type of the node, either 'OPERATOR' or 'VARIABLE'.
        isBeingSolved (bool): Indicates if the node is currently being resolved, used to detect circular references.
    Constants:
        TYPES (Set[str]): A set containing the possible types of nodes - 'OPERATOR' and 'VARIABLE'.
    """
    TYPES: Set[str] = {
            "OPERATOR",
            "VARIABLE"
            }

    def __init__(self, name: str, value: bool = False):
        """
        Initializes a new instance of the Node class.
        Args: name (str): The name of the node.
              value (bool, optional): The initial logical value of the node. Defaults to False.
        """
        self.name = name
        self.value = value
        self.hasBeenSolved = value
        self.left = None
        self.right = None
        self.type = "OPERATOR" if name in "+|^!" else "VARIABLE"
        self.isBeingSolved = False

    def solve(self, explain=False):
        """
        Recursively solves the logical value of the node and its descendants in a logical tree.

        This method is responsible for evaluating the logical value of the node based on its type (either 'OPERATOR' or 'VARIABLE')
        and its children, if any. It uses a recursive approach to traverse the tree structure and compute the logical value.
        If the node is a 'VARIABLE', it checks if its value has already been resolved and returns it. If not, it recursively
        evaluates its value based on the rules associated with the variable.
        If the node is an 'OPERATOR', it evaluates the logical operation based on its operator type and the values of its
        left and right children.

        Args:
            explain (bool, optional): Indicates whether to provide explanations during the solving process. Defaults to False.

        Returns:
            Tuple[bool, List[str]]: A tuple containing the resolved logical value of the node and a list of explanations, if
            'explain' is True.
        """
        explanations = []

        if self.type == "VARIABLE":
            if self.hasBeenSolved:
                if explain:
                    explanations.append(f"Variable '{self.name}' is already solved: {self.value}")
                return self.value, explanations

            if self.isBeingSolved:
                if explain:
                    print(f"We have a circular reference for '{self.name}'. Thus, {self.name}: False")
                return False, explanations

            self.isBeingSolved = True
            result = False
            for node in parse.global_dict[self.name]:
                node_result, node_explanations = node.solve(explain)
                explanations.extend(node_explanations)
                result = result or node_result
            self.value = result
            self.hasBeenSolved = True
            self.isBeingSolved = False
            return self.value, explanations

        # Handling operators
        if self.name in ["+", "|", "^"]:
            if explain:
                operands = [self.left.name if self.left else "", self.right.name if self.right else ""]
                op_explanation = f"Operator '{self.name}'. We are looking to know the value of its operands: {' and '.join(filter(None, operands))}."
                explanations.append(op_explanation)

            left_value, left_explanations = (False, [])
            if self.left:
                left_value, left_explanations = self.left.solve(explain)
                explanations.extend(left_explanations)

            right_value, right_explanations = (False, [])
            if self.right:
                right_value, right_explanations = self.right.solve(explain)
                explanations.extend(right_explanations)

            if self.name == "+":
                self.value = left_value and right_value
            elif self.name == "|":
                self.value = left_value or right_value
            elif self.name == "^":
                self.value = left_value != right_value

            if explain:
                result_explanation = f"Operator '{self.name}' : {left_value} {self.name} {right_value} results in {self.value}"
                explanations.append(result_explanation)

        elif self.name == "!":
            if explain:
                op_explanation = f"Operator '!'. We are looking to know the value of its operand: {self.right.name}."
                explanations.append(op_explanation)

            right_value, right_explanations = self.right.solve(explain) if self.right else (False, [])
            explanations.extend(right_explanations)

            self.value = not right_value
            if explain:
                result_explanation = f"Operator '!' : not {right_value} results in {self.value}"
                explanations.append(result_explanation)

        self.hasBeenSolved = True
        return self.value, explanations

    def __str__(self):
        """
        Returns a string representation of the node, showing its name, value, and resolution status.
        Returns: str: A string representing the node.
        """
        if self.type == "VARIABLE":
            return f"{self.name} ({self.value}, {self.hasBeenSolved})\n"
        else:
            return f".{self.name}.\n"

    def __repr__(self):
        """
        Returns a string representation of the node. This method calls the __str__ method.
        Returns: str: A string representing the node.
        """
        return str(self)

