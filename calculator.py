"""Calculator demo.

This file is finished. Do not edit it.

It looks for four files in this folder: add.py, subtract.py, multiply.py and
divide.py. Each one must contain a function with the same name as the file.
If a file is missing, or something is wrong inside it, this demo tells you
which one instead of crashing.
"""

import importlib

# Each line: file name (also the function name), symbol, first number,
# second number, and the answer we expect.
OPERATIONS = [
    ("add", "+", 12, 4, 16),
    ("subtract", "-", 12, 4, 8),
    ("multiply", "*", 12, 4, 48),
    ("divide", "/", 12, 4, 3),
]

# Optional extra, used only if power.py exists (the stretch task).
BONUS = [
    ("power", "to the power of", 2, 10, 1024),
]


def load(name):
    """Load the function called `name` from the file `name.py`.

    Returns (function, None) if it works, or (None, message) if it does not.
    """
    try:
        module = importlib.import_module(name)
    except ModuleNotFoundError as error:
        if error.name == name:
            return None, "still missing"
        return None, f"imports '{error.name}', which cannot be found"
    except Exception as error:
        return None, f"has an error: {type(error).__name__}: {error}"

    function = getattr(module, name, None)
    if not callable(function):
        return None, f"exists, but has no function called {name}"
    return function, None


def try_operation(name, symbol, a, b, expected):
    """Run one operation. Returns (line_to_print, is_ready)."""
    function, problem = load(name)
    if function is None:
        return f"{name}.py {problem}", False

    try:
        result = function(a, b)
    except Exception as error:
        return f"{name}.py crashed: {type(error).__name__}: {error}", False

    line = f"{a} {symbol} {b} = {result}"
    if result != expected:
        return f"{line}   (expected {expected}, check {name}.py)", False
    return line, True


def try_divide_by_zero():
    """Check that divide.py does not crash when b is 0."""
    function, problem = load("divide")
    if function is None:
        return None, False

    try:
        result = function(12, 0)
    except ZeroDivisionError:
        return "divide.py crashes when b is 0. It must handle that case.", False
    except Exception as error:
        return f"divide.py crashed when b is 0: {type(error).__name__}: {error}", False

    return f"12 / 0 = {result}   (handled)", True


def main():
    print("Calculator demo")
    print()

    not_ready = []

    for name, symbol, a, b, expected in OPERATIONS:
        line, ready = try_operation(name, symbol, a, b, expected)
        print(f"  {line}")
        if not ready:
            not_ready.append(name + ".py")

    zero_line, zero_ready = try_divide_by_zero()
    if zero_line is not None:
        print(f"  {zero_line}")
        if not zero_ready and "divide.py" not in not_ready:
            not_ready.append("divide.py")

    for name, symbol, a, b, expected in BONUS:
        function, problem = load(name)
        if function is not None or problem != "still missing":
            line, ready = try_operation(name, symbol, a, b, expected)
            print(f"  {line}   (bonus)")

    print()
    if not_ready:
        print("Not working yet: " + ", ".join(not_ready))
    else:
        print("All four files work. Well done.")


if __name__ == "__main__":
    main()
