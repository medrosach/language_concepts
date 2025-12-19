import sys
sys.path.append('..\\Algorithms')
from DataStructures_Nodes import SingleLinkedListNode as ListNode

ListSize = int(sys.argv[1])
LL = ListNode.fromIterable(list(range(1, ListSize + 1)))

print("Original List:")
print(LL.strChain())

lastOfFirstHalf = LL.findNodeByIndex(ListSize // 2)
lastOfSecondHalf = lastOfFirstHalf.Next()
print("Last node of first half:", lastOfFirstHalf)
print("First node of second half:", lastOfSecondHalf)

headOfSecondHalf = lastOfSecondHalf.Revert()

lastOfFirstHalf.Next(headOfSecondHalf)
lastOfSecondHalf.Next(None)
print("List with reversed second half:")
print(LL.strChain())