


print("hello Joeyyy!")      # -> hello Joeyyy!
print(123)                  # -> 12


# ---------------------------------------------------------------------
# 2. FUNDAMENTAL DATA TYPES
# ---------------------------------------------------------------------
# int      whole numbers          9, -4, 1000
# float    decimal numbers        1.234
# bool     True / False           (capital T and F, no quotes)
# str      text                   'hello' or "hello"
# complex  real + imaginary       1.0 - 2.0j
# Use type(x) to see the type of any value.

x = 5
y = 1.234
b1 = True
text = "hello"
c = 1.0 - 2.0j

print(type(x), type(y), type(b1), type(text), type(c))
# -> <class 'int'> <class 'float'> <class 'bool'> <class 'str'> <class 'complex'>

# Complex numbers have .real and .imag parts
print(c.real, c.imag)       # -> 1.0 -2.0

# Strings: single, double or triple quotes.
name1 = 'my name is joey"s tribiani'   # single quotes outside, so " is fine inside
name3 = "my name is joy's x"           # double quotes outside, so ' is fine inside
multi = """This string
spans many lines."""                   # triple quotes allow several lines
print(name1)
print(name3)
print(multi)


# ---------------------------------------------------------------------
# 3. VARIABLES AND DYNAMIC TYPING
# ---------------------------------------------------------------------
# A variable is created by assignment (no need to declare a type).
# A variable is just a LABEL pointing to a value, and the label can be
# moved to a value of a different type ("dynamic typing").

tenth = 10
print(type(tenth))          # -> <class 'int'>
tenth = 15.9
print(type(tenth))          # -> <class 'float'>
tenth = 'ten'
print(type(tenth))          # -> <class 'str'>

# NAMING RULES FOR VARIABLES
# 1. Must not start with a number        (1name  -> error)
# 2. Must not start with a special char  (@name  -> error), except _
# 3. No spaces or dashes; use underscores (my_name)
# 4. Do not reuse Python's built-in names (sum, list, str, len, max...)
#    e.g. "sum = 0" hides the built-in sum() function.
# 5. Names are case-sensitive (age and Age are different)
_str = "ruchik"             # starting with _ is allowed
print(_str)


# ---------------------------------------------------------------------
# 4. TYPE CASTING (changing a value's type)
# ---------------------------------------------------------------------
# IMPLICIT: Python converts automatically (int + float -> float).
z = 5 + 1.234
print(z, type(z))           # -> 6.234 <class 'float'>

# EXPLICIT: you convert with int(), float(), str(), bool()
a = 7
# print("abc" + a)          # [WILL FAIL] TypeError: can only concatenate str to str
print("abc" + str(a))       # -> abc7
print(int("42") + 1)        # -> 43
print(float("3.5"))         # -> 3.5
print(type(str(z)))         # -> <class 'str'>

# Python is STRONGLY typed: it will not silently mix str and int.
# (JavaScript would turn "str" + 1 into "str1" automatically. Python won't.)


# ---------------------------------------------------------------------
# 5. OPERATORS
# ---------------------------------------------------------------------
# ARITHMETIC
a, b = 10, 4
print(a + b)    # -> 14   addition
print(a - b)    # -> 6    subtraction
print(a * b)    # -> 40   multiplication
print(a / b)    # -> 2.5  division (always gives a float)
print(a % b)    # -> 2    modulus (remainder)
print(a ** b)   # -> 10000  power (10 to the power 4)
print(a // b)   # -> 2    floor division (drops the decimal part)

# COMPARISON (result is True or False)
# NOTE:  =  assigns a value,   ==  compares two values
a, b = 5, 7
print(a == b)   # -> False
print(a != b)   # -> True
print(a < b)    # -> True
print(a > b)    # -> False
print(a <= b)   # -> True
print(a >= b)   # -> False

# LOGICAL
p, q = True, False
print(p and q)  # -> False  (both must be True)
print(p or q)   # -> True   (at least one True)
print(not q)    # -> True   (reverses)
print(not p)    # -> False

# ASSIGNMENT SHORTCUTS
n = -5
n += 15         # same as n = n + 15
print(n)        # -> 10
n -= 7          # n = n - 7  -> 3
n *= 3          # n = n * 3  -> 9
print(n)        # -> 9

# IS vs ==
#   ==  compares VALUES
#   is  compares whether both names point to the SAME OBJECT in memory
# Use == to compare values. Use "is" mainly for None:  if x is None
print('a' == 'a')            # -> True
print(True is True)          # -> True
print([1, 2] == [1, 2])      # -> True   (same values)
print([1, 2] is [1, 2])      # -> False  (two different list objects)

# ---------------------------------------------------------------------
# 7. FORMATTING STRINGS (f-string, .format, +)
# ---------------------------------------------------------------------
age = 57
year = 1974
print(f"I am {age} years old, born in {year}")          # f-string (best)
print("I am {} years old, born in {}".format(age, year))  # .format()
print("I am " + str(age) + " years old")                # + needs str()

language = "telugu"      # NOTE: the notebook used 'languageeeee' here but
subject = 'telugu'       # 'language' in format(), which caused a NameError.
print("I love {}, my subject is {}".format(language, subject))
print(f"{3.14159:.2f}")  # -> 3.14  (2 decimal places)


# ---------------------------------------------------------------------
# 8. BRANCHING: if / elif / else
# ---------------------------------------------------------------------
# Python checks conditions from top to bottom and runs the FIRST one that
# is True. Indentation (4 spaces) defines the block. else is optional.
i = 13

if i < 3:
    print("value is less than 3")
    if i < 2:                       # nested if
        print("less than 3 and 2")
elif i < 5:
    print("less than 5")
elif i < 12:
    print("less than 12")
else:
    print("12 or more")             # -> 12 or more

# Truthiness: 0, None, "", [], {} are treated as False; anything else True.
if "hello":
    print("non-empty strings are True")

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# Sum of the numbers in a list
total = 0
for num in numbers:
    total += num          # same as total = total + num
print("sum:", total)      # -> sum: 66
# (The built-in does the same: sum(numbers))

# Loop over the INDEXES with range(len(...))
char = [1, 32, 5]
for idx in range(len(char)):
    print(f" index {idx} has value {char[idx]}")
# Cleaner way when you need both index and value:
for idx, value in enumerate(char):
    print(f" index {idx} has value {value}")

# Looping over a string
s = 'Jimhalpertt'
for letter in s[:3]:
    print(letter)         # J, i, m

# Building a string while looping
names = ["joey", "ruchik", "kota"]
joined = ''
for nm in names:
    joined = joined + ' ' + nm
print(joined)             # ->  joey ruchik kota

# Reversing a string with a loop (add each letter in FRONT)
s = 'chandler'
reversed_s = ''
for letter in s:
    reversed_s = letter + reversed_s
print(reversed_s)       
# ---------------------------------------------------------------------
# 11. RANGE()
# ---------------------------------------------------------------------
# range(stop)               0 up to stop-1
# range(start, stop)        start up to stop-1
# range(start, stop, step)  jump by "step" (can be negative)
# range does not store all numbers in memory; use list() to see them.
print(list(range(5)))           # -> [0, 1, 2, 3, 4]
print(list(range(1, 17, 3)))    # -> [1, 4, 7, 10, 13, 16]
print(list(range(8, -1, -2)))   # -> [8, 6, 4, 2, 0]
print(list(range(2, 25, 5)))    # -> [2, 7, 12, 17, 22]

genre = ['pop', 'pizza', 'jazz', 'swapna', 'joey', 'bing', 'kota']
# Start at the last index and go backwards in steps of 2
for idx in range(len(genre) - 1, -1, -2):
    print("I like", genre[idx])   # kota, joey, jazz, pop


# ---------------------------------------------------------------------
# 12. WHILE LOOP
# ---------------------------------------------------------------------
# A while loop repeats AS LONG AS the condition is True. Use it when you
# don't know in advance how many times to repeat.
# Always change something inside the loop or it runs forever!

n = 5
total = 0          # NOTE: avoid naming this "sum" (it hides the built-in)
i = 1
while i <= n:
    total = total + i
    i = i + 1      # update the counter
print("The sum is", total)    # -> The sum is 15

# Countdown
count = 3
while count >= 0:
    print("Countdown:", count)
    count -= 1
print("happy new year")

# Even numbers 2 to 10
i = 2
while i <= 10:
    print(i)
    i += 2

# Walking through a string with an index
s = 'ruchik'
i = 0
while i < len(s):
    print(s[i])
    i += 1


# ---------------------------------------------------------------------
# 13. BREAK AND CONTINUE
# ---------------------------------------------------------------------
# break    -> stop the whole loop immediately
# continue -> skip the rest of THIS round and go to the next one

for val in "string":
    if val == "i":
        break              # leaves the loop when it meets "i"
    print(val)             # prints s, t, r
print("The end")

for val in "strinnnkig":
    if val == "i":
        continue           # skips "i" but keeps looping
    print(val)             # prints every letter except i
print("The end")

# "Keep asking until the user types the right word" pattern.
# Real version uses input(); here a list of fake answers is used so the
# file runs without waiting.
password = 'stop'
fake_answers = iter(["abc", "hello", "stop"])   # pretend user typing
while True:
    user_input = next(fake_answers)             # real: input("enter your name: ")
    if user_input == password:
        print("name matched, breaking")
        break
    else:
        print("name didn't match... keep entering the names")
