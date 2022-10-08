class HashMap:

    # Time: O(1) - Space: O(n)
    def __init__(self, size):
        self.size = size
        self.map = [None] * self.size
        self.length = 0

    # Time: O(n) - Space: O(1)
    def _hash(self, key):
        index_hash = 0
        for char in str(key):
            index_hash += ord(char)
        return index_hash % self.size

    # Time: O(n) - Space: O(1)
    def put(self, key, value):
        index = self._hash(key)
        new_pair = [key, value]

        if self.map[index] is None:
            self.map[index] = [new_pair]
            self.length += 1
            return True
        for pair in self.map[index]:
            if pair[0] == key:
                pair[1] = value
                return True
        self.map[index].append(new_pair)
        self.length += 1
        return True

    # Time: O(n) - Space: O(1)
    def get(self, key):
        index = self._hash(key)
        if self.map[index] is not None:
            for pair in self.map[index]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Time: O(n) - Space: O(1)
    def remove(self, key):
        index = self._hash(key)
        if self.map[index] is None:
            return False
        for i in range(len(self.map[index])):
            if self.map[index][i][0] == key:
                del self.map[index][i]
                if not self.map[index]:
                    self.map[index] = None
                self.length -= 1
                return True
        return False

    # Time: O(1) - Space: O(1)
    def __len__(self):
        return self.length
