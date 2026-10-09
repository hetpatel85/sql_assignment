import os
import shutil

# ---------------------------------------------------------------------
# SETUP: a working folder for the demo files
# ---------------------------------------------------------------------
# Use os.path.join to build paths (works on Mac, Windows and Linux).
# NOTE: the notebook used paths like "/Users/ruchikkota/Desktop/..." which
# only exist on one computer, so I used a relative folder instead.
FOLDER = "file_demo"
os.makedirs(FOLDER, exist_ok=True)           # exist_ok=True: no error if it exists


def path(name):
    return os.path.join(FOLDER, name)


# ---------------------------------------------------------------------
# 1. FILE MODES  - open(filename, mode)
# ---------------------------------------------------------------------
# | Mode | Meaning                                  | If file missing  |
# |------|------------------------------------------|------------------|
# | "r"  | Read (default)                           | ERROR            |
# | "w"  | Write. ERASES existing content first!    | creates it       |
# | "a"  | Append: add to the end, keep content     | creates it       |
# | "r+" | Read AND write (does not erase)          | ERROR            |
# | "x"  | Create new file, error if it exists      | creates it       |
# Add "b" for binary files (images, pdf): "rb", "wb".

# ---------------------------------------------------------------------
# 2. WRITING A FILE ("w")
# ---------------------------------------------------------------------
# "with open(...) as f" closes the file automatically, even if an error
# happens. Always prefer it over open() + f.close().
# write() does NOT add a new line; you must put \n yourself.
with open(path("sample.txt"), "w") as f:
    f.write("Hello, this is a sample text file.\n")
    f.write("It has multiple lines.\n")
    f.write("hi hello world\n")
    f.write("hello this is python testing file operations commands")

# writelines() writes a list of strings (also without adding \n)
with open(path("lines.txt"), "w") as f:
    f.writelines(["first\n", "second\n", "third\n"])

# ---------------------------------------------------------------------
# 3. READING A WHOLE FILE ("r")
# ---------------------------------------------------------------------
with open(path("sample.txt"), "r") as f:
    content = f.read()                       # the entire file as ONE string
    print("File content:")
    print(content)

# ---------------------------------------------------------------------
# 4. READING LINE BY LINE
# ---------------------------------------------------------------------
# Looping over the file object reads one line at a time (memory-friendly
# for big files). Each line still ends with \n, so use .strip().
with open(path("sample.txt"), "r") as f:
    for line in f:
        print("Line:", line.strip())

# ---------------------------------------------------------------------
# 5. OVERWRITING vs APPENDING
# ---------------------------------------------------------------------
# "w" wipes the file. Each time the notebook ran "w", the old text was lost.
with open(path("example.txt"), "w") as f:
    f.write('this is boring sessions\n')     # the notebook had no \n here,
                                             # which glued the next line on

# "a" adds to the END without erasing.
with open(path("example.txt"), "a") as f:
    f.write("Line 5: This is appended.\n")
    f.write("Line 6: This is python session 5\n")

with open(path("example.txt"), "r") as f:
    print(f.read())
# -> this is boring sessions
# -> Line 5: This is appended.
# -> Line 6: This is python session 5

# ---------------------------------------------------------------------
# 6. READ ONLY PART OF A FILE
# ---------------------------------------------------------------------
# read(n) reads n CHARACTERS from the current position.
with open(path("example.txt"), "r") as f:
    print("First 10 characters:", f.read(10))    # -> this is bo
# (The notebook used read(56) while the comment said "first 10". Match the
#  number to what you want.)

# readline() reads ONE line each time it is called.
with open(path("example.txt"), "r") as f:
    print("Line 1:", f.readline().strip())
    print("Line 2:", f.readline().strip())
    print("Line 3:", f.readline().strip())

# readlines() returns ALL lines as a LIST of strings.
with open(path("example.txt"), "r") as f:
    lines = f.readlines()
    print(lines)
    # -> ['this is boring sessions\n', 'Line 5: This is appended.\n', 'Line 6: This is python session 5\n']
    print(len(lines), "lines")                   # -> 3 lines

# Get the Nth line (here the 3rd): skip N-1 lines, then read one
t = 3
with open(path("example.txt"), "r") as f:
    for _ in range(t - 1):
        f.readline()
    third = f.readline()
print(third.strip())                             # -> Line 6: This is python session 5

# ---------------------------------------------------------------------
# 7. COPYING A FILE
# ---------------------------------------------------------------------
# Open the source for reading and one or more targets for writing at once.
with open(path("example.txt"), "r") as src, \
        open(path("copy_sample.txt"), "w") as dest, \
        open(path("copy_sample1.txt"), "w") as dest1:
    for line in src:
        dest.write(line)
        dest1.write(line)

with open(path("copy_sample.txt"), "r") as f:
    print("Copy content:")
    print(f.read())
# Shortcut for a plain copy:  shutil.copy(source, destination)

# ---------------------------------------------------------------------
# 8. THE FILE POINTER: seek() and tell()
# ---------------------------------------------------------------------
# A file has a "cursor". read/write start at the cursor and move it.
#   f.tell()      -> current cursor position (in bytes)
#   f.seek(n)     -> move the cursor to position n
#   f.seek(0)     -> go back to the start (to read again)
with open(path("sample.txt"), "r") as f:
    print(f.read(5))             # -> Hello
    print(f.tell())              # -> 5
    f.seek(0)
    print(f.read(5))             # -> Hello  (read again from the start)

# ---------------------------------------------------------------------
# 9. "r+" MODE: read and write, WITHOUT erasing
# ---------------------------------------------------------------------
# Writing in the middle OVERWRITES the characters that are there; it does
# not insert. That is what happened in the notebook with seek(35).
with open(path("demo_rplus.txt"), "w") as f:
    f.write("0123456789")

with open(path("demo_rplus.txt"), "r+") as f:
    f.seek(3)
    f.write("AB")                # replaces the characters at positions 3 and 4
with open(path("demo_rplus.txt"), "r") as f:
    print(f.read())              # -> 012AB56789

# ---------------------------------------------------------------------
# 10. CHECKING, LISTING AND DELETING FILES  (os module)
# ---------------------------------------------------------------------
print(os.path.exists(path("sample.txt")))        # -> True
print(os.path.exists(path("nope.txt")))          # -> False
print(os.path.getsize(path("sample.txt")), "bytes")
print(sorted(os.listdir(FOLDER)))                # files inside the folder
print(os.getcwd())                               # current working directory

# Safe way to read a file that might not exist
try:
    with open(path("nope.txt"), "r") as f:
        f.read()
except FileNotFoundError:
    print("File not found, handled safely")

# Delete a file (permanent! it does NOT go to the recycle bin)
if os.path.exists(path("copy_sample1.txt")):
    os.remove(path("copy_sample1.txt"))

# ---------------------------------------------------------------------
# 11. EXCEL FILES (.xlsx) WITH PANDAS
# ---------------------------------------------------------------------
# Needs:  pip install pandas openpyxl
# DataFrame = a table (rows and columns).
try:
    import pandas as pd

    data = {
        "Name": ["Alice", "Bob", "Charlie", "ruchik", "sushma"],
        "Marks": [85, 90, 78, 87, 11],
    }
    df = pd.DataFrame(data)

    df.to_excel(path("students.xlsx"), index=False)   # index=False: no 0,1,2.. column
    df_read = pd.read_excel(path("students.xlsx"))
    print("Data from Excel:")
    print(df_read)

    # CSV works the same way (and needs no extra package):
    df.to_csv(path("students.csv"), index=False)
    print(pd.read_csv(path("students.csv")).head(3))   # first 3 rows
    # NOTE: the notebook had typos in comments: pd.readcsc() should be pd.read_csv()
except ImportError as err:
    print("Skipping the Excel/CSV demo, a package is missing:", err)
    print("Install with: pip install pandas openpyxl")

# ---------------------------------------------------------------------
# 12. CSV WITHOUT PANDAS (built-in csv module)
# ---------------------------------------------------------------------
import csv

with open(path("people.csv"), "w", newline="") as f:     # newline="" avoids blank rows on Windows
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["Joey", 30])
    writer.writerow(["Chandler", 32])

with open(path("people.csv"), "r") as f:
    for row in csv.reader(f):
        print(row)                # -> ['name', 'age'] ... each row is a list of strings

# ---------------------------------------------------------------------
# CLEAN UP (delete the demo folder)
# ---------------------------------------------------------------------
CLEAN_UP = True
if CLEAN_UP:
    shutil.rmtree(FOLDER)          # deletes the folder and everything in it
    print("Demo folder removed")
