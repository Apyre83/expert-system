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
        explanations = []

        if self.type == "VARIABLE":
            if self.hasBeenSolved:
                if explain:
                    explanations.append(f"Variable '{self.name}' déjà résolue : {self.value}")
                return self.value, explanations

            if self.isBeingSolved:
                if explain:
                    print(f"Nous n'avons pas de valeur a calculer pour '{self.name}'. Ainsi, {self.name}: False")
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
                op_explanation = f"Opérateur '{self.name}'. Nous cherchons à connaître la valeur de ses opérandes: {' et '.join(filter(None, operands))}."
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
                result_explanation = f"Opérateur '{self.name}' : {' et '.join(filter(None, [str(left_value), str(right_value)]))} résulte en {self.value}"
                explanations.append(result_explanation)

        elif self.name == "!":
            if explain:
                op_explanation = f"Opérateur '!'. Nous cherchons à connaître la valeur de son opérande: {self.right.name}."
                explanations.append(op_explanation)

            right_value, right_explanations = self.right.solve(explain) if self.right else (False, [])
            explanations.extend(right_explanations)

            self.value = not right_value
            if explain:
                result_explanation = f"Opérateur '!' : not {right_value} résulte en {self.value}"
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

