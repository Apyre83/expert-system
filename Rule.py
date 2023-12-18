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

    def solve(self):
        # print(f"solve() with {self.name}")
        if self.type == "VARIABLE":
            if self.hasBeenSolved:
                return self.value
            else:
                if (id(self) == id(parse.global_dict[self.name])):
                    return self.value

                self.value = parse.global_dict[self.name].solve()
                self.hasBeenSolved = True
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

