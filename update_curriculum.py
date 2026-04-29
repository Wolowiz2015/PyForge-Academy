import re

with open("pyforge/curriculum.py", "r", encoding="utf-8") as f:
    content = f.read()

new_lessons = """
    # =====================================================================
    # OFFICIAL PYTHON TUTORIAL TRACK
    # =====================================================================
    _l("T.1", "Whetting Your Appetite & The Interpreter", "Official Tutorial", 10,
       '''
# 1. Whetting Your Appetite & 2. Using the Python Interpreter

Python is an interpreted, high-level, general-purpose programming language. It lets you work quickly and integrate systems more effectively.

## Invoking the Interpreter
You can start the Python interpreter by typing `python` in your terminal.
- **Argument Passing:** When known to the interpreter, the script name and additional arguments are passed to the script in the variable `sys.argv`.
- **Interactive Mode:** When started without a script, Python acts as a REPL (Read-Eval-Print Loop).
- **Source Code Encoding:** By default, Python source files are treated as encoded in UTF-8.
''',
       '''
import sys
print("Interpreter version:", sys.version.split()[0])
print("Arguments passed:", sys.argv)
''',
       "Import the sys module and store the executable path in `py_path`.",
       '''import sys; assert _vars.get("py_path") == sys.executable''',
       None, ["interpreter", "sys"]),

    _l("T.3", "An Informal Introduction to Python", "Official Tutorial", 15,
       '''
# 3. An Informal Introduction to Python

## Using Python as a Calculator
- **Numbers:** The interpreter acts as a simple calculator. It supports `int` and `float`. Division (`/`) always returns a float. Use `//` for floor division.
- **Text:** Strings can be enclosed in single quotes (`'...'`) or double quotes (`"..."`). Strings are immutable sequences.
- **Lists:** Python knows a number of compound data types. The most versatile is the list, written as comma-separated values between square brackets. Lists are mutable.

## First Steps Towards Programming
You can use `while` loops for initial programming tasks, like generating the Fibonacci series.
''',
       '''
# Numbers
a, b = 5, 2
print("Division:", a / b, "Floor:", a // b)

# Text
word = "Python"
print(word[0:2])

# Lists
squares = [1, 4, 9, 16]
squares.append(25)
print(squares)
''',
       "Create a list of the first three even numbers (2, 4, 6) and assign it to `evens`.",
       '''assert _vars.get("evens") == [2, 4, 6]''',
       "list", ["numbers", "strings", "lists"]),

    _l("T.4", "More Control Flow Tools", "Official Tutorial", 25,
       '''
# 4. More Control Flow Tools

Python provides standard control flow tools with a very readable syntax.

- **if Statements:** Conditional execution.
- **for Statements:** Iterates over items of any sequence.
- **The range() Function:** Generates arithmetic progressions.
- **break, continue, else:** `break` breaks out of the innermost enclosing loop. `continue` continues with the next iteration. Loop `else` clauses run when the loop exhausts naturally.
- **pass Statements:** Does nothing. Used syntactically when a statement is required.
- **match Statements:** Structural pattern matching (Python 3.10+).

## Defining Functions
Functions are defined using the `def` keyword.
- **Default Argument Values, Keyword Arguments.**
- **Special Parameters:** Positional-only (`/`), Keyword-only (`*`).
- **Arbitrary Argument Lists:** `*args` and `**kwargs`.
- **Lambda Expressions:** Small anonymous functions created with the `lambda` keyword.
- **Documentation Strings & Annotations:** Docstrings document functions, annotations provide type hints.
''',
       '''
def ask_ok(prompt, retries=4, reminder='Please try again!'):
    print(prompt, "retries:", retries)

ask_ok("Do you really want to quit?")

# Lambda example
make_incrementor = lambda n: lambda x: x + n
f = make_incrementor(42)
print("Lambda result:", f(0))
''',
       "Define a function `add(a, b)` that returns a + b.",
       '''assert add(5, 5) == 10''',
       "call-stack", ["control-flow", "functions", "lambda"]),

    _l("T.5", "Data Structures", "Official Tutorial", 20,
       '''
# 5. Data Structures

## More on Lists
Lists have methods like `.append()`, `.extend()`, `.insert()`, `.remove()`, `.pop()`, `.clear()`, `.index()`, `.count()`, `.sort()`, and `.reverse()`.
- **Stacks & Queues:** Lists can be used as stacks (LIFO) easily. For queues (FIFO), use `collections.deque`.
- **List Comprehensions:** A concise way to create lists.

## The del Statement
Removes an item from a list given its index instead of its value.

## Tuples and Sequences
Tuples are immutable sequences, usually containing a heterogeneous sequence of elements.

## Sets
Sets are unordered collections with no duplicate elements.

## Dictionaries
Associative arrays or hash maps indexed by keys.

## Looping Techniques
Use `items()` for dicts, `enumerate()` for sequences, `zip()` for looping over multiple sequences.
''',
       '''
# Comprehension
squares = [x**2 for x in range(5)]
print(squares)

# Dictionary looping
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print(k, v)
''',
       "Create a set containing 1, 2, 3 and assign it to `my_set`.",
       '''assert _vars.get("my_set") == {1, 2, 3}''',
       "dict", ["lists", "tuples", "sets", "dictionaries"]),

    _l("T.6", "Modules and Packages", "Official Tutorial", 15,
       '''
# 6. Modules

A module is a file containing Python definitions and statements. The file name is the module name with the suffix `.py` appended.

- **Executing modules as scripts:** `python -m module_name`.
- **The Module Search Path:** Python searches `sys.path`.
- **Standard Modules:** Built-in modules like `sys`, `math`.
- **The dir() Function:** Used to find out which names a module defines.

## Packages
Packages are a way of structuring Python's module namespace by using "dotted module names".
- `__init__.py` files are required to make Python treat directories containing the file as packages.
- You can use absolute or relative imports.
''',
       '''
import math
import sys

print("Pi is:", math.pi)
print("Paths:", sys.path[:2])
''',
       "Use the `dir()` function on the `math` module and store the result in `math_dir`.",
       '''import math; assert _vars.get("math_dir") == dir(math)''',
       None, ["modules", "packages", "import"]),

    _l("T.7", "Input and Output", "Official Tutorial", 15,
       '''
# 7. Input and Output

## Fancier Output Formatting
- **Formatted String Literals (f-strings):** `f"Value is {val}"`.
- **The String format() Method:** `"Value is {}".format(val)`.
- **Manual String Formatting:** Using `str.rjust()`, `str.ljust()`.

## Reading and Writing Files
- `open()` returns a file object. It's good practice to use the `with` keyword when dealing with file objects.
- **Methods of File Objects:** `read()`, `readline()`, `readlines()`, `write()`.
- **Saving structured data with json:** The `json` standard module can take Python data hierarchies, and convert them to string representations.
''',
       '''
import json

data = {"name": "PyForge", "version": 1.0}
json_str = json.dumps(data)
print("JSON:", json_str)

# Formatting
year = 2026
event = 'Release'
print(f'Results of the {year} {event}')
''',
       "Format the string 'Hello, Python!' using an f-string and store it in `greeting`.",
       '''assert _vars.get("greeting") == "Hello, Python!"''',
       None, ["io", "json", "formatting"]),

    _l("T.8", "Errors and Exceptions", "Official Tutorial", 15,
       '''
# 8. Errors and Exceptions

- **Syntax Errors:** Parsing errors.
- **Exceptions:** Errors detected during execution.
- **Handling Exceptions:** Use `try`...`except` blocks.
- **Raising Exceptions:** The `raise` statement allows the programmer to force a specified exception to occur.
- **Exception Chaining:** `raise ... from ...`
- **User-defined Exceptions:** Create classes inheriting from `Exception`.
- **Clean-up Actions:** The `finally` clause executes under all circumstances.
- **Exception Groups:** (Python 3.11+) `ExceptionGroup` and `except*`.
''',
       '''
try:
    x = 1 / 0
except ZeroDivisionError as err:
    print("Handling run-time error:", err)
finally:
    print("Cleanup executed.")
''',
       "Write a try/except block that catches a TypeError when adding 1 + '1' and stores True in `caught`.",
       '''assert _vars.get("caught") is True''',
       None, ["exceptions", "errors"]),

    _l("T.9", "Classes", "Official Tutorial", 20,
       '''
# 9. Classes

Classes provide a means of bundling data and functionality together.

- **Python Scopes and Namespaces:** A namespace is a mapping from names to objects.
- **Class Definition Syntax & Objects:** Classes support instantiation and attribute references.
- **Instance Objects & Method Objects:** Methods are functions attached to objects.
- **Class and Instance Variables:** Instance variables are for data unique to each instance.
- **Inheritance & Multiple Inheritance:** Derived classes override methods of their base classes.
- **Private Variables:** Denoted by a single leading underscore (convention) or double leading underscore (name mangling).
- **Iterators & Generators:** `__iter__()` and `__next__()` protocols. Generators use `yield`.
''',
       '''
class Dog:
    kind = 'canine'         # class variable

    def __init__(self, name):
        self.name = name    # instance variable

d = Dog('Fido')
e = Dog('Buddy')
print(d.name, d.kind)
''',
       "Create a class `Cat` with an `__init__` that takes and stores a `name`.",
       '''assert Cat("Whiskers").name == "Whiskers"''',
       "object", ["classes", "oop"]),

    _l("T.10", "Brief Tour of the Standard Library", "Official Tutorial", 20,
       '''
# 10 & 11. The Standard Library

Python comes with a "Batteries Included" philosophy.

- **OS Interface (`os`, `shutil`)**
- **File Wildcards (`glob`)**
- **Command Line Arguments (`sys.argv`, `argparse`)**
- **Mathematics (`math`, `random`, `statistics`)**
- **Internet Access (`urllib.request`)**
- **Dates and Times (`datetime`)**
- **Data Compression (`zlib`, `gzip`)**
- **Performance Measurement (`timeit`, `profile`)**
- **Output Formatting (`reprlib`, `pprint`)**
- **Templating (`string.Template`)**
- **Multi-threading (`threading`)**
- **Logging (`logging`)**
- **Decimal Floating Point (`decimal`)**
''',
       '''
import random
import datetime

print("Random choice:", random.choice(['apple', 'pear', 'banana']))
print("Current date:", datetime.date.today())
''',
       "Import `random` and assign a random float between 0 and 1 using `random.random()` to `r_val`.",
       '''import random; assert 0 <= _vars.get("r_val", -1) <= 1''',
       None, ["stdlib", "modules"]),

    _l("T.12", "Virtual Environments and Packages", "Official Tutorial", 10,
       '''
# 12. Virtual Environments and Packages

Python applications will often use packages and modules that don't come as part of the standard library.

- **Creating Virtual Environments:** Use the `venv` module. `python -m venv tutorial-env`.
- **Activating:** `tutorial-env\\Scripts\\activate` (Windows) or `source tutorial-env/bin/activate` (Unix).
- **Managing Packages with pip:** `pip install`, `pip uninstall`, `pip freeze > requirements.txt`.
''',
       '''
# Shell commands (not Python):
# python -m venv myenv
# myenv\\Scripts\\activate
# pip install requests
print("Virtual environments keep dependencies isolated per project!")
''',
       "Assign the string 'isolated' to the variable `venv_purpose`.",
       '''assert _vars.get("venv_purpose") == "isolated"''',
       None, ["venv", "pip"]),

    _l("T.14", "Advanced Topics & Appendix", "Official Tutorial", 10,
       '''
# 14, 15, 16. Advanced Topics & Appendix

- **Interactive Input Editing:** Modern Python interpreters support tab completion and history editing out of the box (via `readline` or `pyreadline`).
- **Floating-Point Arithmetic: Issues and Limitations:** Float precision issues exist because floats are represented in base 2. `0.1 + 0.2` is not exactly `0.3`.
- **Appendix (Interactive Mode):** Startup files, customization modules, and error handling specifics in the REPL.
''',
       '''
print("Float precision issue:")
print("0.1 + 0.2 =", 0.1 + 0.2)
print("Is 0.1 + 0.2 == 0.3?", 0.1 + 0.2 == 0.3)

from decimal import Decimal
print("Using Decimal:", Decimal('0.1') + Decimal('0.2') == Decimal('0.3'))
''',
       "Import Decimal from decimal and store Decimal('0.1') in `d_val`.",
       '''from decimal import Decimal; assert _vars.get("d_val") == Decimal('0.1')''',
       None, ["floats", "advanced"]),
"""

# Insert before the last closing bracket ]
pos = content.rfind("]")
if pos != -1:
    content = content[:pos] + new_lessons + content[pos:]
    with open("pyforge/curriculum.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Curriculum updated.")
else:
    print("Could not find end of CURRICULUM array.")
