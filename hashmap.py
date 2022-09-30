class HashMap:

    def __init__(self):
        self.map = [None] * 71
        self.length = 0

    def _hash(self, key):
        index_hash = 0
        for char in str(key):
            index_hash += ord(char)
        return index_hash % 71

    def put(self, key, value):
        index_hash = self._hash(key)
        key_val = [key, value]

        if self.map[index_hash] is None:
            self.map[index_hash] = list([key_val])
            return True
        for pair in self.map[index_hash]:
            if pair[0] == key:
                pair[1] = value
                return True
        self.map[index_hash].append(key_val)
        self.length += 1
        return True

    def get(self, key):
        index_hash = self._hash(key)
        if self.map[index_hash] is not None:
            for pair in self.map[index_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def remove(self, key):
        index_hash = self._hash(key)
        if self.map[index_hash] is None:
            return False
        for i in range(0, len(self.map[index_hash])):
            if self.map[index_hash][i][0] == key:
                del self.map[index_hash][i]
                if not self.map[index_hash]:
                    self.map[index_hash] = None
                self.length -= 1
                return True
        return False

    def __len__(self):
        return self.length

    def __str__(self):
        pairs = ""
        for item in self.map:
            if item is not None:
                for pair in item:
                    pairs += '\t' + str(pair) + '\n'
        return pairs