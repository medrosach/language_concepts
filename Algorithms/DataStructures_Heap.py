clsas Heap:

    def __init__(self):
        self.data = [] 
        self.size = 0
        self.type = "min"  # or "max"
    
    def insert(self, value):
        """Insert value into the heap."""
        self.data.append(value)
        self.size += 1
        self._heapify_up(self.size - 1)
    
    def _heapify_up(self, index):
        """Maintain heap property by moving the element at index up."""
        parent_index = (index - 1) // 2
        if index > 0:
            if (self.type == "min" and self.data[index] < self.data[parent_index]) or \
               (self.type == "max" and self.data[index] > self.data[parent_index]):
                self.data[index], self.data[parent_index] = self.data[parent_index], self.data[index]
                self._heapify_up(parent_index)
    def _heapify_down(self, index):
        """Maintain heap property by moving the element at index down."""
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest_largest = index

        if left_child_index < self.size:
            if (self.type == "min" and self.data[left_child_index] < self.data[smallest_largest]) or \
               (self.type == "max" and self.data[left_child_index] > self.data[smallest_largest]):
                smallest_largest = left_child_index
                