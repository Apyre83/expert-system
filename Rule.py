import parse
from typing import List, Set
class Node:

    TYPES: Set[str] = {
            "OPERATOR",
            "VARIABLE"
            }

    def __init__(self, name: str, value: bool = False):
        self.name = name
        self.value = value
        self.hasBeenSolved = value
        self.left = None
        self.right = None
        self.type = "OPERATOR" if name in "+|^!" else "VARIABLE"
        self.isBeingSolved = False

    def solve(self):
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
        if self.type == "VARIABLE":
            return f"{self.name} ({self.value}, {self.hasBeenSolved})\n"
        else:
            return f".{self.name}.\n"

    def __repr__(self):
        return str(self)

