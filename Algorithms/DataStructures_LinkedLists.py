from DataStructures_Nodes import SingleLinkedListNode, DoublyLinkedListNode


class LinkedList:
    def __init__(self, iterable=None):
        """Simple singly-linked list implementation.

        - Indexing and insertion/deletion operations are 1-based where noted.
        - Methods: insert_at_head, insert_at_tail, insert_at(index),
          delete_at_head, delete_at_tail, delete_at(index), delete_value(value)
        """
        self.head = None
        self.tail = None
        self.size = 0
        if iterable:
            for item in iterable:
                self.insert_at_tail(item)

    def __len__(self):
        return self.size

    def __iter__(self):
        node = self.head
        while node:
            yield node.payload
            node = node.Next()

    def __str__(self):
        return self.head.strChain() if self.head else "None"

    # Insertions
    def insert_at_head(self, value):
        new_node = SingleLinkedListNode(value)
        new_node.Next(self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1

    def insert_at_tail(self, value):
        new_node = SingleLinkedListNode(value)
        if self.tail:
            self.tail.Next(new_node)
        else:
            self.head = new_node
        self.tail = new_node
        self.size += 1

    def insert_at(self, index, value):
        """Insert value at 1-based index. index==1 inserts at head; index==size+1 appends."""
        if index < 1 or index > self.size + 1:
            raise IndexError("Index out of bounds")
        if index == 1:
            return self.insert_at_head(value)
        if index == self.size + 1:
            return self.insert_at_tail(value)

        new_node = SingleLinkedListNode(value)
        prev = self.head
        for _ in range(1, index - 1):
            prev = prev.Next()
        new_node.Next(prev.Next())
        prev.Next(new_node)
        self.size += 1

    # Deletions
    def delete_at_head(self):
        if not self.head:
            raise IndexError("Delete from empty list")
        self.head = self.head.Next()
        if not self.head:
            self.tail = None
        self.size -= 1

    def delete_at_tail(self):
        if self.size == 0:
            raise IndexError("Delete from empty list")
        if self.size == 1:
            self.head = None
            self.tail = None
            self.size = 0
            return
        prev = self.head
        while prev.Next() is not self.tail:
            prev = prev.Next()
        prev.Next(None)
        self.tail = prev
        self.size -= 1

    def delete_at(self, index):
        if index < 1 or index > self.size:
            raise IndexError("Index out of bounds")
        if index == 1:
            return self.delete_at_head()
        prev = self.head
        for _ in range(1, index - 1):
            prev = prev.Next()
        to_delete = prev.Next()
        prev.Next(to_delete.Next())
        if to_delete is self.tail:
            self.tail = prev
        self.size -= 1

    def delete_value(self, value):
        """Delete the first node that equals value. Returns True if deleted."""
        prev = None
        node = self.head
        idx = 1
        while node:
            if node.payload == value:
                if prev is None:
                    self.delete_at_head()
                else:
                    prev.Next(node.Next())
                    if node is self.tail:
                        self.tail = prev
                    self.size -= 1
                return True
            prev = node
            node = node.Next()
            idx += 1
        return False

    @classmethod
    def from_head(cls, head_node):
        """Construct a LinkedList view from an existing head node.

        - Traverses nodes using `Next()` to determine `tail` and `size`.
        - Handles cycles: counts each unique node once and sets `tail`
          to the last unique node before the cycle repeats (or None if empty).
        """
        inst = cls()
        inst.head = head_node
        if head_node is None:
            inst.tail = None
            inst.size = 0
            return inst

        seen = {}
        node = head_node
        prev = None
        while node is not None:
            nid = id(node)
            if nid in seen:
                # cycle detected; prev is last unique node
                inst.tail = prev
                inst.size = len(seen)
                return inst
            seen[nid] = node
            prev = node
            node = node.Next()

        # reached end (no cycle)
        inst.tail = prev
        inst.size = len(seen)
        return inst


class DoublyLinkedList:
    """Doubly-linked list using `DoublyLinkedListNode`.

    API mirrors `LinkedList`: `insert_at_head`, `insert_at_tail`, `insert_at`,
    `delete_at_head`, `delete_at_tail`, `delete_at`, `delete_value`, iteration
    and `__str__` (with loop detection).
    """
    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self.size = 0
        if iterable:
            for item in iterable:
                self.insert_at_tail(item)

    def __len__(self):
        return self.size

    def __iter__(self):
        node = self.head
        while node:
            yield node.payload
            node = node.Next()

    def __str__(self):
        return self.head.strChain() if self.head else "None"

    # Insertions
    def insert_at_head(self, value):
        new_node = DoublyLinkedListNode(value)
        new_node.Next(self.head)
        if self.head:
            self.head.Previous(new_node)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1

    def insert_at_tail(self, value):
        new_node = DoublyLinkedListNode(value)
        if self.tail:
            self.tail.Next(new_node)
            new_node.Previous(self.tail)
        else:
            self.head = new_node
        self.tail = new_node
        self.size += 1

    def insert_at(self, index, value):
        if index < 1 or index > self.size + 1:
            raise IndexError("Index out of bounds")
        if index == 1:
            return self.insert_at_head(value)
        if index == self.size + 1:
            return self.insert_at_tail(value)

        new_node = DoublyLinkedListNode(value)
        prev = self.head
        for _ in range(1, index - 1):
            prev = prev.Next()
        nxt = prev.Next()
        prev.Next(new_node)
        new_node.Previous(prev)
        new_node.Next(nxt)
        if nxt:
            nxt.Previous(new_node)
        self.size += 1

    # Deletions
    def delete_at_head(self):
        if not self.head:
            raise IndexError("Delete from empty list")
        nxt = self.head.Next()
        self.head = nxt
        if self.head:
            self.head.Previous(None)
        else:
            self.tail = None
        self.size -= 1

    def delete_at_tail(self):
        if self.size == 0:
            raise IndexError("Delete from empty list")
        if self.size == 1:
            self.head = None
            self.tail = None
            self.size = 0
            return
        prev = self.tail.Previous()
        prev.Next(None)
        self.tail = prev
        self.size -= 1

    def delete_at(self, index):
        if index < 1 or index > self.size:
            raise IndexError("Index out of bounds")
        if index == 1:
            return self.delete_at_head()
        if index == self.size:
            return self.delete_at_tail()
        prev = self.head
        for _ in range(1, index - 1):
            prev = prev.Next()
        to_delete = prev.Next()
        nxt = to_delete.Next()
        prev.Next(nxt)
        if nxt:
            nxt.Previous(prev)
        self.size -= 1

    def delete_value(self, value):
        prev = None
        node = self.head
        while node:
            if node.payload == value:
                if prev is None:
                    self.delete_at_head()
                else:
                    nxt = node.Next()
                    prev.Next(nxt)
                    if nxt:
                        nxt.Previous(prev)
                    if node is self.tail:
                        self.tail = prev
                    self.size -= 1
                return True
            prev = node
            node = node.Next()
        return False

    @classmethod
    def from_head(cls, head_node):
        """Construct a DoublyLinkedList view from an existing head node.

        - Traverses using `Next()`; sets `Previous()` pointers to match
          traversal order (overwriting previous values if present).
        - Handles cycles: counts each unique node once and sets `tail`
          to the last unique node before the cycle repeats.
        """
        inst = cls()
        inst.head = head_node
        if head_node is None:
            inst.tail = None
            inst.size = 0
            return inst

        seen = {}
        node = head_node
        prev = None
        idx = 0
        while node is not None:
            nid = id(node)
            if nid in seen:
                inst.tail = prev
                inst.size = len(seen)
                return inst
            # link previous pointer to maintain doubly-linked invariant
            if prev is None:
                node.Previous(None)
            else:
                node.Previous(prev)

            seen[nid] = node
            prev = node
            node = node.Next()
            idx += 1

        inst.tail = prev
        inst.size = len(seen)
        return inst
