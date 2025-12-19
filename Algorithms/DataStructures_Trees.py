from collections import deque
from typing import Generator, Optional
from DataStructures_Nodes import TreeNode


class BinaryTree:
    """Simple binary search tree (BST) wrapper around `TreeNode`.

    - Not balanced. Uses Python value ordering for comparisons.
    - Methods: insert, find, inorder/preorder/postorder generators, to_list.
    - `from_root` classmethod builds a BinaryTree view from an existing
      `TreeNode` root and computes `.size` while protecting against cycles.
    """

    def __init__(self, iterable=None):
        self.root: Optional[TreeNode] = None
        self.size = 0
        if iterable:
            for v in iterable:
                self.insert(v)

    def insert(self, value):
        """Insert value into the BST.

        If the tree is empty, sets root. Otherwise inserts as a leaf.
        """
        new_node = TreeNode(value)
        if self.root is None:
            self.root = new_node
            self.size = 1
            return new_node

        curr = self.root
        while True:
            # Use payload comparison; allow TreeNode wrappers in comparison.
            curr_val = curr.payload
            if value < curr_val:
                left = curr.Left()
                if left is None:
                    curr.Left(new_node)
                    new_node.Parent(curr)
                    self.size += 1
                    return new_node
                curr = left
            else:
                right = curr.Right()
                if right is None:
                    curr.Right(new_node)
                    new_node.Parent(curr)
                    self.size += 1
                    return new_node
                curr = right

    def find(self, value) -> Optional[TreeNode]:
        """Find node by value using BST property; return the node or None."""
        curr = self.root
        while curr is not None:
            if value == curr.payload:
                return curr
            if value < curr.payload:
                curr = curr.Left()
            else:
                curr = curr.Right()
        return None

    def inorder(self, node: Optional[TreeNode] = None, _seen=None) -> Generator:
        if node is None:
            node = self.root
        if node is None:
            return
        if _seen is None:
            _seen = set()
        nid = id(node)
        if nid in _seen:
            return
        _seen.add(nid)
        left = node.Left()
        if left is not None:
            yield from self.inorder(left, _seen)
        yield node.payload
        right = node.Right()
        if right is not None:
            yield from self.inorder(right, _seen)

    def preorder(self, node: Optional[TreeNode] = None, _seen=None) -> Generator:
        if node is None:
            node = self.root
        if node is None:
            return
        if _seen is None:
            _seen = set()
        nid = id(node)
        if nid in _seen:
            return
        _seen.add(nid)
        yield node.payload
        left = node.Left()
        if left is not None:
            yield from self.preorder(left, _seen)
        right = node.Right()
        if right is not None:
            yield from self.preorder(right, _seen)

    def postorder(self, node: Optional[TreeNode] = None, _seen=None) -> Generator:
        if node is None:
            node = self.root
        if node is None:
            return
        if _seen is None:
            _seen = set()
        nid = id(node)
        if nid in _seen:
            return
        _seen.add(nid)
        left = node.Left()
        if left is not None:
            yield from self.postorder(left, _seen)
        right = node.Right()
        if right is not None:
            yield from self.postorder(right, _seen)
        yield node.payload

    def inorder_list(self):
        return list(self.inorder())

    def preorder_list(self):
        return list(self.preorder())

    def postorder_list(self):
        return list(self.postorder())

    def __str__(self):
        return "Inorder: " + " -> ".join(str(x) for x in self.inorder()) + " -> None"
    
    def printTree(self):
        if self.root is not None:
            self.root.printTree()
        else:
            print("<empty tree>")

    @classmethod
    def from_root(cls, root_node: Optional[TreeNode]):
        """Build a BinaryTree view from an existing `TreeNode` root.

        Traverses the tree breadth-first, counts unique nodes, and sets
        parent pointers for any children encountered.
        Protects against cycles by tracking visited node ids.
        """
        inst = cls()
        inst.root = root_node
        if root_node is None:
            inst.size = 0
            return inst

        q = deque([root_node])
        seen = set()
        count = 0
        while q:
            node = q.popleft()
            nid = id(node)
            if nid in seen:
                continue
            seen.add(nid)
            count += 1
            left = node.Left()
            if left is not None:
                left.Parent(node)
                q.append(left)
            right = node.Right()
            if right is not None:
                right.Parent(node)
                q.append(right)

        inst.size = count
        return inst

class AVLTree(BinaryTree):
    """Placeholder for future AVL tree implementation."""
    pass


if __name__ == "__main__":
    # Quick demo
    t = BinaryTree()
    t.insert(5)
    t.insert(3)
    t.insert(7)
    t.insert(1)
    t.insert(4)
    print(t)
    print("Preorder:", t.preorder_list())
    print("Postorder:", t.postorder_list())