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

    def solve(self):
        """
        Resolves the logical value of the node. For variables, it resolves their value based on the logical tree.
        For operators, it computes the logical operation based on the values of child nodes.
        Returns: bool: The resolved logical value of the node.
        Note:    The method uses recursion to resolve values and employs mechanisms to handle circular references.
        """
        if self.type == "VARIABLE":
            if self.hasBeenSolved:
                return self.value
            if self.isBeingSolved:
                return False

            self.isBeingSolved = True
            result = False
            for node in parse.global_dict[self.name]:
                node_result = node.solve()
                result = result or node_result
            self.value = result
            self.hasBeenSolved = True
            self.isBeingSolved = False
            return self.value


        if self.name in ["+", "|", "^"]:
            left_value = self.left.solve() if self.left is not None else False
            right_value = self.right.solve() if self.right is not None else False

            if self.name == "+":
                self.value = left_value and right_value
            elif self.name == "|":
                self.value = left_value or right_value
            elif self.name == "^":
                self.value = left_value != right_value

        elif self.name == "!":
            right_value = self.right.solve() if self.right is not None else False
            self.value = not right_value

        self.hasBeenSolved = True
        return self.value

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

