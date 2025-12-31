from typing import List


class TreeNode:
    def __init__(self, value):
        self.parent = None
        self.left = None
        self.right = None
        self.value = value

    def __str__(self):
        return f'P: {self.parent.value if self.parent else None} | {self.left.value if self.left else None} <- ({self.value}) -> {self.right.value if self.right else None} R: {True if self.parent is None else False}'

class SigmaTree:
    def __init__(self, root_value):
        self.root = TreeNode(root_value)

    def print_tree(self):
        def _print(node, prefix="", is_left=True):
            if node is None:
                return

            # najpierw prawa gałąź (żeby była "na górze")
            if node.right is not None:
                _print(node.right, prefix + ("│   " if is_left else "    "), False)

            # aktualny węzeł
            connector = "└── " if is_left else "┌── "
            print(prefix + connector + str(node.value))

            # potem lewa gałąź (na dole)
            if node.left is not None:
                _print(node.left, prefix + ("    " if is_left else "│   "), True)

        _print(self.root)

    def add_node(self, node: TreeNode):
        root = self.root
        self.add(root, node)
        self.search(root)

    def add(self, parent: TreeNode, node: TreeNode):
        left = parent.left
        right = parent.right

        if left is None and right is None:
            if node.value <= parent.value:
                parent.left = node
                node.parent = parent
            else:
                parent.right = node
                node.parent = parent
        elif left is None and right is not None:
            if node.value <= parent.value:
                parent.left = node
                node.parent = parent
            else:
                self.add(right, node)
        elif left is not None and right is None:
            if node.value <= parent.value:
                self.add(left, node)
            else:
                parent.right = node
                node.parent = parent
        else:
            if node.value <= parent.value:
                self.add(left, node)
            else:
                self.add(right, node)


    def add_range(self, values: List[TreeNode]):
        for node in values:
            self.add_node(node)

    def get_paths(self):
        root = self.root
        return self.search(root)

    def search(self, node: TreeNode) -> int:
        val = 0
        if node is None:
            return val
        if node.parent is None:
            return self.search(node.left) + self.search(node.right)
        if node.value > node.parent.value:
            val += 1
        val += self.search(node.left) + self.search(node.right)
        return val
