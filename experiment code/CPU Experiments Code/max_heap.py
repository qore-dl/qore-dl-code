class MaxHeap(object):
    def __init__(self,max_size,fn):
        """MaxHeap class.
               Arguments:
                   max_size {int} -- The maximum size of MaxHeap instance.
                   fn {function} -- Function to caculate the values of items
                   when comparing items.
               Attributes:
                   _items {object} -- The items in the MaxHeap instance.
                   size {int} -- The size of MaxHeap instance.
               """
        self.max_size = max_size
        self.fn = fn

        self._items = [None]*max_size
        self.size = 0

    def __str__(self):
        item_values = str([self.fn(x) for x in self.items])
        info = (self.size, self.max_size, self.items, item_values)
        return "Size: %d\nMax size: %d\nItems: %s\nItem_values: %s\n" % info
    # Python内置的@property装饰器就是负责把一个方法变成属性调用的：
    @property
    def items(self):
        return self._items[:self.size]#生成数值传递的副本，防止因为操作而影响原地址的list

    @property
    def full(self):
        """If the heap is full.
                Returns:
                    bool
                """
        return self.size == self.max_size

    def value(self,idx):
        """Caculate the value of item.
                Arguments:
                    idx {int} -- The index of item.
                Returns:
                    float
                """
        item = self._items[idx]

        if item is None:
            ret = -float('inf')
        else:
            ret = self.fn(item)

        return ret

    def add(self,item):
        """Add a new item to the MaxHeap.
                Arguments:
                    item {object} -- The item to add.
                """
        if self.full:
            if self.fn(item) < self.value(0):
                tmp = self._items[0]
                self._items[0] = item
                self._shift_down(0)#从顶至底，开始维护最大值堆，另整个堆满足左右子树小于父节点
                return tmp
            else:
                return item
        else:
            self._items[self.size] = item#堆还没满，从底向上不断浮动，直到达到最合适的位置
            self.size += 1
            self._shift_up(self.size-1)
            return None

    def pop(self):
        """Pop the top item out of the heap.
               Returns:
                   object -- The item popped.
               """
        assert self.size>0,"Cannot pop item! The MaxHeap is empty!"
        ret = self._items[0]
        self._items[0],self._items[self.size-1] = self._items[self.size-1],self._items[0]
        self.size -= 1
        self._shift_down(0)#从顶部开始维护
        return ret

    def _shift_up(self,idx):
        """Shift up item unitl its parent is greater than the item.
                Arguments:
                    idx {int} -- Heap item's index.
                """
        assert idx < self.size,"The parameter idx must be less than heap's size!"
        parent = (idx - 1)//2
        while parent >= 0 and self.value(parent) < self.value(idx):
            self._items[parent],self._items[idx] = self._items[idx],self._items[parent]
            idx = parent
            parent = (idx - 1)//2


    def _shift_down(self,idx):
        """Shift down item until its children are less than the item.
               Arguments:
                   idx {int} -- Heap item's index.
               """
        child = (idx+1)*2-1
        while child < self.size:
            # Compare the left child and the right child and get the index
            # of the larger one.
            if child+1 < self.size and self.value(child+1) > self.value(child):
                child = child+1
            # Swap the items, if the value of father is less than child.
            if self.value(idx) < self.value(child):
                self._items[idx],self._items[child] = self._items[child],self._items[idx]
                idx = child
                child = (idx+1)*2 - 1
            else:
                break

    def _is_valid(self):
        """Validate a MaxHeap by comparing all the parents and its children.
                Returns:
                    bool
                """
        ret = []
        for i in range(1,self.size):
            parent = (i-1) // 2
            ret.append(self.value(i)<=self.value(parent))
        return all(ret)#all判断可迭代对象中是否全部元素为True/1/非空/非None

    def clear(self):
        self._items = [None] * self.max_size
        self.size = 0






