def factorial(n):
    """
    Classic recursion example: Factorial
    n! = n * (n-1) * ... * 1
    """
    # Base case
    if n == 0 or n == 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)


def fibonacci(n):
    """
    Fibonacci sequence: F(n) = F(n-1) + F(n-2)
    """
    # Base cases
    if n == 0:
        return 0
    elif n == 1:
        return 1
    # Recursive case
    return fibonacci(n - 1) + fibonacci(n - 2)


def linear_sum(arr, n=None):
    """Sum of array elements using linear recursion"""
    if n is None:
        n = len(arr)

    # Base case
    if n == 0:
        return 0
    # Recursive case: last element + sum of rest
    return linear_sum(arr, n - 1) + arr[n - 1]


def reverse_string(s):
    """Reverse string using recursion"""
    # Base case
    if len(s) <= 1:
        return s
    # Recursive case: last char + reverse of rest
    return s[-1] + reverse_string(s[:-1])


def binary_search_recursive(arr, target, left=0, right=None):
    """Binary search using recursion"""
    if right is None:
        right = len(arr) - 1

    # Base case: element not found
    if left > right:
        return -1

    mid = (left + right) // 2

    # Base case: element found
    if arr[mid] == target:
        return mid
    # Recursive cases
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def fibonacci_multiple(n):
    """Fibonacci with multiple recursive calls"""
    if n <= 1:
        return n
    return fibonacci_multiple(n - 1) + fibonacci_multiple(n - 2)


def tower_of_hanoi(n, source, target, auxiliary):
    """Tower of Hanoi - exponential recursion"""
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return

    tower_of_hanoi(n - 1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
    tower_of_hanoi(n - 1, auxiliary, target, source)


def factorial_tail(n, accumulator=1):
    """Tail-recursive factorial"""
    # Base case
    if n == 0:
        return accumulator
    # Tail recursive call
    return factorial_tail(n - 1, n * accumulator)


def gcd(a, b):
    """Greatest Common Divisor using tail recursion"""
    if b == 0:
        return a
    return gcd(b, a % b)


def analyze_recursion_depth():
    """Analyze recursion depth and time complexity"""

    def recursive_function(n, depth=0):
        if n <= 0:
            return 0

        print(f"Depth: {depth}, n: {n}")

        # Multiple recursive calls
        return recursive_function(n - 1, depth + 1) + recursive_function(
            n - 2, depth + 1
        )

    # This demonstrates exponential growth
    recursive_function(4)


import time
import sys


def benchmark_recursion():
    """Benchmark different recursion patterns"""

    sys.setrecursionlimit(10000)  # Increase for large tests

    test_cases = [5, 10, 15, 20, 25]

    for n in test_cases:
        print(f"\nTesting with n={n}")

        # Factorial (linear)
        start = time.time()
        result = factorial(n)
        fact_time = time.time() - start
        print(f"Factorial: {fact_time:.6f}s")

        # Fibonacci naive (exponential)
        if n <= 35:  # Prevent extremely long runs
            start = time.time()
            result = fibonacci(n)
            fib_time = time.time() - start
            print(f"Fibonacci: {fib_time:.6f}s")
        else:
            print("Fibonacci: SKIPPED (too slow)")

        # Binary search style (logarithmic)
        arr = list(range(2 ** min(n, 20)))  # Prevent huge arrays
        start = time.time()
        binary_search_recursive(arr, arr[-1])
        bin_time = time.time() - start
        print(f"Binary Search: {bin_time:.6f}s")


def space_analysis():
    """
    Recursion Space Complexity Details:

    Call Stack Usage:
    - Each recursive call creates a stack frame
    - Stack frame contains: parameters, local variables, return address
    - Memory grows with recursion depth

    Python Specifics:
    - Default recursion limit: ~1000 frames
    - Each frame: ~1KB (depends on local variables)
    - Maximum practical depth: ~500-1000

    Memory Comparison:
    - Iterative solutions: O(1) auxiliary space
    - Recursive solutions: O(depth) auxiliary space
    """

    def demonstrate_stack_usage(n, depth=0):
        """Show how stack frames accumulate"""
        local_var = "x" * 100  # Each call uses ~100 bytes

        if depth >= n:
            return depth

        return demonstrate_stack_usage(n, depth + 1)

    try:
        demonstrate_stack_usage(1000)
    except RecursionError as e:
        print(f"Recursion limit reached: {e}")


def tail_recursion_limitation():
    """
    Python Tail Recursion Reality:

    Despite being tail-recursive, Python DOES NOT optimize:
    - Still creates new stack frames
    - Still has recursion limits
    - No performance benefit over regular recursion

    Example showing tail recursion doesn't help in Python:
    """

    def regular_factorial(n):
        if n == 0:
            return 1
        return n * regular_factorial(n - 1)  # Not tail call

    def tail_factorial(n, acc=1):
        if n == 0:
            return acc
        return tail_factorial(n - 1, n * acc)  # Tail call

    # Both will hit recursion limit at similar depths
    # Both use O(n) stack space


def validated_recursion(func):
    """Decorator for recursive function validation"""

    def wrapper(*args, **kwargs):
        # Common preconditions for recursive functions
        if any(arg is None for arg in args):
            raise ValueError("None arguments not allowed")

        # Check for negative values where inappropriate
        if hasattr(func, "__name__") and "factorial" in func.__name__:
            if args[0] < 0:
                raise ValueError("Factorial not defined for negative numbers")

        try:
            result = func(*args, **kwargs)

            # Postcondition validation
            if "factorial" in func.__name__ and args[0] >= 0:
                assert result >= 1, "Factorial must be >= 1"

            return result

        except RecursionError:
            raise RecursionError(f"Recursion depth exceeded for {func.__name__}")

    return wrapper


@validated_recursion
def safe_factorial(n):
    """Factorial with built-in validation"""
    if n < 0:
        raise ValueError("Input must be non-negative")
    if n == 0:
        return 1
    return n * safe_factorial(n - 1)


def test_recursion_edge_cases():
    """Comprehensive edge case testing for recursive functions"""

    test_cases = [
        # (function, args, expected, description)
        (factorial, (0,), 1, "Factorial of 0"),
        (factorial, (1,), 1, "Factorial of 1"),
        (fibonacci, (0,), 0, "Fibonacci of 0"),
        (fibonacci, (1,), 1, "Fibonacci of 1"),
        (reverse_string, ("",), "", "Empty string"),
        (reverse_string, ("a",), "a", "Single character"),
        (gcd, (0, 5), 5, "GCD with zero"),
        (gcd, (5, 0), 5, "GCD with zero reversed"),
    ]

    error_cases = [
        (factorial, (-1,), ValueError, "Negative factorial"),
        (factorial, (10000,), RecursionError, "Deep recursion"),
    ]

    print("Testing normal cases:")
    for func, args, expected, description in test_cases:
        try:
            result = func(*args)
            status = "PASS" if result == expected else "FAIL"
            print(f"  {description:30}: {status}")
        except Exception as e:
            print(f"  {description:30}: ERROR - {e}")

    print("\nTesting error cases:")
    for func, args, expected_error, description in error_cases:
        try:
            func(*args)
            print(f"  {description:30}: FAIL - Should have raised {expected_error}")
        except expected_error:
            print(f"  {description:30}: PASS")
        except Exception as e:
            print(f"  {description:30}: FAIL - Wrong error: {e}")


from functools import lru_cache


def fibonacci_naive(n):
    """Naive Fibonacci (exponential time)"""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


@lru_cache(maxsize=None)
def fibonacci_memoized(n):
    """Memoized Fibonacci (linear time)"""
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def fibonacci_iterative(n):
    """Iterative Fibonacci (O(1) space)"""
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def factorial_iterative(n):
    """Convert recursive factorial to iterative"""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def reverse_string_iterative(s):
    """Convert recursive reverse to iterative"""
    result = []
    for char in s:
        result.insert(0, char)
    return "".join(result)


def depth_limited_recursion(func, max_depth=1000):
    """Decorator to limit recursion depth"""
    state = {"depth": 0}

    def wrapper(*args, **kwargs):
        state["depth"] += 1
        if state["depth"] > max_depth:
            state["depth"] -= 1
            raise RecursionError(f"Maximum recursion depth {max_depth} exceeded")

        try:
            return func(*args, **kwargs)
        finally:
            state["depth"] -= 1

    return wrapper


@depth_limited_recursion
def safe_recursive_function(n):
    """Recursive function with depth limiting"""
    if n == 0:
        return 0
    return safe_recursive_function(n - 1) + n


def cache_performance_analysis():
    """
    Cache Performance Characteristics:

    Recursion Cache Behavior:
    - Stack-based memory access: Excellent locality
    - Repeated computations: Poor (solved by memoization)
    - Function call overhead: Significant in Python

    Optimization Strategies:
    1. Memoization: Cache computed results
    2. Iterative conversion: Eliminate call overhead
    3. Tail recursion: Though not optimized in Python
    4. Dynamic programming: Bottom-up computation

    Real-world Impact:
    - Naive Fibonacci(40): ~1 second
    - Memoized Fibonacci(40): ~0.0001 second
    - Iterative Fibonacci(40): ~0.00001 second
    """

    def demonstrate_memoization_impact():
        import time

        n = 35

        # Naive (exponential)
        start = time.time()
        result1 = fibonacci_naive(n)
        time1 = time.time() - start

        # Memoized (linear)
        start = time.time()
        result2 = fibonacci_memoized(n)
        time2 = time.time() - start

        # Iterative (linear time, constant space)
        start = time.time()
        result3 = fibonacci_iterative(n)
        time3 = time.time() - start

        print(f"Fibonacci({n}):")
        print(f"  Naive:     {time1:.6f}s")
        print(f"  Memoized:  {time2:.6f}s")
        print(f"  Iterative: {time3:.6f}s")
        print(
            f"  Speedup:   {time1/time2:.0f}x (memoized), {time1/time3:.0f}x (iterative)"
        )

    demonstrate_memoization_impact()


def practical_recursion_patterns():
    """
    Common Real-world Recursion Patterns
    """

    def file_system_traversal(path, depth=0):
        """Recursive directory traversal"""
        import os

        indent = "  " * depth
        print(f"{indent}{os.path.basename(path)}/")

        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    file_system_traversal(item_path, depth + 1)
                else:
                    print(f"{indent}  {item}")
        except PermissionError:
            print(f"{indent}  [Permission denied]")

    def json_traversal(data, path=""):
        """Recursive JSON traversal"""
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                json_traversal(value, new_path)
        elif isinstance(data, list):
            for i, value in enumerate(data):
                new_path = f"{path}[{i}]"
                json_traversal(value, new_path)
        else:
            print(f"{path}: {data}")

    def backtracking_template(decision_space, path, results):
        """Backtracking recursion template"""
        # Base case: solution found
        if is_solution(path):
            results.append(path.copy())
            return

        # Explore all choices
        for choice in get_choices(decision_space, path):
            if is_valid(choice, path):
                # Make choice
                path.append(choice)

                # Explore recursively
                backtracking_template(decision_space, path, results)

                # Undo choice (backtrack)
                path.pop()

    return file_system_traversal, json_traversal, backtracking_template


def recursive_design_patterns():
    """
    Design Patterns for Effective Recursion
    """

    def divide_and_conquer(data):
        """
        Divide and Conquer Pattern:
        1. Divide problem into subproblems
        2. Conquer subproblems recursively
        3. Combine results
        """
        # Base case: problem is small enough to solve directly
        if len(data) <= 1:
            return data

        # Divide
        mid = len(data) // 2
        left = divide_and_conquer(data[:mid])
        right = divide_and_conquer(data[mid:])

        # Combine (merge in merge sort)
        return merge(left, right)

    def recursive_backtracking(partial_solution, step=0):
        """
        Backtracking Pattern:
        1. Try an option
        2. Recursively explore
        3. Undo if it doesn't work
        """
        # Base case: complete solution
        if step == len(partial_solution):
            return True

        # Try all possibilities
        for option in get_options(partial_solution, step):
            if is_valid(partial_solution, step, option):
                # Make choice
                partial_solution[step] = option

                # Recursively explore
                if recursive_backtracking(partial_solution, step + 1):
                    return True

                # Backtrack (undo choice)
                partial_solution[step] = None

        return False

    return divide_and_conquer, recursive_backtracking


def recursion_anti_patterns():
    """
    Common Recursion Anti-patterns:
    """

    # 1. No base case (infinite recursion)
    def infinite_recursion(n):
        return n + infinite_recursion(n - 1)  # CRASH!

    # 2. Exponential without memoization
    def naive_fibonacci(n):
        if n <= 1:
            return n
        return naive_fibonacci(n - 1) + naive_fibonacci(n - 2)  # O(2^n)

    # 3. Deep recursion for simple problems
    def recursive_sum(n):
        if n == 0:
            return 0
        return n + recursive_sum(n - 1)  # Use iterative instead!

    # 4. Modifying mutable defaults
    def bad_recursion(arr=[]):  # DANGER: mutable default!
        arr.append(1)
        if len(arr) > 5:
            return arr
        return bad_recursion(arr)
