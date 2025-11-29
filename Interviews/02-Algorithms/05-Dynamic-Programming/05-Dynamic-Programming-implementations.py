def fibonacci_naive(n):
    """Naive recursive (exponential time)"""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memo(n, memo=None):
    """Top-down DP with memoization"""
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_tab(n):
    """Bottom-up DP with tabulation"""
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def fibonacci_optimized(n):
    """Space-optimized DP (O(1) space)"""
    if n <= 1:
        return n

    prev2, prev1 = 0, 1
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current

    return prev1


def knapsack_01(weights, values, capacity):
    """
    0/1 Knapsack Problem
    Choose items to maximize value without exceeding capacity
    """
    n = len(weights)

    # dp[i][w] = max value with first i items and capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                # Max of including or excluding current item
                dp[i][w] = max(
                    dp[i - 1][w],  # Exclude item
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],  # Include item
                )
            else:
                dp[i][w] = dp[i - 1][w]  # Can't include this item

    return dp[n][capacity]


def knapsack_01_optimized(weights, values, capacity):
    """Space-optimized knapsack (1D array)"""
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        # Traverse backwards to avoid overwriting
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])

    return dp[capacity]


def longest_common_subsequence(text1, text2):
    """Find length of longest common subsequence"""
    m, n = len(text1), len(text2)

    # dp[i][j] = LCS length of text1[:i] and text2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct the LCS
    lcs = reconstruct_lcs(text1, text2, dp)
    return dp[m][n], lcs


def reconstruct_lcs(text1, text2, dp):
    """Reconstruct the actual LCS string"""
    i, j = len(text1), len(text2)
    result = []

    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            result.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(result))


def coin_change(coins, amount):
    """Minimum coins needed to make amount"""
    # dp[i] = min coins to make amount i
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed for amount 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1


def coin_change_ii(coins, amount):
    """Number of combinations to make amount"""
    # dp[i] = number of combinations to make amount i
    dp = [0] * (amount + 1)
    dp[0] = 1  # Base case: 1 way to make amount 0 (no coins)

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]


def matrix_chain_multiplication(dims):
    """Minimum operations for matrix chain multiplication"""
    n = len(dims) - 1  # Number of matrices
    # dp[i][j] = min operations to multiply matrices i through j
    dp = [[0.0] * n for _ in range(n)]

    # l is chain length
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float("inf")

            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]


def benchmark_dp_algorithms():
    """Benchmark different DP approaches"""
    import time

    # Test Fibonacci
    n = 35
    print(f"Fibonacci({n}):")

    # Naive (exponential - skip for large n)
    if n <= 30:
        start = time.time()
        result = fibonacci_naive(n)
        naive_time = time.time() - start
        print(f"  Naive:      {naive_time:.6f}s")

    # Memoized
    start = time.time()
    result = fibonacci_memo(n)
    memo_time = time.time() - start
    print(f"  Memoized:   {memo_time:.6f}s")

    # Tabulation
    start = time.time()
    result = fibonacci_tab(n)
    tab_time = time.time() - start
    print(f"  Tabulation: {tab_time:.6f}s")

    # Test Knapsack
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5

    print(f"\nKnapsack (capacity {capacity}):")
    start = time.time()
    result = knapsack_01(weights, values, capacity)
    knapsack_time = time.time() - start
    print(f"  Result: {result}, Time: {knapsack_time:.6f}s")


def space_optimization_techniques():
    """
    Space Optimization Strategies:
    """

    # 1. State Reduction
    def optimized_fibonacci(n):
        """Only keep previous two states"""
        if n <= 1:
            return n
        prev2, prev1 = 0, 1
        for i in range(2, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current
        return prev1

    # 2. Rolling Arrays
    def knapsack_rolling_array(weights, values, capacity):
        """Use 2 rows instead of full table"""
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(2)]

        for i in range(1, n + 1):
            curr, prev = i % 2, (i - 1) % 2
            for w in range(1, capacity + 1):
                if weights[i - 1] <= w:
                    dp[curr][w] = max(
                        dp[prev][w], values[i - 1] + dp[prev][w - weights[i - 1]]
                    )
                else:
                    dp[curr][w] = dp[prev][w]

        return dp[n % 2][capacity]

    # 3. Further compression to 1D
    def knapsack_1d(weights, values, capacity):
        """Single array with backward traversal"""
        dp = [0] * (capacity + 1)
        for i in range(len(weights)):
            for w in range(capacity, weights[i] - 1, -1):
                dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
        return dp[capacity]

    return optimized_fibonacci, knapsack_rolling_array, knapsack_1d


def validated_dp_function(func):
    """Decorator for DP function validation"""

    def wrapper(*args, **kwargs):
        # Common DP preconditions
        if not args:
            raise ValueError("Function requires arguments")

        # Check for negative values
        if "amount" in kwargs and kwargs["amount"] < 0:
            raise ValueError("Amount cannot be negative")

        # Check for empty inputs
        if "coins" in kwargs and not kwargs["coins"]:
            raise ValueError("Coins list cannot be empty")

        try:
            result = func(*args, **kwargs)

            # Postcondition validation
            if "fibonacci" in func.__name__:
                assert result >= 0, "Fibonacci result must be non-negative"

            if "knapsack" in func.__name__:
                assert result >= 0, "Knapsack value must be non-negative"

            return result

        except RecursionError:
            raise RecursionError("DP recursion depth exceeded")
        except MemoryError:
            raise MemoryError("DP table too large for memory")

    return wrapper


@validated_dp_function
def safe_coin_change(coins, amount):
    """Coin change with validation"""
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if amount == 0:
        return 0

    # Remove invalid coins
    coins = [coin for coin in coins if coin > 0]

    if not coins:
        return -1

    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for i in range(coin, amount + 1):
            if dp[i - coin] != float("inf"):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1


def test_dp_edge_cases():
    """Comprehensive edge case testing for DP algorithms"""

    test_cases = [
        # Fibonacci
        (fibonacci_tab, (0,), 0, "Fibonacci(0)"),
        (fibonacci_tab, (1,), 1, "Fibonacci(1)"),
        # Coin Change
        (coin_change, ([1, 2, 5], 0), 0, "Coin change amount 0"),
        (coin_change, ([2], 3), -1, "Coin change impossible"),
        (coin_change, ([1], 1), 1, "Coin change single coin"),
        # Knapsack
        (knapsack_01, ([], [], 10), 0, "Empty knapsack"),
        (knapsack_01, ([1, 2], [3, 4], 0), 0, "Zero capacity"),
        # LCS
        (longest_common_subsequence, ("", "abc"), (0, ""), "Empty string LCS"),
        (longest_common_subsequence, ("abc", "abc"), (3, "abc"), "Identical strings"),
    ]

    error_cases = [
        (fibonacci_tab, (-1,), ValueError, "Negative Fibonacci"),
        (coin_change, ([1, 2, 3], -5), ValueError, "Negative amount"),
    ]

    print("Testing normal cases:")
    for func, args, expected, description in test_cases:
        try:
            result = func(*args)
            if isinstance(expected, tuple):
                status = "PASS" if result == expected else "FAIL"
            else:
                status = "PASS" if result == expected else "FAIL"
            print(f"  {description:40}: {status}")
        except Exception as e:
            print(f"  {description:40}: ERROR - {e}")

    print("\nTesting error cases:")
    for func, args, expected_error, description in error_cases:
        try:
            func(*args)
            print(f"  {description:40}: FAIL - Should have raised {expected_error}")
        except expected_error:
            print(f"  {description:40}: PASS")
        except Exception as e:
            print(f"  {description:40}: FAIL - Wrong error: {e}")


from functools import lru_cache
import functools


def memoize(func):
    """Custom memoization decorator"""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


# Built-in memoization
@lru_cache(maxsize=None)
def fibonacci_builtin_memo(n):
    if n <= 1:
        return n
    return fibonacci_builtin_memo(n - 1) + fibonacci_builtin_memo(n - 2)


def state_compression_examples():
    """
    Techniques for reducing state space:
    """

    # 1. Bitmask DP for subset problems
    def subset_sum_bitmask(nums, target):
        """Subset sum using bitmask DP"""
        n = len(nums)
        dp = [False] * (1 << n)
        dp[0] = True

        for mask in range(1 << n):
            if not dp[mask]:
                continue
            current_sum = sum(nums[i] for i in range(n) if mask & (1 << i))
            for i in range(n):
                if not (mask & (1 << i)) and current_sum + nums[i] <= target:
                    new_mask = mask | (1 << i)
                    dp[new_mask] = True
                    if current_sum + nums[i] == target:
                        return True
        return False

    # 2. Sliding window optimization
    def sliding_window_dp(arr, k):
        """DP with sliding window optimization"""
        n = len(arr)
        if n == 0:
            return 0

        # Only keep last k states
        dp = [0] * n
        dp[0] = arr[0]

        for i in range(1, n):
            # Look back only k steps
            start = max(0, i - k)
            dp[i] = arr[i] + max(dp[start:i] or [0])

        return max(dp)

    return subset_sum_bitmask, sliding_window_dp


def cache_performance_analysis():
    """
    Cache Performance Characteristics:

    Memoization (Top-down):
    - Pros: Only computes needed subproblems, clean code
    - Cons: Recursion overhead, stack depth limits

    Tabulation (Bottom-up):
    - Pros: Better cache locality, no recursion overhead
    - Cons: Computes all subproblems, may compute unused states

    Memory Access Patterns:
    - Row-major vs column-major traversal
    - Cache-friendly: Sequential memory access
    - Cache-unfriendly: Random access patterns

    Optimization Tips:
    1. Use iterative DP for better cache performance
    2. Arrange loops for sequential memory access
    3. Use space-optimized versions to fit in cache
    4. Prefer arrays over hash tables for better locality
    """

    def cache_friendly_knapsack(weights, values, capacity):
        """Cache-friendly knapsack implementation"""
        n = len(weights)
        dp = [0] * (capacity + 1)

        # Sequential memory access pattern
        for i in range(n):
            # Backward traversal to avoid cache conflicts
            for w in range(capacity, weights[i] - 1, -1):
                if dp[w] < values[i] + dp[w - weights[i]]:
                    dp[w] = values[i] + dp[w - weights[i]]

        return dp[capacity]

    return cache_friendly_knapsack


def practical_dp_applications():
    """
    Real-world DP Applications and Patterns
    """

    def edit_distance(word1, word2):
        """Minimum edit distance between two strings"""
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize base cases
        for i in range(m + 1):
            dp[i][0] = i  # Delete all characters
        for j in range(n + 1):
            dp[0][j] = j  # Insert all characters

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]  # No cost
                else:
                    dp[i][j] = min(
                        dp[i - 1][j] + 1,  # Delete
                        dp[i][j - 1] + 1,  # Insert
                        dp[i - 1][j - 1] + 1,  # Replace
                    )

        return dp[m][n]

    def longest_increasing_subsequence(nums):
        """Longest increasing subsequence"""
        if not nums:
            return 0

        n = len(nums)
        dp = [1] * n  # Each element is a subsequence of length 1

        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)

    def word_break(s, word_dict):
        """Check if string can be segmented into dictionary words"""
        word_set = set(word_dict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True  # Empty string can be segmented

        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break

        return dp[n]

    return edit_distance, longest_increasing_subsequence, word_break


def dp_design_patterns():
    """
    Common DP Design Patterns
    """

    def sequence_dp_pattern(sequence):
        """
        Pattern for sequence problems (LIS, LCS, etc.)
        dp[i] = best solution ending at position i
        """
        n = len(sequence)
        dp = [1] * n  # or appropriate initialization

        for i in range(n):
            for j in range(i):
                if is_valid_transition(sequence, j, i):
                    dp[i] = update_state(dp[i], dp[j])

        return max(dp) if dp else 0

    def interval_dp_pattern(intervals):
        """
        Pattern for interval problems (matrix chain, etc.)
        dp[i][j] = best solution for interval i to j
        """
        n = len(intervals)
        dp = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float("inf")

                for k in range(i, j):
                    dp[i][j] = min(
                        dp[i][j], dp[i][k] + dp[k + 1][j] + cost(intervals, i, k, j)
                    )

        return dp[0][n - 1]

    def two_sequence_dp_pattern(seq1, seq2):
        """
        Pattern for two-sequence problems (edit distance, etc.)
        dp[i][j] = best solution for seq1[:i] and seq2[:j]
        """
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize boundaries
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i - 1] == seq2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

        return dp[m][n]

    return sequence_dp_pattern, interval_dp_pattern, two_sequence_dp_pattern


def dp_anti_patterns():
    """
    Common DP Mistakes:
    """

    # 1. Wrong state definition
    def wrong_fibonacci(n):
        if n <= 1:
            return n
        # Missing memoization - exponential time!
        return wrong_fibonacci(n - 1) + wrong_fibonacci(n - 2)

    # 2. Incorrect base cases
    def wrong_coin_change(coins, amount):
        dp = [float("inf")] * (amount + 1)
        dp[0] = 1  # WRONG: should be 0 coins for amount 0
        # ... rest of implementation

    # 3. Wrong loop order
    def wrong_knapsack(weights, values, capacity):
        dp = [0] * (capacity + 1)
        for w in range(capacity + 1):  # WRONG ORDER!
            for i in range(len(weights)):
                if weights[i] <= w:
                    dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
        # This allows using same item multiple times!

    # 4. Not handling impossible cases
    def incomplete_coin_change(coins, amount):
        dp = [0] * (amount + 1)
        # Missing check for impossible amounts
        return dp[amount]  # Could return 0 for impossible case
