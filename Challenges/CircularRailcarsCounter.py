import sys
sys.path.append("..\\Algorithms")
from DataStructures_Nodes import DoublyLinkedListNode as Node 
import random

def guessThePerimeter(circularStart: Node) -> int:
    if not circularStart:
        return 0
    
    traverser = circularStart
    knownStartState = circularStart.payload
    count = 1
    while True:
        traverser = traverser.Next()
        if traverser.payload == knownStartState:
            traverser.payload = not traverser.payload
            if circularStart.payload != knownStartState:
                break
        count += 1
    return count

def RandomListOfBools(size: int) -> list[bool]:
    return [random.randint(0,1) == 1 for _ in range(size)]

def testCase(iteratable: list[bool]):
    train = Node.fromIterable(iteratable)
    if train:
        traverser = train
        while traverser.Next() is not None:
            traverser = traverser.Next() 
        traverser.Next(train)  # Make it circular
        train.Previous(traverser)  # For doubly linked list consistency

        print(train.strChain())  # For visual verification
    count = guessThePerimeter(train)
    expectedCount = len(iteratable)
    assert count == expectedCount, f"Test failed: expected {expectedCount}, got {count}"
    print(f"Test passed: counted {count} railcars successfully.")

for thisTestCase in [
    [],
    RandomListOfBools(1),
    RandomListOfBools(2),
    RandomListOfBools(5),
    RandomListOfBools(10),
    RandomListOfBools(50),
    RandomListOfBools(100),
    [True]* 10,
    [False]* 10,
]:
    testCase(thisTestCase)