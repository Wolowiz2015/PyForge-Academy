"""
Curriculum content for PyForge Academy.

Every lesson is a self-contained dict with:
  - id, title, level, estimated_minutes
  - theory: markdown-flavored explanation
  - example: runnable code shown in the editor
  - exercise: a task with a starter snippet and a check function (in `assert_code`)
  - viz: optional visualization hint string consumed by the visualizer
  - tags: searchable keywords

Tracks are organized as: Foundations -> Core -> Data Structures -> OOP ->
Functional & Iterators -> Async & Concurrency -> Stdlib Power Tools ->
Data Science -> Web & APIs -> Testing & Tooling -> Performance ->
AI & LLMs -> Capstone Projects.

This module ships the curriculum as an in-memory dict so the app has zero
external content dependencies on first launch. Lessons can later be moved
to a content CMS for live updates.
"""

from typing import List, Dict, Any


def _l(lid, title, level, minutes, theory, example, exercise=None,
       assert_code=None, viz=None, tags=None) -> Dict[str, Any]:
    """Helper to build a lesson dict."""
    return {
        "id": lid,
        "title": title,
        "level": level,
        "minutes": minutes,
        "theory": theory.strip(),
        "example": example.strip("\n"),
        "exercise": (exercise or "").strip(),
        "assert_code": (assert_code or "").strip(),
        "viz": viz,
        "tags": tags or [],
    }


CURRICULUM: List[Dict[str, Any]] = [

    # ---------------------------------------------------------------- 0. Welcome
    _l("0.1", "Welcome to PyForge Academy", "Onboarding", 3,
       """
# Welcome

PyForge teaches Python the way real engineers learn it: **read theory, run code,
visualize what's happening in memory, then build something**. Every lesson has:

- A short concept explanation
- A runnable example
- An exercise auto-checked against the goal
- Optional visualization to *see* what the bytes are doing
- An on-call AI tutor (Mistral via Ollama) for free-form questions

Press **▶ Run** on any code panel to execute it locally. Press **🧠 Visualize**
when available. Open the AI panel on the right whenever you're stuck.
""",
       """
print("Welcome to PyForge Academy")
print("Press Run to execute this snippet.")
""",
       "Change the message to print your own name.",
       """assert "Tharchen" in _stdout or len(_stdout.strip()) > 0""",
       None, ["intro"]),

    # ---------------------------------------------------------------- Foundations
    _l("1.1", "Variables & Types", "Foundations", 8,
       """
# Variables & Types

A **variable** is a name bound to an object in memory. Python is *dynamically
typed* — the variable doesn't have a type, the *object* does.

Core built-in types:
- `int`, `float` — numbers
- `str` — text (immutable)
- `bool` — True / False
- `list`, `tuple`, `dict`, `set` — collections
- `None` — absence of a value

Use `type(x)` to inspect, `isinstance(x, T)` to check.
""",
       """
name = "Tharchen"
age = 28
height = 1.74
is_engineer = True

print(name, type(name))
print(age, type(age))
print(height, type(height))
print(is_engineer, type(is_engineer))
""",
       "Create a variable `country` set to your country and print its type.",
       """assert 'country' in _vars and isinstance(_vars['country'], str)""",
       "memory", ["variables", "types", "basics"]),

    _l("1.2", "Strings — slicing & f-strings", "Foundations", 10,
       """
# Strings

Strings are **immutable sequences of Unicode code points**. You can:

- Index: `s[0]`
- Slice: `s[1:5]`, `s[::-1]` (reverse)
- Format with f-strings: `f"Hello {name}, you are {age}"`
- Use methods: `.upper()`, `.split()`, `.strip()`, `.replace()`

Slicing never raises `IndexError` — it returns whatever fits.
""",
       """
text = "PyForge Academy"
print(text[0])
print(text[:7])
print(text[::-1])
print(text.upper())
print(text.split())

name = "Mistral"
print(f"AI assistant: {name}, length={len(name)}")
""",
       "Reverse the string `'autonomy'` using slicing and store it in a variable named `rev`.",
       """assert _vars.get('rev') == 'ymonotua'""",
       None, ["strings", "slicing"]),

    _l("1.3", "Numbers, operators, and the math module", "Foundations", 8,
       """
# Numbers & Math

Python's number tower: `int` (arbitrary precision), `float` (IEEE-754 double),
`complex`, `Decimal`, `Fraction`.

Operators: `+ - * / // % **` — note `/` is true division, `//` is floor division.

For real math work import the `math` module: `math.sqrt`, `math.log`,
`math.pi`, `math.factorial`.
""",
       """
import math
print(7 / 2)      # 3.5
print(7 // 2)     # 3
print(7 % 2)      # 1
print(2 ** 10)    # 1024
print(math.sqrt(2))
print(math.factorial(10))
""",
       "Compute the area of a circle with radius 5 and store it in `area`.",
       """import math; assert abs(_vars.get('area', 0) - math.pi * 25) < 1e-6""",
       None, ["math", "numbers"]),

    _l("1.4", "Control flow — if / elif / else", "Foundations", 8,
       """
# Control Flow

Python uses **indentation**, not braces. The standard idiom:

```
if condition:
    ...
elif other:
    ...
else:
    ...
```

Truthiness: empty string, empty list, `0`, `None` are all *falsy*.
Use `and`, `or`, `not` — they short-circuit.
""",
       """
def classify(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"

for s in [95, 80, 65, 40]:
    print(s, "->", classify(s))
""",
       "Define a function `is_even(n)` that returns True if `n` is even.",
       """assert is_even(2) and not is_even(3)""",
       None, ["control-flow", "if"]),

    _l("1.5", "Loops — for, while, range", "Foundations", 10,
       """
# Loops

`for` iterates over **any iterable**. `range(start, stop, step)` is a lazy
iterator over integers.

```
for i in range(5):       # 0..4
for x in [1, 2, 3]:      # any iterable
while condition:         # repeat until false
```

Break out with `break`, skip with `continue`. The lesser-known `else` clause
on a loop runs only if the loop wasn't broken.
""",
       """
total = 0
for i in range(1, 11):
    total += i
print("Sum 1..10 =", total)

n = 17
for d in range(2, n):
    if n % d == 0:
        print("composite")
        break
else:
    print("prime")
""",
       "Compute the factorial of 8 with a for loop. Store result in `fact`.",
       """assert _vars.get('fact') == 40320""",
       "loop", ["loops", "for", "while"]),

    # ---------------------------------------------------------------- Core
    _l("2.1", "Functions & arguments", "Core", 12,
       """
# Functions

Functions are **first-class objects** — you can pass them, return them, store
them in lists. Arguments come in flavors:

- Positional: `f(1, 2)`
- Keyword: `f(x=1, y=2)`
- Default: `def f(x, y=10)`
- *args / **kwargs: variadic capture
- Keyword-only after `*`: `def f(*, key)`
- Positional-only before `/`: `def f(x, /)`
""",
       """
def greet(name, greeting="Hello", *, loud=False):
    msg = f"{greeting}, {name}!"
    return msg.upper() if loud else msg

print(greet("Tharchen"))
print(greet("World", greeting="Hi", loud=True))

def total(*nums, **opts):
    factor = opts.get("factor", 1)
    return sum(nums) * factor

print(total(1, 2, 3, 4, factor=10))
""",
       "Write a function `power(base, exp=2)` returning base**exp.",
       """assert power(3) == 9 and power(2, 10) == 1024""",
       "call-stack", ["functions", "args"]),

    _l("2.2", "Lambdas, map, filter, reduce", "Core", 10,
       """
# Lambdas & Functional helpers

A **lambda** is an anonymous expression-only function: `lambda x: x*2`.

- `map(f, iter)` — apply f to each element
- `filter(pred, iter)` — keep elements where pred is True
- `functools.reduce(f, iter, init)` — fold

In modern Python, comprehensions usually beat `map`/`filter` for clarity.
""",
       """
from functools import reduce

nums = [1, 2, 3, 4, 5]

doubled  = list(map(lambda x: x*2, nums))
evens    = list(filter(lambda x: x % 2 == 0, nums))
total    = reduce(lambda a, b: a + b, nums, 0)

print(doubled)   # [2,4,6,8,10]
print(evens)     # [2,4]
print(total)     # 15
""",
       "Use a lambda + map to produce squares of [1..6] in `sq`.",
       """assert _vars.get('sq') == [1,4,9,16,25,36]""",
       None, ["lambda", "functional"]),

    _l("2.3", "List, dict, set comprehensions", "Core", 10,
       """
# Comprehensions

Pythonic, fast, and readable when the body is small.

```
[expr for x in iterable if cond]            # list
{k: v for k, v in pairs}                    # dict
{expr for x in iterable}                    # set
(expr for x in iterable)                    # generator
```

Rule of thumb: if the comprehension spans more than two lines, use a regular
loop instead.
""",
       """
squares = [x*x for x in range(10) if x % 2 == 0]
print(squares)

word = "mississippi"
counts = {c: word.count(c) for c in set(word)}
print(counts)

unique_lengths = {len(w) for w in ["hi", "hey", "hello", "yo"]}
print(unique_lengths)
""",
       "Build a dict `sq_map` mapping n -> n*n for n in 1..5.",
       """assert _vars.get('sq_map') == {1:1,2:4,3:9,4:16,5:25}""",
       None, ["comprehension"]),

    # ---------------------------------------------------------------- Data Structures
    _l("3.1", "Lists in depth", "Data Structures", 10,
       """
# Lists

Dynamic arrays — O(1) append/pop from end, O(n) insert/remove from middle.

Key methods: `.append`, `.extend`, `.insert`, `.pop`, `.remove`, `.sort`,
`.reverse`, `.index`, `.count`.

`sorted()` returns a new list; `.sort()` mutates in place.
""",
       """
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()
print(nums)

nums.append(99)
nums.insert(0, -1)
print(nums)

# Copy vs alias
a = [1,2,3]
b = a            # alias - same object!
c = a.copy()     # real copy
b.append(99)
print("a:", a, "c:", c)
""",
       "Sort `[5,2,8,1,9]` descending into `desc`.",
       """assert _vars.get('desc') == [9,8,5,2,1]""",
       "list", ["list", "data-structures"]),

    _l("3.2", "Dicts — Python's superpower", "Data Structures", 12,
       """
# Dicts

Hash maps with O(1) average lookup. Since 3.7, **insertion order is preserved**.

Key patterns:
- `.get(key, default)` for safe access
- `.setdefault(key, default)` to insert-if-missing
- Dict comprehension to transform
- `collections.defaultdict` for grouping
- `collections.Counter` for histograms
""",
       """
from collections import Counter, defaultdict

person = {"name": "Tharchen", "city": "Nagoya", "stack": ["Python", "FastAPI"]}
print(person["name"])
print(person.get("missing", "n/a"))

# Group words by first letter
words = ["apple", "ant", "banana", "berry", "cherry"]
groups = defaultdict(list)
for w in words:
    groups[w[0]].append(w)
print(dict(groups))

# Histogram
print(Counter("mississippi"))
""",
       "Count letters in `'engineer'` into a dict named `freq`.",
       """from collections import Counter; assert _vars.get('freq') == dict(Counter('engineer'))""",
       "dict", ["dict", "hashmap"]),

    _l("3.3", "Tuples, sets, frozensets", "Data Structures", 8,
       """
# Tuples & Sets

**Tuples** are immutable sequences — great for fixed records and dict keys.
Tuple unpacking is everywhere in idiomatic Python.

**Sets** are unordered collections of unique hashable values. O(1) membership
test. Operations: `|` (union), `&` (intersection), `-` (difference),
`^` (symmetric diff).
""",
       """
point = (3, 4)
x, y = point
print(x, y)

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b)   # union
print(a & b)   # intersection
print(a - b)   # difference

# Deduplicate while preserving order (3.7+)
seen = dict.fromkeys([1,2,1,3,2,4])
print(list(seen))
""",
       "Get unique chars in 'mississippi' as a sorted list named `letters`.",
       """assert _vars.get('letters') == ['i','m','p','s']""",
       None, ["tuple", "set"]),

    # ---------------------------------------------------------------- OOP
    _l("4.1", "Classes & instances", "OOP", 12,
       """
# Classes

Use classes when state and behavior naturally belong together.

```
class Engineer:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def promote(self):
        self.level += 1
```

`__init__` runs at construction. `self` is the instance — there is no
implicit `this`.
""",
       """
class Engineer:
    def __init__(self, name, level=1):
        self.name = name
        self.level = level

    def promote(self):
        self.level += 1
        return self.level

    def __repr__(self):
        return f"<Engineer {self.name} L{self.level}>"

e = Engineer("Tharchen", 3)
e.promote()
print(e)
""",
       "Define a class `Counter` with method `inc()` that increments `self.value` (start at 0).",
       """c = Counter(); c.inc(); c.inc(); assert c.value == 2""",
       "object", ["oop", "classes"]),

    _l("4.2", "Inheritance & super()", "OOP", 10,
       """
# Inheritance

Single, multiple, and **MRO** (method resolution order) via C3 linearization.
Use `super().__init__(...)` to chain up.

Prefer composition over deep hierarchies. Mixins are fine for orthogonal
behavior (e.g., `LoggableMixin`).
""",
       """
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof"

class Puppy(Dog):
    def speak(self):
        base = super().speak()
        return base + " (squeaky)"

print(Puppy("Mochi").speak())
print(Puppy.__mro__)
""",
       "Make a class `Square(Rectangle)` where Rectangle has area(); a Square(4) should have area 16.",
       """
class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

assert 'Square' in dir() and Square(4).area() == 16
""",
       None, ["oop", "inheritance"]),

    _l("4.3", "Dunder methods & dataclasses", "OOP", 12,
       """
# Dunder Methods

Special methods that hook your class into Python's protocols:
`__repr__`, `__str__`, `__eq__`, `__hash__`, `__len__`, `__iter__`,
`__add__`, `__getitem__`, `__call__`, `__enter__/__exit__`.

For pure-data records, use `@dataclass` — it auto-generates `__init__`,
`__repr__`, `__eq__`.
""",
       """
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __abs__(self):
        return (self.x**2 + self.y**2) ** 0.5

v = Vec2(3, 4) + Vec2(1, 1)
print(v, abs(v))
""",
       "Create a frozen dataclass `Point(x, y)` then assert `Point(1,2) == Point(1,2)`.",
       """
from dataclasses import is_dataclass
assert is_dataclass(Point) and Point(1,2) == Point(1,2)
""",
       None, ["dataclass", "dunder"]),

    # ---------------------------------------------------------------- Functional & Iterators
    _l("5.1", "Generators & yield", "Functional & Iterators", 10,
       """
# Generators

A function with `yield` returns a **generator** — a lazy iterator. State is
preserved between yields. Memory-cheap for huge sequences.

```
def squares(n):
    for i in range(n):
        yield i*i
```

`yield from sub` delegates iteration. Generator expressions: `(x*x for x in xs)`.
""",
       """
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

g = fib()
print([next(g) for _ in range(10)])
""",
       "Write a generator `evens(n)` yielding the first n even numbers (0, 2, 4, ...).",
       """assert list(evens(5)) == [0,2,4,6,8]""",
       "generator", ["generator", "yield"]),

    _l("5.2", "itertools toolbox", "Functional & Iterators", 10,
       """
# itertools

A standard-library treasure chest:

- `chain`, `cycle`, `repeat` — combine/repeat
- `islice`, `takewhile`, `dropwhile` — slice lazily
- `groupby` — like SQL GROUP BY (input must be sorted)
- `product`, `permutations`, `combinations` — combinatorics
- `accumulate` — running totals
""",
       """
import itertools as it

# All pairs
print(list(it.combinations([1,2,3,4], 2)))

# Running sum
print(list(it.accumulate([1,2,3,4,5])))

# First 10 primes via lazy filter
def primes():
    n = 2
    while True:
        if all(n % d for d in range(2, int(n**0.5)+1)):
            yield n
        n += 1

print(list(it.islice(primes(), 10)))
""",
       "Use itertools.combinations to count pairs from [1..5] into `pairs`.",
       """import itertools as it; assert _vars.get('pairs') == list(it.combinations([1,2,3,4,5], 2))""",
       None, ["itertools"]),

    _l("5.3", "Decorators", "Functional & Iterators", 14,
       """
# Decorators

A decorator is a callable that takes a function and returns a (usually
wrapped) function. Use `@functools.wraps` to preserve metadata.

```
def timed(fn):
    @wraps(fn)
    def inner(*a, **k):
        t0 = time.perf_counter()
        try:    return fn(*a, **k)
        finally: print(time.perf_counter() - t0)
    return inner
```

Common uses: caching (`@functools.lru_cache`), retries, validation, route
registration (FastAPI, Flask).
""",
       """
from functools import wraps
import time

def timed(fn):
    @wraps(fn)
    def inner(*a, **k):
        t0 = time.perf_counter()
        result = fn(*a, **k)
        dt = (time.perf_counter() - t0) * 1000
        print(f"{fn.__name__} took {dt:.2f}ms")
        return result
    return inner

@timed
def slow_sum(n):
    return sum(range(n))

print(slow_sum(1_000_000))
""",
       "Write a decorator `@shout` that uppercases the string returned by the wrapped function. Apply it to `def hi(): return 'hello'`.",
       """assert hi() == 'HELLO'""",
       None, ["decorators"]),

    # ---------------------------------------------------------------- Async & Concurrency
    _l("6.1", "Threads, processes, the GIL", "Async & Concurrency", 12,
       """
# Concurrency Models

CPython has a **Global Interpreter Lock**: only one thread runs Python
bytecode at a time. So:

- **I/O-bound** work? `threading` or `asyncio` give real concurrency.
- **CPU-bound** work? Use `multiprocessing` or release the GIL via C
  extensions (NumPy, polars).

`concurrent.futures` is the modern, unified API.
""",
       """
from concurrent.futures import ThreadPoolExecutor
import time

def slow_square(n):
    # Simulated work — pretend each task does ~50ms of I/O-like waiting.
    time.sleep(0.05)
    return n * n

nums = list(range(8))

# Sequential
t0 = time.time()
seq = [slow_square(n) for n in nums]
seq_t = time.time() - t0

# Threaded — wins because the work is I/O-bound (sleep releases the GIL)
t0 = time.time()
with ThreadPoolExecutor(max_workers=4) as pool:
    par = list(pool.map(slow_square, nums))
par_t = time.time() - t0

print(f"sequential: {seq_t:.2f}s   threaded: {par_t:.2f}s")
print(f"speedup ≈ {seq_t / par_t:.1f}x")
""",
       "Use ThreadPoolExecutor to compute squares of [1..5] into `out`.",
       """from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as p: out = list(p.map(lambda x: x*x, [1,2,3,4,5]))
assert out == [1,4,9,16,25]""",
       None, ["concurrency", "threads"]),

    _l("6.2", "asyncio fundamentals", "Async & Concurrency", 14,
       """
# asyncio

Cooperative concurrency via the event loop. `async def` defines a coroutine,
`await` suspends it.

- `asyncio.run(coro)` — top-level runner
- `asyncio.gather(*coros)` — fan out
- `asyncio.create_task(coro)` — schedule, fire-and-forget
- `asyncio.Queue` — producer/consumer

Pair with `httpx.AsyncClient` or `aiohttp` for real HTTP.
""",
       """
import asyncio

async def worker(name, delay):
    await asyncio.sleep(delay)
    return f"{name} done after {delay}s"

async def main():
    results = await asyncio.gather(
        worker("A", 0.1),
        worker("B", 0.2),
        worker("C", 0.05),
    )
    for r in results:
        print(r)

asyncio.run(main())
""",
       "Use asyncio.gather to await two coroutines that return 1 and 2; store in `pair`.",
       """import asyncio
async def one(): return 1
async def two(): return 2
pair = asyncio.run(asyncio.gather(one(), two()))
assert pair == [1, 2]""",
       None, ["asyncio"]),

    # ---------------------------------------------------------------- Stdlib Power Tools
    _l("7.1", "Files & paths with pathlib", "Stdlib Power Tools", 8,
       """
# pathlib

Modern, OS-agnostic file paths. Replaces most `os.path` usage.

```
from pathlib import Path
p = Path("data/notes.txt")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("hello")
text = p.read_text()
```

`Path.glob`, `Path.rglob`, `Path.exists`, `Path.with_suffix` — read the docs,
all the verbs you want are there.
""",
       """
from pathlib import Path
import tempfile, os

with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    (root / "a.txt").write_text("hello")
    (root / "b.txt").write_text("world")
    for f in root.glob("*.txt"):
        print(f.name, "->", f.read_text())
""",
       "Use pathlib to confirm '/' and store `Path('/').exists()` in `root_exists`.",
       """from pathlib import Path; assert _vars.get('root_exists') == Path('/').exists()""",
       None, ["pathlib", "files"]),

    _l("7.2", "JSON, CSV, sqlite3", "Stdlib Power Tools", 10,
       """
# Built-in Data I/O

- **JSON**: `json.dumps(obj)`, `json.loads(s)`, `json.load(f)`. Use
  `default=str` for unknown types.
- **CSV**: `csv.DictReader/DictWriter` — dict-of-strings only.
- **SQLite**: zero-config embedded DB; perfect for local-first apps.

For your local-AI builds, sqlite3 + JSON columns covers 80% of state needs
without a Postgres server.
""",
       """
import sqlite3, json

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE notes(id INTEGER PRIMARY KEY, body TEXT)")
con.executemany("INSERT INTO notes(body) VALUES (?)",
                [("alpha",), ("beta",), ("gamma",)])
con.commit()

rows = con.execute("SELECT id, body FROM notes WHERE body LIKE 'a%'").fetchall()
print(rows)
print(json.dumps(rows))
""",
       "Use json.dumps to serialize {'a': 1, 'b': 2} into `s`.",
       """import json; assert json.loads(_vars.get('s', '{}')) == {'a': 1, 'b': 2}""",
       None, ["json", "sqlite", "csv"]),

    _l("7.3", "Regular expressions with re", "Stdlib Power Tools", 10,
       """
# Regex

`re.match`, `re.search`, `re.findall`, `re.sub`. Use **raw strings** `r"..."`
to avoid backslash hell.

Capture groups with `()`, named groups with `(?P<name>...)`. Compile patterns
you reuse: `pat = re.compile(r"...")`.
""",
       """
import re

text = "Email me at tharchen@example.jp or admin@pyforge.io"
emails = re.findall(r"[\\w.+-]+@[\\w-]+\\.[\\w.-]+", text)
print(emails)

phone = "Call (080) 1234-5678 today"
m = re.search(r"\\((\\d+)\\)\\s+(\\d+-\\d+)", phone)
if m:
    print(m.group(1), m.group(2))
""",
       "Use re.findall to extract all numbers from '5 cats, 3 dogs, 12 fish' into `nums` as ints.",
       """import re; assert _vars.get('nums') == [5, 3, 12]""",
       None, ["regex"]),

    # ---------------------------------------------------------------- Errors
    _l("8.1", "Exceptions, try/except, custom errors", "Errors & Logging", 10,
       """
# Exceptions

Use exceptions for *exceptional* conditions, not control flow.

```
try:
    ...
except (ValueError, KeyError) as e:
    log.exception(...)
except Exception:
    raise        # re-raise unhandled
finally:
    cleanup()
```

Define your own with `class MyError(Exception): pass`. Use `raise X from Y`
to chain causes.
""",
       """
class InsufficientFunds(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFunds(f"need {amount}, have {balance}")
    return balance - amount

try:
    withdraw(100, 200)
except InsufficientFunds as e:
    print("blocked:", e)
""",
       "Catch ZeroDivisionError when computing 1/0 and store the string of the exception in `err`.",
       """assert isinstance(_vars.get('err'), str) and 'division' in _vars.get('err','').lower()""",
       None, ["exceptions"]),

    _l("8.2", "logging properly", "Errors & Logging", 8,
       """
# logging

`print` is for scripts. **Use `logging` for anything that runs more than once.**

```
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s")

log.debug(...) # quiet by default
log.info(...)
log.warning(...)
log.exception(...)  # include traceback
```
""",
       """
import logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
log = logging.getLogger("demo")

log.info("starting up")
try:
    1 / 0
except Exception:
    log.exception("math broke")
log.info("recovered")
""",
       "Get a logger named 'app' and store it in `lg`.",
       """import logging; assert isinstance(_vars.get('lg'), logging.Logger) and _vars.get('lg').name == 'app'""",
       None, ["logging"]),

    # ---------------------------------------------------------------- Data Science
    _l("9.1", "NumPy crash course", "Data Science", 12,
       """
# NumPy

The numerical foundation. `ndarray` is a typed, contiguous, n-dimensional
buffer with **vectorized** operations that bypass the Python interpreter.

Rules of thumb:
- Avoid Python loops on numeric arrays — use vector ops.
- Watch shapes: broadcasting rules are powerful but easy to get wrong.

(Requires `pip install numpy`.)
""",
       """
import numpy as np

a = np.arange(12).reshape(3, 4)
print(a)
print(a.sum(axis=0))     # column sums
print(a[a % 2 == 0])     # boolean mask
print(a @ a.T)           # matrix product
""",
       "Make a 1D NumPy array of squares of 0..9 named `sq_arr`.",
       """import numpy as np; assert np.array_equal(_vars.get('sq_arr'), np.arange(10)**2)""",
       None, ["numpy", "data-science"]),

    _l("9.2", "Pandas dataframes", "Data Science", 12,
       """
# Pandas

Tabular data with labeled axes. The core types are `Series` (1D) and
`DataFrame` (2D).

Common verbs:
- `df.head()`, `.describe()`, `.info()`
- Selection: `df["col"]`, `df.loc[row, col]`, `df.iloc[i, j]`
- Aggregations: `df.groupby("k")["v"].sum()`
- Joins: `df1.merge(df2, on="id")`

(Requires `pip install pandas`.)
""",
       """
import pandas as pd

df = pd.DataFrame({
    "name": ["Aiko", "Ben", "Chika", "Daiki"],
    "team": ["A", "B", "A", "B"],
    "score": [88, 71, 95, 60],
})

print(df.groupby("team")["score"].mean())
print(df[df["score"] > 80])
""",
       "Build a DataFrame `df` with columns 'x'=[1,2,3], 'y'=[4,5,6] and confirm shape (3,2).",
       """assert _vars.get('df') is not None and _vars['df'].shape == (3, 2)""",
       None, ["pandas"]),

    _l("9.3", "Matplotlib basics", "Data Science", 10,
       """
# Plotting

`matplotlib.pyplot` is the workhorse. The two-step pattern:

```
fig, ax = plt.subplots()
ax.plot(x, y, label="series")
ax.set_xlabel("..."); ax.set_ylabel("..."); ax.legend()
fig.tight_layout()
```

For static reports, prefer `fig, ax = plt.subplots()` over the global state.

(Requires `pip install matplotlib`.)
""",
       """
import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import math

xs = [i/10 for i in range(0, 63)]
ys = [math.sin(x) for x in xs]
fig, ax = plt.subplots()
ax.plot(xs, ys)
ax.set_title("sin(x)")
fig.savefig("/tmp/sine.png")
print("saved")
""",
       "Use matplotlib to compute and save a cosine plot to /tmp/cos.png. Set `done=True` after.",
       """import os; assert _vars.get('done') is True and os.path.exists('/tmp/cos.png')""",
       None, ["matplotlib"]),

    # ---------------------------------------------------------------- Web & APIs
    _l("10.1", "HTTP requests with httpx", "Web & APIs", 10,
       """
# HTTP Clients

`httpx` is the modern client — sync *and* async, HTTP/2, connection pools.

```
import httpx
r = httpx.get(url, timeout=10)
r.raise_for_status()
data = r.json()
```

For lots of requests, reuse a `httpx.Client()` (or `httpx.AsyncClient()`).
""",
       """
import httpx

r = httpx.get("https://httpbin.org/json", timeout=10)
r.raise_for_status()
print(r.status_code)
print(list(r.json().keys()))
""",
       "Make a GET to https://httpbin.org/uuid and store the parsed json in `j`.",
       """import httpx; assert 'uuid' in (_vars.get('j') or {})""",
       None, ["http", "httpx"]),

    _l("10.2", "Build a FastAPI service", "Web & APIs", 14,
       """
# FastAPI

Production-grade async web framework with automatic OpenAPI docs and
Pydantic validation.

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    qty: int = 1

@app.post("/items")
def create(item: Item):
    return {"ok": True, "item": item}
```

Run with `uvicorn module:app --reload`.
""",
       """
# Demo: instantiate the app object — we won't actually serve in this lesson.
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="PyForge Demo")

class Echo(BaseModel):
    msg: str

@app.post("/echo")
def echo(payload: Echo):
    return {"echo": payload.msg.upper()}

print(app.title, [r.path for r in app.routes])
""",
       "Build a FastAPI `app` exposing GET /ping returning {'ping':'pong'}.",
       """from fastapi.testclient import TestClient
client = TestClient(app)
assert client.get('/ping').json() == {'ping': 'pong'}""",
       None, ["fastapi", "web"]),

    # ---------------------------------------------------------------- Testing
    _l("11.1", "pytest essentials", "Testing & Tooling", 10,
       """
# Testing with pytest

`pytest` is the de-facto Python test runner.

```
def test_adds():
    assert add(2, 3) == 5
```

Power features:
- Fixtures (`@pytest.fixture`) for shared setup
- Parametrize (`@pytest.mark.parametrize`) for table-driven tests
- `pytest.raises(Exception)` to assert raises

Run with `pytest -v`.
""",
       """
# Lightweight: assert-based "tests" you can run in this lesson.
def add(a, b): return a + b
def div(a, b):
    if b == 0: raise ZeroDivisionError("nope")
    return a / b

assert add(2, 3) == 5
try:
    div(1, 0)
    raise AssertionError("should have raised")
except ZeroDivisionError:
    pass

print("all green")
""",
       "Define a function `mul(a,b)` that returns a*b. The auto-check will verify it.",
       """assert mul(3, 4) == 12 and mul(0, 99) == 0""",
       None, ["testing", "pytest"]),

    # ---------------------------------------------------------------- Performance
    _l("12.1", "Profiling & cProfile", "Performance", 10,
       """
# Profile before optimizing

> "Premature optimization is the root of all evil." — Knuth

Tools you should know:
- `time.perf_counter()` for ad-hoc timing
- `timeit` for micro-benchmarks
- `cProfile` for function-level profiling
- `memory_profiler` for RAM
- `py-spy` for *production* sampling profiler
""",
       """
import cProfile, pstats, io

def slow():
    return sum(i*i for i in range(200_000))

pr = cProfile.Profile()
pr.enable()
slow()
pr.disable()

buf = io.StringIO()
pstats.Stats(pr, stream=buf).sort_stats("cumulative").print_stats(5)
print(buf.getvalue())
""",
       "Use timeit to measure summing range(1000) once, store float in `dt` (seconds).",
       """import numbers; assert isinstance(_vars.get('dt'), numbers.Number) and _vars.get('dt') >= 0""",
       None, ["performance", "profiling"]),

    _l("12.2", "lru_cache & memoization", "Performance", 8,
       """
# Memoization

`@functools.lru_cache(maxsize=...)` adds a memoization layer with bounded
size. Perfect for pure functions with hashable args (recursive math, parsing,
config lookup).
""",
       """
from functools import lru_cache
import time

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

t0 = time.perf_counter()
print(fib(80))
print(f"{(time.perf_counter()-t0)*1000:.2f}ms")
print(fib.cache_info())
""",
       "Decorate `square` with lru_cache and call square(5); confirm cache hit on second call by checking cache_info().hits >= 1 stored in `hits`.",
       """assert _vars.get('hits', 0) >= 1""",
       None, ["cache", "performance"]),

    # ---------------------------------------------------------------- AI & LLMs
    _l("13.1", "Calling Ollama from Python", "AI & LLMs", 12,
       """
# Local LLMs with Ollama

Ollama exposes a REST API on `http://localhost:11434`. The `/api/generate`
endpoint accepts a model name and prompt, streaming JSON lines back.

```
POST /api/generate
{
  "model": "mistral",
  "prompt": "Explain decorators",
  "stream": false
}
```

This is exactly what the AI Tutor panel in this app uses. No cloud, no API
key, no rate limits.
""",
       """
# We won't hit Ollama in this lesson — just shape the call.
import json

payload = {
    "model": "mistral",
    "prompt": "Say hi briefly",
    "stream": False,
}
print(json.dumps(payload, indent=2))
""",
       "Build the request payload dict for prompt 'hello'. Store in `req`.",
       """assert _vars.get('req', {}).get('model') and _vars['req'].get('prompt') == 'hello'""",
       None, ["ollama", "llm"]),

    _l("13.2", "Mini RAG pipeline (concept)", "AI & LLMs", 14,
       """
# Retrieval-Augmented Generation

The pattern: split docs → embed → store in a vector DB → at query time,
embed the question → top-k nearest chunks → stuff into the prompt.

Stack you'd actually ship:
- Embeddings: `nomic-embed-text` (Ollama) or `sentence-transformers`
- Vector DB: Chroma, Qdrant, FAISS
- Orchestration: LlamaIndex or LangChain (or hand-rolled — often clearer)

This lesson sketches the *structure* without external deps.
""",
       """
# Toy RAG with cosine similarity over fake embeddings.
import math, random

random.seed(0)
def embed(text):
    return [hash((text, i)) % 1000 / 1000 for i in range(8)]

def cos(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    return dot / (na*nb + 1e-9)

docs = ["python is a language", "ollama runs LLMs locally", "fastapi is async"]
vecs = [embed(d) for d in docs]

q = "how to run language models"
qv = embed(q)
ranked = sorted(zip(docs, vecs), key=lambda dv: -cos(qv, dv[1]))
print("top:", ranked[0][0])
""",
       "Define a function `top1(query, docs)` that returns the doc with highest cos sim using the embed/cos helpers above. Store the call result on docs above for q='ollama' in `winner`.",
       """assert isinstance(_vars.get('winner'), str)""",
       None, ["rag", "llm"]),

    # ---------------------------------------------------------------- Advanced Patterns
    _l("14.1", "Context Managers & 'with'", "Advanced Patterns", 15,
       """
# Context Managers

The `with` statement guarantees that resources are properly acquired and released, even if an exception occurs. Under the hood, a context manager implements two dunder methods: `__enter__()` and `__exit__(exc_type, exc_val, traceback)`.

If an exception is raised inside the `with` block, `__exit__` receives the exception details. If `__exit__` returns `True`, the exception is swallowed.

Instead of writing classes, you can use the `@contextmanager` decorator from `contextlib` to create context managers using generators. This is often cleaner and reduces boilerplate.

```python
from contextlib import contextmanager

@contextmanager
def file_manager(name):
    f = open(name, 'w')
    try:
        yield f
    finally:
        f.close()
```
""",
       """
import time

class TimerContext:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
        
    def __exit__(self, exc_type, exc_val, tb):
        self.end = time.perf_counter()
        print(f"Elapsed time: {self.end - self.start:.4f} seconds")
        # Return False to let exceptions propagate
        return False

with TimerContext():
    print("Doing expensive work...")
    time.sleep(0.1)
""",
       "Create a basic context manager class `Temp` with `__enter__` returning 'x' and `__exit__` doing nothing.",
       """assert hasattr(Temp, '__enter__') and hasattr(Temp, '__exit__')""",
       None, ["context-manager", "with"]),

    _l("14.2", "Structural Pattern Matching", "Advanced Patterns", 20,
       """
# Match / Case (Python 3.10+)

Structural Pattern Matching introduces a `match` statement paired with `case` blocks. Unlike traditional switch statements in C or Java, Python's `match` can destructure data types, match specific shapes, and bind variables on the fly.

You can match on:
- Literal values (e.g., `case 200:`)
- Sequences (e.g., `case [x, y, *rest]:` to bind the first two elements to x and y, and the remainder to rest)
- Dictionaries (e.g., `case {"status": "ok", "data": data}:`)
- Class instances (e.g., `case Point(x=0, y=y):`)

You can also use guards (`if condition`) to add conditional logic to a case. The wildcard `_` acts as a catch-all.
""",
       """
def handle_response(response):
    match response:
        case {"status": 200, "data": data}:
            return f"Success with {len(data)} items"
        case {"status": 404}:
            return "Not found"
        case {"status": code, "error": msg} if code >= 500:
            return f"Server error {code}: {msg}"
        case _:
            return "Unknown response"

print(handle_response({"status": 200, "data": [1, 2, 3]}))
print(handle_response({"status": 503, "error": "Database down"}))
""",
       "Define a `process(items)` function that uses match/case to return 'Empty' for `[]`, 'Single' for `[x]`, and 'Many' for `[x, y, *rest]`.",
       """assert process([]) == 'Empty' and process([1]) == 'Single' and process([1,2,3]) == 'Many'""",
       None, ["match", "case", "pattern-matching"]),

    # ---------------------------------------------------------------- Type Hinting
    _l("15.1", "Type Hinting & Protocols", "Type Hinting", 20,
       """
# Modern Type Hinting

Type hinting allows static analyzers like `mypy` to catch errors before runtime. As of Python 3.9+, standard collections support generic types directly (e.g., `list[int]`, `dict[str, float]`).

Union types can be expressed with `|` (e.g., `int | None`). 

`Protocols` (from the `typing` module) provide **structural subtyping** (often called static duck typing). If a class implements the methods defined in a Protocol, it is considered a subtype of that Protocol—even without explicitly inheriting from it. This heavily encourages composition and decoupled design.
""",
       """
from typing import Protocol

# Define a protocol (interface)
class Drawable(Protocol):
    def draw(self) -> str:
        ...

# Implicitly implements Drawable
class Circle:
    def draw(self) -> str:
        return "Drawing a circle"

# Implicitly implements Drawable
class Rectangle:
    def draw(self) -> str:
        return "Drawing a rectangle"

def render(item: Drawable) -> None:
    print(item.draw())

render(Circle())
render(Rectangle())
""",
       "Define a function `greet(name: str) -> str` returning 'hello ' + name.",
       """assert greet.__annotations__ == {'name': str, 'return': str} and greet('world') == 'hello world'""",
       None, ["typing", "protocol", "mypy"]),

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
]


def all_levels() -> List[str]:
    """Return ordered, deduped list of levels for sidebar grouping."""
    seen = []
    for l in CURRICULUM:
        if l["level"] not in seen:
            seen.append(l["level"])
    return seen


def by_level(level: str) -> List[Dict[str, Any]]:
    return [l for l in CURRICULUM if l["level"] == level]


def find_lesson(lid: str) -> Dict[str, Any]:
    for l in CURRICULUM:
        if l["id"] == lid:
            return l
    raise KeyError(lid)
