# =====================================================================
# 1. VARIABLES AND ARITHMETIC OPERATORS
# =====================================================================
# A variable is just a named box that holds a value. Python figures
# out the TYPE of the value automatically (int, float, str, etc.) --
# you never have to declare the type yourself like in some languages.

a = 10          # int  (a whole number)
b = 3           # int
name = "Alex"   # str  (text, always in quotes)
price = 4.99    # float (a number with decimals)

print("a =", a)
print("b =", b)

# Arithmetic operators -- these work the same way as basic math class,
# with a couple of Python-specific extras:
print("Addition:       a + b =", a + b)    # 13
print("Subtraction:    a - b =", a - b)    # 7
print("Multiplication: a * b =", a * b)    # 30
print("Division:       a / b =", a / b)    # 3.333... (ALWAYS returns a float)

# =====================================================================
# 2. TYPE CASTING (converting one type into another)
# =====================================================================
# Type casting means manually converting a value from one type to
# another using a built-in function: int(), float(), str(), bool().
# This matters a LOT with user input, since input() always returns
# text (str) even if the user types a number -- see Section 5.

# --- Type cast #1: string -> int (and int -> string) ---
num_as_text = "25"           # this is a STRING, not a number, even though it looks like one
num_as_text_type = type(num_as_text)
print("Before casting, type is:", num_as_text_type)   # <class 'str'>

num_as_int = int(num_as_text)   # now it's a real number
print("After casting, type is:", type(num_as_int))     # <class 'int'>
print("Now we can do math with it:", num_as_int + 5)    # 30

# Going the other direction: int -> string (useful when combining
# numbers with text in a single message)
score = 95
message = "Your score is " + str(score)   # str() converts 95 into "95"
print(message)
# NOTE: print("Your score is " + score) would CRASH -- you cannot
# combine a string and an int with + unless you first cast the int
# to a string. Try removing str() below to see the error yourself:
# message_broken = "Your score is " + score

# --- Type cast #2: string -> float (and float -> int) ---
price_as_text = "19.99"
price_as_float = float(price_as_text)
print("Price as a float:", price_as_float, "| type:", type(price_as_float))

# float -> int: this does NOT round -- it just CHOPS OFF the decimal part
pi_ish = 3.99
pi_as_int = int(pi_ish)
print("3.99 cast to int becomes:", pi_as_int)   # 3, NOT 4 -- int() truncates, it never rounds


# =====================================================================
# 2a. DYNAMIC TYPING (Python variables can change type on the fly)
# =====================================================================
# Python is "dynamically typed," which means a variable is NOT locked
# into one type forever. The SAME variable name can hold an int, then
# later hold a string, then later hold a float -- Python just looks at
# whatever value is CURRENTLY assigned and figures out the type live,
# every time. (This is different from languages like Java or C, where
# you must declare a variable's type up front and it can never change.)

data = 10                          # right now, data is an int
print(f"data = {data}, type = {type(data)}")

data = "now I'm text"              # SAME variable, completely different type -- totally legal
print(f"data = {data}, type = {type(data)}")

data = 3.14                        # now it's a float
print(f"data = {data}, type = {type(data)}")

data = True                        # now it's a boolean
print(f"data = {data}, type = {type(data)}")

# WHY THIS MATTERS: it's convenient, but it also means Python won't
# warn you in advance if you accidentally reuse a variable name for
# something totally different later in a long program -- there's no
# safety net catching "wait, that used to be a number!" It's on YOU
# to keep track of what a variable currently holds, especially in
# longer scripts.

# You can always check what type something is RIGHT NOW using type():
mystery_value = input("Type anything: ")   # input() ALWAYS gives back a string
print(f"Whatever you typed is currently of type: {type(mystery_value)}")
# Even if you typed "42", it prints <class 'str'> here -- proof that
# input() never gives you a number automatically; YOU decide when to
# cast it, as we practiced in Section 2.


# =====================================================================
# 2b. F-STRINGS (formatted string literals)
# =====================================================================
# Earlier in Section 2, we combined text and numbers like this:
#     message = "Your score is " + str(score)
# That works, but it's clunky -- you have to manually str() every
# number, and it gets messy with multiple values. F-strings fix this.
#
# An f-string is written as f"..." (a lowercase f right before the
# quotes). Inside the quotes, anything wrapped in { } is treated as
# real Python code and automatically converted to text for you --
# NO manual str() casting needed, even for numbers.

score = 95
name = "Alex"

# The old way (from Section 2):
message_old = "Your score is " + str(score)

# The f-string way -- cleaner, and no casting required:
message_new = f"Your score is {score}"
print(message_new)

# You can put MULTIPLE variables in one f-string:
print(f"Hello {name}, your score is {score}.")

# You can even put small expressions/math directly inside { }:
print(f"Next year you'll be {score + 1} points closer to 100.")

# F-strings also support formatting numbers, e.g. controlling decimal
# places -- very useful for prices/percentages:
price = 19.98765
print(f"The price is ${price:.2f}")   # .2f = round to exactly 2 decimal places -> $19.99

percent = 0.4567
print(f"That's {percent:.1%} complete")   # .1% = show as a percentage with 1 decimal -> 45.7%

# From here on, we'll prefer f-strings over + concatenation, since
# it's the standard, more readable way modern Python code is written.


# =====================================================================
# 3. BOOLEANS AND COMPARISON OPERATORS
# =====================================================================
# A boolean is a value that's either True or False -- nothing else.
# You get booleans back whenever you use a COMPARISON operator.

x = 7
y = 10

print("x == y :", x == y)   # equal to?           -> False
print("x != y :", x != y)   # not equal to?        -> True
print("x > y  :", x > y)    # greater than?        -> False
print("x < y  :", x < y)    # less than?           -> True
print("x >= 7 :", x >= 7)   # greater than or equal -> True
print("x <= 7 :", x <= 7)   # less than or equal    -> True

# You can combine multiple booleans using and / or / not:
is_adult = True
has_ticket = False
print("Can enter (needs BOTH):", is_adult and has_ticket)   # False, because has_ticket is False
print("Can enter (needs EITHER):", is_adult or has_ticket)  # True, because is_adult alone is True
print("Opposite of is_adult:", not is_adult)                # False


# =====================================================================
# 4. IF / ELIF / ELSE
# =====================================================================
# This is how Python makes decisions. Only ONE branch runs -- Python
# checks each condition top to bottom and stops at the FIRST one that's
# True. If none are True, it falls through to else (if you provided one).

age = 20

if age < 13:
    print("You are a child.")
elif age < 20:              # only checked if the FIRST condition was False
    print("You are a teenager.")
elif age < 65:              # only checked if BOTH earlier conditions were False
    print("You are an adult.")
else:                       # runs only if NONE of the above were True
    print("You are a senior.")

# Try changing 'age' above to 10, 16, 40, and 70, and re-run this
# block each time -- notice how only ONE message ever prints.


# =====================================================================
# 5. USER INPUT
# =====================================================================
# input() pauses the program and waits for the person to type
# something, then returns whatever they typed AS A STRING -- always,
# even if they type numbers. This is why type casting (Section 2)
# matters so much here.

user_name = input("What is your name? ")
print("Hello, " + user_name + "!")

# Getting a NUMBER from the user requires casting the input() result:
age_text = input("How old are you? ")   # this is a STRING right now, e.g. "20"
age_number = int(age_text)              # NOW it's a real number we can do math with
print("Next year you will be", age_number + 1)

# You can combine input() + casting + if/elif/else all together:
favorite_number_text = input("Enter your favorite number: ")
favorite_number = int(favorite_number_text)

if favorite_number % 2 == 0:
    print(favorite_number, "is even.")
else:
    print(favorite_number, "is odd.")


# =====================================================================
# 6. LOOPS
# =====================================================================

# --- FOR loop ---
# Use a for loop when you know how many times you want to repeat
# something, or you're going through a known sequence/range.
print("\n--- For Loop Example ---")
for i in range(5):              # range(5) produces 0, 1, 2, 3, 4 (5 numbers, starting at 0)
    print("For loop count:", i)

# range(start, stop) lets you control the starting point too:
print("\n--- For Loop with a custom range ---")
for i in range(1, 6):           # produces 1, 2, 3, 4, 5 (stops BEFORE 6)
    print("Counting:", i)

# --- WHILE loop ---
# Use a while loop when you don't know in advance how many times
# you'll repeat -- it just keeps going AS LONG AS the condition is True.
print("\n--- While Loop Example ---")
count = 0
while count < 5:
    print("While loop count:", count)
    count = count + 1   # IMPORTANT: without this line, count never
                         # changes, the condition is always True, and
                         # the loop runs FOREVER (an "infinite loop")

# A practical while loop example: keep asking until the user gives a
# valid answer.
print("\n--- While Loop with User Input ---")
password = ""
while password != "letmein":
    password = input("Enter the password (hint: 'letmein'): ")
print("Access granted!")