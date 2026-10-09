import copy
from functools import reduce

# =====================================================================
# PART A: TUPLES  ( )
# =====================================================================
# A tuple is like a list but IMMUTABLE (cannot be changed after creation).
# Use it for data that must not change (days of week, coordinates, etc.).

t = (1, 2, 3)
t = ('one', 2, 'one')            # mixed types allowed
print(type(t))                   # -> <class 'tuple'>
print(t[2])                      # -> one       (indexing works)
print(t[::])                     # -> ('one', 2, 'one')   (slicing works)
print(len(t))                    # -> 3

# Only two methods:
print(t.index(2))                # -> 1   position of the value
print(t.count('one'))            # -> 2   how many times it appears

# Immutable:
# t[0] = 'change'                # [WILL FAIL] TypeError: 'tuple' object does not support item assignment

# A tuple with ONE item needs a trailing comma
single = (5,)                    # (5) is just the number 5
print(type(single), type((5)))   # -> <class 'tuple'> <class 'int'>

# Trick to "change" a tuple: convert to list, edit, convert back
x = (1, 2, 3)
temp_list = list(x)
temp_list.append(4)
x = tuple(temp_list)             # this is a NEW tuple
print(x)                         # -> (1, 2, 3, 4)

# Unpacking
a, b, c = (10, 20, 30)
print(a, b, c)                   # -> 10 20 30

# =====================================================================
# PART B: SETS  { }
# =====================================================================
# A set is an UNORDERED collection of UNIQUE items.
# No indexing, no duplicates. Fast for membership tests.

x = set()              # empty set (NOTE: {} would create an empty DICT)
x.add(3)
x.add(2)
x.add(1)
x.add(5)
x.add(5)               # duplicate is ignored
print(x)               # -> {1, 2, 3, 5}  (order may vary)

# Remove methods
s = {1, 2, 3}
s.discard(5)           # safe: does nothing if 5 is missing
print(s)               # -> {1, 2, 3}
# s.remove(5)          # [WILL FAIL] KeyError: 5   (remove errors if missing)
s.remove(2)
print(s)               # -> {1, 3}

# pop() removes an ARBITRARY item (sets have no order)
s = {1, 2, 3, 5, 6, 7, 87, 98}
removed = s.pop()
print("popped:", removed)

s.clear()
print(s)               # -> set()   (empty)

# Remove duplicates from a list with set()
lst = [1, 1, 2, 2, 3, 4, 5, 6, 1, 1]
print(set(lst))        # -> {1, 2, 3, 4, 5, 6}
print(list(set(lst)))  # back to a list

# Set maths (extra)
p = {1, 2, 3, 4}
q = {3, 4, 5, 6}
print(p | q)           # union        -> {1, 2, 3, 4, 5, 6}
print(p & q)           # intersection -> {3, 4}
print(p - q)           # difference   -> {1, 2}
print(p ^ q)           # symmetric difference -> {1, 2, 5, 6}

# =====================================================================
# PART C: DICTIONARIES  { key: value }
# =====================================================================
# A dictionary stores KEY -> VALUE pairs (a "mapping"; a hash table in
# other languages). Look up by key, not by position.
# Keys must be unique and immutable (str, int, tuple, bool...).
# Values can be anything.

# Duplicate keys: the LAST value wins
my_dict = {True: 'value1', 'key2': 'value2', 'key1': 'first', 'key1': 'abc'}
print(my_dict)                   # -> {True: 'value1', 'key2': 'value2', 'key1': 'abc'}
print(my_dict['key2'])           # -> value2

# Values of any type, including lists
my_dict = {'key1': 123, 'key2': [12, 23, 33], 'key3': ['item0', 'item1', 'item2']}
print(my_dict['key1'])               # -> 123
print(my_dict['key3'][1])            # -> item1   (index into the list)
print(my_dict['key3'][0].upper())    # -> ITEM0   (call a method on it)

# Change a value
my_dict['key1'] = my_dict['key1'] - 123
print(my_dict['key1'])               # -> 0
my_dict['key1'] -= 123               # shortcut
print(my_dict['key1'])               # -> -123

# Create / update keys by assignment
d = {}
d['animal'] = 'joey'                 # new key
d['answer'] = 42
d['answer'] = 43                     # existing key -> value replaced
print(d)                             # -> {'animal': 'joey', 'answer': 43}

# Nested dictionaries
d = {'key1': {'nestkey': {'subnestkey': 123}}}
print(d['key1']['nestkey']['subnestkey'])   # -> 123

# Counting letters (classic use)
word = 'aabcba'
counts = {}
for ch in word:
    if ch in counts:
        counts[ch] += 1
    else:
        counts[ch] = 1
print(counts)                        # -> {'a': 3, 'b': 2, 'c': 1}

# Useful methods
d = {'key1': 1, 'key2': 2, 'key3': 3}
print(list(d.keys()))                # -> ['key1', 'key2', 'key3']
print(d.values())                    # -> dict_values([1, 2, 3])
print(d.items())                     # -> dict_items([('key1', 1), ('key2', 2), ('key3', 3)])
print(d.get('key9'))                 # -> None   (no error if the key is missing)
print(d.get('key9', 'default'))      # -> default
# d['key9']                          # [WILL FAIL] KeyError: 'key9'
d.update({'key4': 4})                # add/merge
print(d.pop('key1'))                 # remove a key and return its value -> 1
for k, v in d.items():               # loop over keys and values
    print(k, '->', v)
print('key2' in d)                   # -> True   (checks KEYS)

# Dictionary comprehension: {key: value for item in iterable}
print({x: x ** 2 for x in range(1, 6)})   # -> {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# =====================================================================
# PART D: SHALLOW COPY vs DEEP COPY
# =====================================================================
# b = a            -> NOT a copy: both names point to the same list.
# copy.copy(a)     -> SHALLOW: new outer list, but the inner lists are shared.
# copy.deepcopy(a) -> DEEP: everything is copied, fully independent.

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
shallow[0][0] = 12               # changes the SHARED inner list
print('original', original)      # -> [[12, 2], [3, 4]]   <- changed too!
print('shallow ', shallow)       # -> [[12, 2], [3, 4]]

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 12
print('original', original)      # -> [[1, 2], [3, 4]]    <- untouched
print('deep    ', deep)          # -> [[12, 2], [3, 4]]

# =====================================================================
# PART E: FUNCTIONS
# =====================================================================
# A function groups statements so you can reuse them.
#   def name(parameters):
#       '''docstring: what the function does'''
#       ... code ...
#       return result          (optional)
# Parameters = names in the definition. Arguments = values you pass in.


def say_hello():
    print('hello')


say_hello()                      # -> hello


def greeting(name):
    print(f'Hello {name}!')


greeting('Kota')                 # -> Hello Kota!


def print_num(n):
    """Print the multiplication table of n (n x 1 ... n x n)."""
    for i in range(1, n + 1):
        print(i * n)


print_num(3)                     # -> 3, 6, 9

# ---------------------------------------------------------------------
# return vs print  (very common confusion)
# ---------------------------------------------------------------------
# print  -> only SHOWS a value on screen; the function returns None.
# return -> hands the value BACK so you can store/use it.


def add_print(a, b):
    print(a + b)


def add_return(a, b):
    return a + b


x = add_print(5, 6)              # prints 11
print(x)                         # -> None   (nothing was returned)
y = add_return(5, 6)
print(y + 9)                     # -> 20     (we can keep using the result)
# print(x + 6)                   # [WILL FAIL] TypeError: NoneType + int


def func_with_print():
    print("Hello")


def func_with_return():
    return "Hello"


a = func_with_print()            # prints Hello
b = func_with_return()
print("a =", a)                  # -> a = None
print("b =", b)                  # -> b = Hello

# Python doesn't check types, so one function works for many types:
print(add_return('ab', 'cd'))    # -> abcd
print(add_return([1], [2]))      # -> [1, 2]

# Default arguments, keyword arguments, *args, **kwargs (extra)


def power(base, exp=2):          # exp has a default value
    return base ** exp


print(power(4))                  # -> 16
print(power(2, 5))               # -> 32
print(power(exp=3, base=2))      # -> 8   (keyword arguments, any order)


def total(*args):                # *args = any number of positional arguments
    return sum(args)


print(total(1, 2, 3, 4))         # -> 10


def show(**kwargs):              # **kwargs = any number of key=value pairs
    return kwargs


print(show(a=1, b=2))            # -> {'a': 1, 'b': 2}

# Returning several values returns a tuple


def min_max(nums):
    return min(nums), max(nums)


lo, hi = min_max([4, 9, 1])
print(lo, hi)                    # -> 1 9


# ---------------------------------------------------------------------
# Example: prime number check
# ---------------------------------------------------------------------
# A prime is divisible only by 1 and itself. Try dividing by 2..num-1.
# for ... else : the else runs only if the loop did NOT hit "break".
def is_prime(num):
    """Return True if num is prime."""
    if num < 2:                  # fix: the notebook version said 1 was prime
        return False
    for n in range(2, num):
        if num % n == 0:
            return False
    return True


print(is_prime(7), is_prime(10), is_prime(1))   # -> True False False

# =====================================================================
# PART F: LAMBDA (small anonymous function)
# =====================================================================
# lambda arguments: expression      (one expression, returns its value)
add = lambda a, b: a + b
print(add(4, 3))                 # -> 7
square = lambda n: n * n
print(square(6))                 # -> 36

# =====================================================================
# PART G: ITERATORS AND GENERATORS
# =====================================================================
# ITERABLE : something you can loop over (list, str, tuple, dict, range).
# ITERATOR : object with __iter__() and __next__(); gives one item at a
#            time. Get one with iter(iterable); advance with next().
# After the last item next() raises StopIteration (a for loop catches this
# automatically and stops).
nums = [1, 2, 3]
it = iter(nums)
print(next(it))                  # -> 1
print(next(it))                  # -> 2
print(next(it))                  # -> 3
# next(it)                       # [WILL FAIL] StopIteration

s = iter('joey')                 # a string is iterable; iter() makes it an iterator
print(next(s), next(s))          # -> j o

# GENERATOR: a function that uses yield instead of return.
#   - yield PAUSES the function and remembers where it was.
#   - Values are produced one at a time, so no huge list in memory.


def gencubes(n):
    for num in range(n):
        yield num ** 3


print(gencubes(5))               # -> <generator object ...>
for cube in gencubes(5):
    print(cube)                  # -> 0 1 8 27 64


def genfibon(n):
    """Generate the first n Fibonacci numbers."""
    a, b = 1, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


print(list(genfibon(10)))        # -> [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


def fibon(n):
    """Same thing as a normal function: builds the WHOLE list in memory."""
    a, b = 1, 1
    output = []
    for _ in range(n):
        output.append(a)
        a, b = b, a + b
    return output


print(fibon(10))                 # same result, but uses more memory for big n

g = (x * x for x in range(3))    # generator expression (like a comprehension with ())
print(next(g), next(g), next(g)) # -> 0 1 4

# =====================================================================
# PART H: MAP, FILTER, REDUCE
# =====================================================================
# map(function, iterable)    -> apply the function to EVERY item
# filter(function, iterable) -> keep items where the function returns True
# reduce(function, iterable) -> combine items into ONE value (needs import)
# map and filter return lazy objects; wrap in list() to see the result.

# ---- map ----
lst = [1, 2, 3, 4, 5, 6]
print(list(map(lambda x: x + 5, lst)))      # -> [6, 7, 8, 9, 10, 11]


def celsius(T):
    return (float(5) / 9) * (T - 32)


def fahrenheit(T):
    return (float(9) / 5) * T + 32


temp = [0, 22.5, 40, 100]
c_temps = list(map(celsius, temp))
print(c_temps)                               # Fahrenheit -> Celsius
print(list(map(fahrenheit, c_temps)))        # -> [0.0, 22.5, 40.0, 100.0]

# map over TWO or more iterables (stops at the shortest one)
a = [1, 2, 3, 4]
b = [5, 6, 7, 8]
c = [9, 10, 11, 12, 4, 5]
print(list(map(lambda x, y: x + y, a, c)))               # -> [10, 12, 14, 16]
print(list(map(lambda x, y, z: x + y + z, a, b, c)))     # -> [15, 18, 21, 24]
# NOTE: the notebook defined its own function named sum(), which hides the
# built-in sum(). Avoid naming functions after built-ins.

# ---- reduce ----
# reduce(f, [s1, s2, s3, s4]) works like f(f(f(s1, s2), s3), s4)
words = ['kota', 'ruchik', 'joey', 'tribiani']
print(reduce(lambda a, b: a + b, words))     # -> kotaruchikjoeytribiani
print(reduce(lambda a, b: a + b, [1, 2, 3, 4]))          # -> 10

max_find = lambda a, b: a if a > b else b
print(reduce(max_find, [47, 49, 42, 55, 56]))            # -> 56  (same as max())

# ---- filter ----


def even_check(num):
    return num % 2 == 0          # returns True/False
    # NOTE: the notebook version returned True or None. It worked (None
    # counts as False) but returning a real bool is cleaner.


lst = [1, 2, 3, 4, 5, 6, 7, 8]
print(list(filter(even_check, lst)))             # -> [2, 4, 6, 8]
print(list(filter(lambda x: x % 2 == 0, lst)))   # same with lambda

# map vs filter: map CHANGES every item, filter KEEPS some items
print(list(map(lambda x: x % 2 == 0, lst)))
# -> [False, True, False, True, False, True, False, True]

words = ["ruchi", 'Nikhil', 'phoebee', 'swapna']
print(list(filter(lambda w: len(w) > 6, words)))     # -> ['phoebee']


