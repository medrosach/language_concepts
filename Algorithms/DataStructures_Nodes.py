import copy
import operator

class Node:
    """Generic node base class.

    - Each instance has its own `payload` and `NodeLinks` dictionary.
    - `GetSetLink` uses a missing-value sentinel so callers can set a link
      to `None` explicitly (important for linked-list tail markers).
    """

    _MISSING = object()

    def __init__(self, val: any = None, links: dict[str, "Node"] | None = None):
        self.payload = val
        # Instance-level links dictionary (avoid class-level mutable shared state)
        self.NodeLinks: dict[str, "Node"] = {}
        if links:
            for linkName, nodeLink in links.items():
                if not isinstance(linkName, str):
                    raise TypeError("Node link name must be a string")
                if nodeLink is not None and not isinstance(nodeLink, Node):
                    raise TypeError("Node link must be a Node or None")
                self.NodeLinks[linkName] = nodeLink

    def GetSetLink(self, linkName: str, linkVal: object = _MISSING):
        """Get or set a named link.

        - If `linkVal` is not passed (internally compared to `_MISSING`),
          the method returns the current value for `linkName` or `None` if
          it doesn't exist.
        - If `linkVal` is passed, it will set (or create) that link to the
          provided value (which may be `None`) after validating types.
        """
        if not isinstance(linkName, str):
            raise TypeError("linkName must be a string")

        # Setter case (note: linkVal can be None)
        if linkVal is not Node._MISSING:
            if linkVal is not None and not isinstance(linkVal, Node):
                raise TypeError("link value must be a Node or None")
            self.NodeLinks[linkName] = linkVal
            return self.NodeLinks[linkName]

        # Getter case
        return self.NodeLinks.get(linkName, None)

    def __lt__(self, other: any) -> bool:
        return self.__doCompare(operator.lt, other)

    def __gt__(self, other: any) -> bool:
        return self.__doCompare(operator.gt, other)

    def __le__(self, other: any) -> bool:
        return self.__doCompare(operator.le, other)

    def __ge__(self, other: any) -> bool:
        return self.__doCompare(operator.ge, other)

    def __eq__(self, other: any) -> bool:
        return self.__doCompare(operator.eq, other)

    def __ne__(self, other: any) -> bool:
        return self.__doCompare(operator.ne, other)

    def __str__(self):
        return str(self.payload)

    def __doCompare(self, op, value: any) -> bool:
        thisVal = copy.deepcopy(self.payload)
        thatVal = copy.deepcopy(value.payload) if isinstance(value, Node) else copy.deepcopy(value)

        # Allow some safe coercions similar to previous implementation
        if type(thisVal) != type(thatVal):
            if isinstance(thisVal, str):
                thatVal = str(thatVal)
            elif isinstance(thisVal, bool):
                if isinstance(thatVal, str):
                    thatVal = thatVal != ""
                else:
                    thatVal = thatVal != 0

        # Disallow ordering comparisons for strings and bools (only ==/!= allowed)
        if (isinstance(thisVal, str) or isinstance(thisVal, bool)) and op not in (operator.eq, operator.ne):
            raise TypeError(f"Unsupported ordering comparison for type {type(thisVal)}")

        return op(thisVal, thatVal)

class SingleLinkedListNode(Node):
    def __init__(self, item=None, next: "SingleLinkedListNode" = None):
        super().__init__(item)
        self.NodeLinks["next"] = next

    def Next(self, targetNode=Node._MISSING):
        return self.GetSetLink("next", targetNode)
    
    def Revert(self) -> "SingleLinkedListNode":
        """Reverts the linked list starting from this node and returns new head."""
        prev = None
        current = self
        while current is not None:
            next_node = current.Next()
            current.Next(prev)
            prev = current
            current = next_node
        return prev
    
    def strChain(self) -> str:
        """Creates a printable string for the linked list starting from this node.
        Detects loops and indicates their position."""
        theNodesInfo = self.__TraversalSearch()
        if theNodesInfo["loopIndex"] != -1:
            stringChain = " -> ".join(theNodesInfo["parts"])
            if stringChain:
                return f"{stringChain} -> (loop to index {theNodesInfo['loopIndex']}: {theNodesInfo['parts'][theNodesInfo['loopIndex']]})"
            return f"(loop to index {theNodesInfo['loopIndex']}: {theNodesInfo['parts'][theNodesInfo['loopIndex']]})"
        return " -> ".join(theNodesInfo["parts"]) + " -> None"
    
    def findNodeByIndex(self, index: int):
        """Finds a node by its 1-based index (positive) or negative index (from end).
        Returns None if not found."""
        if index == 0:
            return self
        if index > 0:
            return self.__TraversalSearch(target=index, searchType="byIndex")["target"]
        wholeListInfo = self.__TraversalSearch()
        if wholeListInfo["count"] + index >= 0:
            return wholeListInfo["parts"][index]
        return None
    
    def __TraversalSearch(self, target: any = Node._MISSING, searchType: str = "byIndex") -> dict[str]:
        traverser = self
        retVal = {
            "parts": [],
            "target": Node._MISSING,
            "loopIndex": -1,
            "count": 0
        }
        seen = {}
        idx = 0
        while traverser is not None:
            node_id = id(traverser)
            if node_id in seen:
                retVal["loopIndex"] = seen[node_id]
                break

            seen[node_id] = idx
            retVal["parts"].append(str(traverser.payload))
            traverser = traverser.Next()
            idx += 1
            if target != Node._MISSING and ((searchType == "byIndex" and idx == target-1) or (searchType == "byValue" and traverser.payload == target)):
                retVal["target"] = traverser
                break
        retVal["count"] = idx
        return retVal
        
    @classmethod
    def fromIterable(cls, iterable) -> "SingleLinkedListNode":
        """Creates a linked list from an iterable and returns the head node."""
        iterator = iter(iterable)
        try:
            head = cls(next(iterator))
        except StopIteration:
            return None  # Empty iterable

        current = head
        for item in iterator:
            new_node = cls(item)
            current.Next(new_node)
            current = new_node

        return head

class DoublyLinkedListNode(SingleLinkedListNode):
    def __init__(self, item=None, prev=None, next=None):
        super().__init__(item, next)
        self.NodeLinks["previous"] = prev

    def Previous(self, targetNode=Node._MISSING):
        return self.GetSetLink("previous", targetNode)
    
    def Revert(self) -> "DoublyLinkedListNode":
        """Reverts the doubly linked list starting from this node and returns new head."""
        prev = None
        current = self
        while current is not None:
            next_node = current.Next()
            current.Next(prev)
            current.Previous(next_node)
            prev = current
            current = next_node
        return prev
    
    @classmethod
    def fromIterable(cls, iterable) -> "DoublyLinkedListNode":
        """Creates a doubly linked list from an iterable and returns the head node."""
        iterator = iter(iterable)
        try:
            head = cls(next(iterator))
        except StopIteration:
            return None  # Empty iterable

        current = head
        for item in iterator:
            new_node = cls(item)
            current.Next(new_node)
            new_node.Previous(current)
            current = new_node

        return head

class TreeNode(Node):
    def __init__(self, item=None, leftNode=None, rightNode=None, parent=None):
        super().__init__(item)
        self.NodeLinks["left"] = leftNode
        self.NodeLinks["right"] = rightNode
        self.NodeLinks["parent"] = parent

    def Left(self, targetNode=Node._MISSING):
        return self.GetSetLink("left", targetNode)

    def Right(self, targetNode=Node._MISSING):
        return self.GetSetLink("right", targetNode)

    def Parent(self, targetNode=Node._MISSING):
        return self.GetSetLink("parent", targetNode)
    
    def getHeight(self) -> int:
        left_height = self.Left().getHeight() if self.Left() else 0
        right_height = self.Right().getHeight() if self.Right() else 0
        return 1 + max(left_height, right_height)
    
    def printTree(self):
        height = self.getHeight()
        currentNodes = [{"node":self, "level":0}]
        prev_level = 0
        padding = " " * (2**height)
        while currentNodes:
            nodeInfo = currentNodes.pop(0)
            if nodeInfo["level"] > prev_level:
                print()
                prev_level = nodeInfo["level"]
                padding = " " * (2**(height - prev_level))
            print(padding + str(nodeInfo["node"]), end=padding)
            if nodeInfo["node"].Left():
                currentNodes.append({"node": nodeInfo["node"].Left(), "level": nodeInfo["level"] + 1})
            if nodeInfo["node"].Right():
                currentNodes.append({"node": nodeInfo["node"].Right(), "level": nodeInfo["level"] + 1})
        print()

