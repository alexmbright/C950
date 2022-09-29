from hashmap import HashMap

h = HashMap()
h.put('Test', 'Hello')
h.put('Test again', 'Hi there')
h.put('Alex', 'LOL')
h.put('Alex', 'LOL LOL')
h.put('Test', 'Hello again')
print(h)
h.remove('Test again')
print(h)
h.put('Test', 'Hi there')
print(h.get('Test'))