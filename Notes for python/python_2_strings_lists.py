# =====================================================================
# PART A: STRINGS
# =====================================================================
# A string stores text. It is a SEQUENCE: Python remembers the position
# (index) of every character.

# ---------------------------------------------------------------------
# A1. CREATING STRINGS
# ---------------------------------------------------------------------
# Use single quotes ' ' or double quotes " ". Pick the one that is NOT
# inside your text.
a = 'hello'
b = "String built with double quotes"
c = "Now I'm ready to use the single quotes inside a string!"
# d = 'I'm using single quotes'   # [WILL FAIL] SyntaxError: the ' in I'm ends the string
d = 'It\'s fine with a backslash'  # \' is an "escape": it puts a literal quote
print(a, b, c, d, sep="\n")

# Escape characters:  \n new line,  \t tab,  \\ backslash,  \' and \" quotes
print('Use \\n to print a new line:\nsee?')

print(len('Hello World'))        # -> 11  (spaces count too)

# ---------------------------------------------------------------------
# A4. INDEXING
# ---------------------------------------------------------------------
# Index starts at 0. Negative index counts from the END (-1 = last).
#   H   e   l   l   o       W   o   r   l   d
#   0   1   2   3   4   5   6   7   8   9   10
#  -11 -10  -9  -8  -7  -6  -5  -4  -3  -2  -1
s = 'Hello World'
print(s[0])      # -> H
print(s[1])      # -> e
print(s[10])     # -> d
print(s[-1])     # -> d   (last letter)
print(s[-3])     # -> r   (third from the end)
# print(s[11])   # [WILL FAIL] IndexError: string index out of range

# ---------------------------------------------------------------------
# A5. SLICING  s[start:stop:step]
# ---------------------------------------------------------------------
# start is INCLUDED, stop is NOT included ("up to but not including").
# Any part can be left out: start defaults to 0, stop to the end,
# step to 1.
print(s[2:])       # -> llo World   (from index 2 to the end)
print(s[:5])       # -> Hello       (index 0 up to, not including, 5)
print(s[0:1])      # -> H
print(s[::])       # -> Hello World (everything)
print(s[:-1])      # -> Hello Worl  (everything except the last letter)
print(s[::2])      # -> HloWrd      (every 2nd character)
print(s[::-1])     # -> dlroW olleH (step -1 = reversed string)
print(s)           # slicing never changes the original -> Hello World

# ---------------------------------------------------------------------
# A6. STRINGS ARE IMMUTABLE
# ---------------------------------------------------------------------
# You cannot change a character inside a string.
# s[0] = 'x'       # [WILL FAIL] TypeError: 'str' object does not support item assignment
# You CAN build a new string and reassign the variable:
s = 'Hello World'
print(s + ', I am Joey!')     # -> Hello World, I am Joey!   (s itself unchanged)
s = s + ', I am Joey!'        # reassign to keep the change
print(s)
new = 'J' + s[1:]             # "change" the first letter by building a new string
print(new)

# Repetition with *
letter = 'z'
print(letter * 10)            # -> zzzzzzzzzz

# ---------------------------------------------------------------------
# A7. COMMON STRING METHODS   (syntax: object.method(arguments))
# ---------------------------------------------------------------------
# Methods never change the original string; they RETURN a new one.
s = 'Hello world'
print(s.upper())              # -> HELLO WORLD
print(s.lower())              # -> hello world
print(s.title())              # -> Hello World   (each word capitalised)
print(s.capitalize())         # -> Hello world   (only first letter)
print(s.split())              # -> ['Hello', 'world']   (splits on spaces)
print(s.split('w'))           # -> ['Hello ', 'orld']   (the 'w' is removed)
print('ruchik.kota'.split('.'))   # -> ['ruchik', 'kota']
print('-'.join(['a', 'b', 'c']))  # -> a-b-c   (join is the opposite of split)
print('  padded  '.strip())       # -> padded  (removes spaces at both ends)
print(s.replace('world', 'Python'))   # -> Hello Python

# Location and counting
print(s.count('o'))           # -> 2   how many times 'o' appears
print(s.find('o'))            # -> 4   index of the FIRST 'o'
print(s.find('z'))            # -> -1  find() returns -1 if not found
print(s.index('o'))           # -> 4   same as find, but ERRORS if not found
print(s.startswith('Hell'))   # -> True
print(s.endswith('d'))        # -> True   (same idea as s[-1] == 'd')

# expandtabs: turns \t into spaces
print('hello\thi'.expandtabs())    # -> hello   hi

# ---------------------------------------------------------------------
# A8. "IS" CHECK METHODS (all return True or False)
# ---------------------------------------------------------------------
print('hello'.isalnum())     # -> True   letters and/or digits only
print('$'.isalnum())         # -> False  special character
print('Ruchik'.isalpha())    # -> True   letters only
print('1234'.isdigit())      # -> True   digits only
print('ruch'.islower())      # -> True   all cased letters are lowercase
print('RUCH'.isupper())      # -> True
print(' '.isspace())         # -> True   only whitespace
print('Ruchik'.istitle())    # -> True   Title Case

# =====================================================================
# PART B: LISTS
# =====================================================================
# A list is an ordered, MUTABLE (changeable) sequence in [ ] separated by
# commas. It can hold ANY types and has no fixed size.

# ---------------------------------------------------------------------
# B1. CREATING LISTS
# ---------------------------------------------------------------------
my_list = [1, 2, 3]
my_list = ['A string', 23, 100.232, 'o']      # mixed types are fine
nested = [[1, 2, 3], 5, 7, 'text']            # lists can contain lists
print(len(my_list))                           # -> 4

# ---------------------------------------------------------------------
# B2. INDEXING AND SLICING (same rules as strings)
# ---------------------------------------------------------------------
my_list = ['one', 'two', 'three', 4, 5]
print(my_list[2])         # -> three
print(my_list[-1])        # -> 5
print(my_list[1:])        # -> ['two', 'three', 4, 5]
print(my_list[0:5:3])     # -> ['one', 4]       (start 0, every 3rd item)
print(my_list[:5:2])      # -> ['one', 'three', 5]

# ---------------------------------------------------------------------
# B3. CONCATENATE AND REPEAT
# ---------------------------------------------------------------------
print(my_list + ['new item', 5])   # makes a NEW list; my_list is unchanged
print(my_list)
my_list = my_list + ['added permanently']   # reassign to keep it
print(my_list)
print([1, 2] * 3)                  # -> [1, 2, 1, 2, 1, 2]

# ---------------------------------------------------------------------
# B4. LISTS ARE MUTABLE
# ---------------------------------------------------------------------
l = [1, 2, 3]
l[1] = 4                  # change an item in place
print(l)                  # -> [1, 4, 3]

# ---------------------------------------------------------------------
# B5. LIST METHODS (most change the list IN PLACE)
# ---------------------------------------------------------------------
l = [1, 2, 3, 2]

# append(x): add ONE item at the end
l.append(4)
print(l)                  # -> [1, 2, 3, 2, 4]

# count(x): how many times x appears
print(l.count(2))         # -> 2
print(l.count(10))        # -> 0

# index(x): position of the FIRST x (ValueError if not in the list)
print(l.index(3))         # -> 2
# l.index(12)             # [WILL FAIL] ValueError: 12 is not in list

# insert(index, x): put x at that position
l.insert(1, 'mango')
print(l)                  # -> [1, 'mango', 2, 3, 2, 4]

# pop(): remove AND return the last item (or the item at a given index)
last = l.pop()
print(last, l)            # -> 4 [1, 'mango', 2, 3, 2]
first = l.pop(0)
print(first, l)           # -> 1 ['mango', 2, 3, 2]
# [].pop()                # [WILL FAIL] IndexError: pop from empty list

# remove(x): delete the FIRST item equal to x
l = [1, 2, 3, 4, 3]
l.remove(3)
print(l)                  # -> [1, 2, 4, 3]   (only the first 3 was removed)

# reverse(): flip the order in place
l.reverse()
print(l)                  # -> [3, 4, 2, 1]

# sort(): sort in place (ascending by default)
l = [1, 3, 47, 8, 12]
l.sort()
print(l)                  # -> [1, 3, 8, 12, 47]
l.sort(reverse=True)
print(l)                  # -> [47, 12, 8, 3, 1]
# sorted(l) returns a NEW sorted list and leaves l alone.
new_list = ['a', 'e', 'x', 'b', 'c', '1', '2']
new_list.sort()
print(new_list)           # -> ['1', '2', 'a', 'b', 'c', 'e', 'x']
# NOTE: a list with numbers AND strings cannot be sorted (TypeError).

# ---------------------------------------------------------------------
# B6. APPEND vs EXTEND
# ---------------------------------------------------------------------
# append adds its argument as ONE item. extend adds EACH item of an iterable.
x = [1, 2, 3]
x.append([4, 5])
print(x)                  # -> [1, 2, 3, [4, 5]]   (a list inside the list)

x = [1, 2, 3]
x.extend([4, 5])
print(x)                  # -> [1, 2, 3, 4, 5]

# ---------------------------------------------------------------------
# B7. NESTED LISTS (matrix)
# ---------------------------------------------------------------------
lst_1 = [1, 2, 3]
lst_2 = [4, 5, [9, 8]]
lst_3 = [7, 8, 9]
matrix = [lst_1, lst_2, lst_3]
print(matrix)                 # -> [[1, 2, 3], [4, 5, [9, 8]], [7, 8, 9]]
print(matrix[0][2])           # -> 3   (row 0, item 2)
print(matrix[1][2][1])        # -> 8   (row 1 -> item 2 is [9, 8] -> item 1)

# ---------------------------------------------------------------------
# B8. LIST COMPREHENSIONS (build a list in one line)
# ---------------------------------------------------------------------
# Pattern:  [expression for item in iterable if condition]
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Take column 3 of each row
first_col = [row[2] for row in matrix]
print(first_col)              # -> [3, 6, 9]

# Same thing with a normal for loop
first_col = []
for row in matrix:
    first_col.append(row[2])
print(first_col)              # -> [3, 6, 9]

# With a condition: drop 91 and 18
my_list = [1, 2, 3, 91, 4, 5, 6, 18, 9, 7]
cleaned = [i for i in my_list if i != 91 and i != 18]
print(cleaned)                # -> [1, 2, 3, 4, 5, 6, 9, 7]

# Squares of 1..5
print([n ** 2 for n in range(1, 6)])   # -> [1, 4, 9, 16, 25]

# ---------------------------------------------------------------------
# B9. STRING vs LIST - QUICK COMPARISON
# ---------------------------------------------------------------------
# | Feature          | str                | list              |
# |------------------|--------------------|-------------------|
# | Brackets         | ' ' or " "         | [ ]               |
# | Mutable?         | NO                 | YES               |
# | Indexing/slicing | yes                | yes               |
# | Holds            | characters only    | any objects       |
