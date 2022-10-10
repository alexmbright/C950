class HashMap:

    # Time: O(1) - Space: O(n)
    def __init__(self):
        self.size = 49157
        self.map = [None] * self.size
        self.length = 0

    # Time: O(n) - Space: O(1)
    # Returns the hash value (index) of the desired bucket.
    # Hash value if key is numeric: key % size
    # Hash value if key is not numeric: sum of Unicode codes % size
    def _hash(self, key):
        if str(key).isnumeric():
            return key % self.size
        index_hash = 0
        for char in str(key):
            index_hash += ord(char)
        return index_hash % self.size

    # Time: O(n) - Space: O(1)
    # Puts new key-value pair into the HashMap, or updates value if key exists
    def put(self, key, value):

        # Determine bucket index and instantiate new key-value pair
        index = self._hash(key)
        new_pair = [key, value]

        # If bucket does not exist, add key-value pair
        if self.map[index] is None:
            self.map[index] = [new_pair]
            self.length += 1 # Keep track of HashMap length!
            return

        # If key already exists in bucket, update value
        for pair in self.map[index]:
            if pair[0] == key:
                pair[1] = value
                return

        # If bucket exists and key is unique, add new key-value pair
        self.map[index].append(new_pair)
        self.length += 1
        return

    # Time: O(n) - Space: O(1)
    # Searches for and returns value for provided key
    def get(self, key):
        index = self._hash(key)
        if self.map[index] is not None:
            for pair in self.map[index]:
                if pair[0] == key:
                    return pair[1]

        # If key not found in the HashMap, return None
        return None

    # Time: O(n) - Space: O(1)
    # Searches for and removes provided key (and value) from HashMap.
    # Returns True if key-value pair removed, otherwise False
    def remove(self, key):
        index = self._hash(key)

        # If bucket does not exist, return False
        if self.map[index] is None:
            return False

        # If key found in bucket, remove and return True
        for i in range(len(self.map[index])):
            if self.map[index][i][0] == key:
                del self.map[index][i]
                # If necessary, replace empty bucket with None
                if not self.map[index]:
                    self.map[index] = None
                self.length -= 1 # Keep track of HashMap length!
                return True

        # If key not found, remove and return False
        return False

    # Time: O(1) - Space: O(1)
    # Overrides built-in len function
    # This is why we kept track of length. Especially helpful in loops.
    def __len__(self):
        return self.length

    # Time: O(n) - Space: O(1)
    # Overrides built-in str function
    # Used for testing collision count and optimizing hash function
    def __str__(self):
        result = ""
        collisions = 0
        for bucket in self.map:
            if bucket is not None:
                if len(bucket) > 1:
                    collisions += len(bucket) - 1
                result += "\n" + str(bucket)
        result += "\n\nCollision count: " + str(collisions)
        return result

