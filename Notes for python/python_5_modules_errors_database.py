# =====================================================================
# PART A: MODULES AND LIBRARIES
# =====================================================================
# A MODULE is a Python file (.py) containing functions/variables you can
# reuse. A LIBRARY/PACKAGE is a collection of modules.
# Import styles:
#   import math                 -> use as math.sqrt(16)
#   from math import sqrt       -> use as sqrt(16)
#   import math as m            -> use as m.sqrt(16)
#   from math import *          -> imports everything (avoid: name clashes)
# A module runs only ONCE, the first time it is imported (it is cached).
# "Standard library" modules come with Python (no install needed).
# Third-party ones are installed with  pip install <name>.

# ---------------------------------------------------------------------
# math
# ---------------------------------------------------------------------
import math

print(math.ceil(25.7))        # -> 26   round UP
print(math.floor(25.7))       # -> 25   round DOWN
print(math.sqrt(16))          # -> 4.0
print(math.factorial(5))      # -> 120  (5*4*3*2*1)
print(math.pi)                # -> 3.141592653589793
print(math.pow(2, 3))         # -> 8.0
print(math.gcd(12, 18))       # -> 6

# ---------------------------------------------------------------------
# random
# ---------------------------------------------------------------------
import random

print(random.randint(1, 10))             # random integer from 1 to 10 (both included)
print(random.choice(['a', 'b', 'c']))    # one random item from a list
nums = [1, 2, 3, 4, 5]
random.shuffle(nums)                     # shuffles the list in place
print(nums)
print(random.random())                   # random float from 0.0 to 1.0

# ---------------------------------------------------------------------
# datetime
# ---------------------------------------------------------------------
from datetime import datetime, timedelta

now = datetime.now()
# strftime formats a date: %Y year, %m month, %d day, %H hour, %M minute, %S second
print("Current Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("Tomorrow:", (now + timedelta(days=1)).strftime("%Y-%m-%d"))

# ---------------------------------------------------------------------
# os  (talk to the operating system)
# ---------------------------------------------------------------------
import os

print(os.getcwd())                 # current working directory
print(len(os.listdir()), "items in this folder")   # list files in the folder
print(os.path.join("folder", "file.txt"))          # build a path safely

# ---------------------------------------------------------------------
# sys  (information about Python itself)
# ---------------------------------------------------------------------
import sys

print(sys.version)                 # Python version
print(sys.path[:2])                # folders Python searches when you import

# ---------------------------------------------------------------------
# statistics
# ---------------------------------------------------------------------
import statistics

data = [10, 20, 30, 40, 50, 70]
print(statistics.mean(data))       # -> 36.666666666666664   (average)
print(statistics.median(data))     # -> 35.0   (middle; average of 30 and 40)
print(statistics.mode([1, 2, 2, 3]))   # -> 2  (most frequent)

# ---------------------------------------------------------------------
# EXPLORING A MODULE: dir() and help()
# ---------------------------------------------------------------------
# dir(module)     lists everything inside the module
# help(function)  shows the documentation for it
print([name for name in dir(math) if not name.startswith('_')][:8])
# -> ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'cbrt']
help(math.floor)
# -> Help on built-in function floor in module math: floor(x, /) Return the floor of x ...
# =====================================================================
# PART B: ERRORS AND EXCEPTION HANDLING
# =====================================================================
# Two kinds of error:
#   Syntax error : the code is written wrongly, Python cannot even start.
#   Exception    : the code is valid but fails WHILE running
#                  (dividing by zero, missing file, wrong type...).
# An unhandled exception stops the program. try/except lets you handle it
# and keep going.
#
# Common exceptions:
#   ZeroDivisionError   10 / 0
#   ValueError          int("abc")
#   TypeError           "a" + 1
#   NameError           using a variable that doesn't exist
#   IndexError          [1, 2][5]
#   KeyError            {'a': 1}['b']
#   FileNotFoundError   open("missing.txt")
#   ModuleNotFoundError import something_not_installed
#   io.UnsupportedOperation  writing to a file opened with "r"

# ---------------------------------------------------------------------
# try / except / else / finally
# ---------------------------------------------------------------------
#   try:      code that might fail
#   except X: runs if error X happens
#   else:     runs only if NO error happened
#   finally:  ALWAYS runs (cleanup: closing files, connections...)

# A bare "except:" catches everything. Fine to learn, but in real code name
# the exception, otherwise you can hide real bugs (and even Ctrl+C).
try:
    printf(Hello)                # NameError: neither printf nor Hello exists
except:
    print('something went wrong')       # -> something went wrong

# Catch a SPECIFIC error and read its message
try:
    print(10 / 0)
except ZeroDivisionError as e:
    print("Error:", e)                  # -> Error: division by zero

# Several except blocks (the first matching one runs)
for value in ["12", "abc", "0"]:
    try:
        print(100 / int(value))
    except ValueError:
        print(f"{value!r} is not a number")
    except ZeroDivisionError:
        print("can't divide by zero")
# -> 8.333333333333334 / 'abc' is not a number / can't divide by zero

# Catch several types in one line
try:
    int("x")
except (ValueError, TypeError) as e:
    print("bad input:", e)

# else + finally with files
try:
    f = open('testfile.txt', 'w')
    f.write('Test write this')
except IOError:
    print("Error: Could not find file or read data")
else:
    print("Content written successfully")      # runs only if the try worked
    f.close()
finally:
    print("Always executes (success or error)")

# Opening in read mode and then writing causes an error:
try:
    f = open('testfile.txt', 'r')
    f.write('Test write this')                 # not allowed in "r" mode
except IOError:
    # io.UnsupportedOperation is a kind of IOError, so this catches it
    print("Error: you are opening the file in read mode and writing data")
finally:
    f.close()
os.remove('testfile.txt')

# Raising your own errors with raise


def set_age(age):
    if age < 0:
        raise ValueError("age cannot be negative")
    return age


try:
    set_age(-5)
except ValueError as e:
    print("Caught:", e)                        # -> Caught: age cannot be negative

# ---------------------------------------------------------------------
# Asking the user until they type a valid integer
# ---------------------------------------------------------------------
# Notebook problem: the first version did only ONE check and the variable
# "val" did not exist after a failure (printing it gave an error).
# Solution: a while loop that repeats until the conversion works.
# Real version uses input(); here fake answers are used so the file runs
# without waiting. Replace  next(answers)  with  input("Please enter an integer: ")


def ask_int(answers):
    while True:
        try:
            val = int(next(answers))      # real: int(input("Please enter an integer: "))
        except ValueError:
            print("Looks like you did not enter an integer!")
        else:
            return val                    # valid input: leave the loop
        finally:
            print("Finally, I executed!") # runs on every attempt


print(ask_int(iter(["isdj", "4"])))
# -> Looks like you did not enter an integer!
# -> Finally, I executed!
# -> Finally, I executed!
# -> 4