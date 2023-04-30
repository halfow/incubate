"""
Generate a Tree
"""
from pathlib import Path

from rich.tree import Tree


def walk(root, depth: int = 9):
    """
    Walk a directory and generate a Tree
    """
    tree = Tree(f"📂 {root}")
    stack = [(Path(root), tree)]
    while stack:
        path, node = stack.pop()

        if len(path.parts) >= depth:
            continue

        for child in path.iterdir():
            if child.is_dir():
                stack.append((child, node.add(f"📁 {child.name}")))
            else:
                node.add(f"📄[blue] {child.name}")

    return tree


if __name__ == "__main__":
    from rich import print

    tree = walk(".", depth=2)
    print(tree)
