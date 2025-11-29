# Sliding Window: Complete Guide

## Explanation

**Sliding Window** is a technique that maintains a window (subarray) that slides through the data structure, typically used to solve subarray/substring problems efficiently. The window expands and contracts based on problem constraints.

### Key Concepts:
- **Fixed-size window**: Window maintains constant size
- **Variable-size window**: Window expands/contracts based on conditions
- **Two pointers**: Left and right pointers define window boundaries

## Implementation Patterns

### 1. Fixed-Size Window Pattern

```python
def max_sum_subarray_fixed(arr, k):
    """
    Maximum sum of any contiguous subarray of size k
    Fixed window size
    """
    if len(arr) < k:
        return 0
    
    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(k, len(arr)):
        # Add next element, remove first element of previous window
        window_sum = window_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum

def average_of_subarrays_fixed(arr, k):
    """
    Find averages of all contiguous subarrays of size k
    """
    result = []
    window_sum = 0
    left = 0
    
    for right in range(len(arr)):
        window_sum += arr[right]
        
        # When window reaches size k
        if right >= k - 1:
            result.append(window_sum / k)
            window_sum -= arr[left]
            left += 1
    
    return result

def count_anagrams_in_string(s, p):
    """
    Find all anagrams of string p in string s
    Fixed window size = len(p)
    """
    from collections import Counter
    
    if len(p) > len(s):
        return []
    
    p_count = Counter(p)
    window_count = Counter()
    result = []
    left = 0
    
    for right in range(len(s)):
        # Add current character to window
        window_count[s[right]] += 1
        
        # When window reaches target size
        if right - left + 1 == len(p):
            # Check if window is an anagram
            if window_count == p_count:
                result.append(left)
            
            # Remove left character from window
            window_count[s[left]] -= 1
            if window_count[s[left]] == 0:
                del window_count[s[left]]
            left += 1
    
    return result
```

### 2. Variable-Size Window Pattern

```python
def longest_substring_without_repeating(s):
    """
    Longest substring without repeating characters
    Variable window expands until duplicate found
    """
    char_index = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        current_char = s[right]
        
        # If character is in current window, move left pointer
        if current_char in char_index and char_index[current_char] >= left:
            left = char_index[current_char] + 1
        
        # Update character's latest index
        char_index[current_char] = right
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length

def minimum_window_substring(s, t):
    """
    Find minimum window in s that contains all characters of t
    Variable window that expands and contracts
    """
    from collections import Counter, defaultdict
    
    if not s or not t:
        return ""
    
    target_count = Counter(t)
    required = len(target_count)
    formed = 0
    window_count = defaultdict(int)
    
    left = 0
    min_len = float('inf')
    min_window = ""
    
    for right in range(len(s)):
        char = s[right]
        window_count[char] += 1
        
        # Check if this character completes a requirement
        if char in target_count and window_count[char] == target_count[char]:
            formed += 1
        
        # Try to contract window from left
        while left <= right and formed == required:
            # Update minimum window
            current_len = right - left + 1
            if current_len < min_len:
                min_len = current_len
                min_window = s[left:right + 1]
            
            # Remove left character from window
            left_char = s[left]
            window_count[left_char] -= 1
            if left_char in target_count and window_count[left_char] < target_count[left_char]:
                formed -= 1
            
            left += 1
    
    return min_window if min_len != float('inf') else ""

def longest_substring_with_k_distinct(s, k):
    """
    Longest substring with at most k distinct characters
    """
    if k == 0 or not s:
        return 0
    
    char_count = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Add current character to window
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink window if distinct characters exceed k
        while len(char_count) > k:
            left_char = s[left]
            char_count[left_char] -= 1
            if char_count[left_char] == 0:
                del char_count[left_char]
            left += 1
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### 3. Optimized Sliding Window Patterns

```python
def optimized_sliding_window_patterns():
    """
    Optimized versions with early termination and other improvements
    """
    
    def max_consecutive_ones_iii(nums, k):
        """
        Maximum consecutive ones with at most k zeros flipped
        """
        left = 0
        max_length = 0
        zero_count = 0
        
        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count += 1
            
            # Shrink window if zero count exceeds k
            while zero_count > k:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1
            
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    def permutation_in_string(s1, s2):
        """
        Check if s1's permutation is substring of s2
        """
        from collections import Counter
        
        if len(s1) > len(s2):
            return False
        
        s1_count = Counter(s1)
        window_count = Counter()
        left = 0
        
        for right in range(len(s2)):
            # Add current character
            window_count[s2[right]] += 1
            
            # Maintain window size equal to s1 length
            if right - left + 1 > len(s1):
                # Remove left character
                window_count[s2[left]] -= 1
                if window_count[s2[left]] == 0:
                    del window_count[s2[left]]
                left += 1
            
            # Check if window matches s1 permutation
            if right - left + 1 == len(s1) and window_count == s1_count:
                return True
        
        return False
    
    def fruit_into_baskets(fruits):
        """
        Maximum fruits you can pick (at most 2 types)
        """
        basket = {}
        left = 0
        max_fruits = 0
        
        for right in range(len(fruits)):
            # Add current fruit
            current_fruit = fruits[right]
            basket[current_fruit] = basket.get(current_fruit, 0) + 1
            
            # Shrink window if more than 2 types
            while len(basket) > 2:
                left_fruit = fruits[left]
                basket[left_fruit] -= 1
                if basket[left_fruit] == 0:
                    del basket[left_fruit]
                left += 1
            
            max_fruits = max(max_fruits, right - left + 1)
        
        return max_fruits
    
    return (max_consecutive_ones_iii, permutation_in_string, 
            fruit_into_baskets)
```

### 4. Advanced Sliding Window Patterns

```python
def advanced_sliding_window_patterns():
    """
    Advanced patterns for complex constraints
    """
    
    def subarrays_with_k_distinct(nums, k):
        """
        Count subarrays with exactly k distinct elements
        Uses at_most(k) - at_most(k-1) trick
        """
        def at_most_k_distinct(nums, k):
            count = {}
            left = 0
            result = 0
            
            for right in range(len(nums)):
                # Add current number
                count[nums[right]] = count.get(nums[right], 0) + 1
                
                # Shrink window if distinct count > k
                while len(count) > k:
                    count[nums[left]] -= 1
                    if count[nums[left]] == 0:
                        del count[nums[left]]
                    left += 1
                
                # All subarrays ending at right are valid
                result += right - left + 1
            
            return result
        
        return at_most_k_distinct(nums, k) - at_most_k_distinct(nums, k - 1)
    
    def longest_repeating_character_replacement(s, k):
        """
        Longest substring with same characters after at most k replacements
        """
        char_count = {}
        left = 0
        max_count = 0
        max_length = 0
        
        for right in range(len(s)):
            # Add current character
            char_count[s[right]] = char_count.get(s[right], 0) + 1
            max_count = max(max_count, char_count[s[right]])
            
            # Check if window needs shrinking
            # (window_size - max_count) = number of replacements needed
            while (right - left + 1) - max_count > k:
                char_count[s[left]] -= 1
                left += 1
            
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    def minimum_size_subarray_sum(target, nums):
        """
        Minimal length subarray with sum >= target
        """
        left = 0
        current_sum = 0
        min_length = float('inf')
        
        for right in range(len(nums)):
            current_sum += nums[right]
            
            # Shrink window while condition is satisfied
            while current_sum >= target:
                min_length = min(min_length, right - left + 1)
                current_sum -= nums[left]
                left += 1
        
        return min_length if min_length != float('inf') else 0
    
    return (subarrays_with_k_distinct, longest_repeating_character_replacement,
            minimum_size_subarray_sum)
```

## Time Complexity Analysis

### Comparative Analysis

| Pattern | Best Case | Average Case | Worst Case | In Practice |
|---------|-----------|--------------|------------|-------------|
| **Fixed Window** | Ω(n) | Θ(n) | O(n) | Very efficient, single pass |
| **Variable Window** | Ω(n) | Θ(n) | O(2n) | Each element visited twice |
| **Optimized Variable** | Ω(n) | Θ(n) | O(n) | With clever optimizations |
| **Advanced Patterns** | Ω(n) | Θ(n) | O(n) | Mathematical insights |

### Mathematical Analysis

#### 1. Fixed Window
- Each element visited exactly once
- Constant time operations per element → O(n)

#### 2. Variable Window (Basic)
- Each element visited at most twice (by left and right)
- 2n operations → O(n)

#### 3. Variable Window (HashMap)
- HashMap operations O(1) on average
- Still O(n) overall

#### 4. Advanced Patterns
- Mathematical transformations maintain O(n)
- Clever counting techniques avoid nested loops

### Real-world Performance
```python
def benchmark_sliding_window():
    """Benchmark different sliding window patterns"""
    import time
    import random
    
    # Test data
    large_array = [random.randint(0, 100) for _ in range(100000)]
    large_string = 'a' * 50000 + 'b' * 50000
    
    print("Sliding Window Performance:")
    
    # Fixed window (Max sum subarray)
    start = time.time()
    max_sum_subarray_fixed(large_array, 100)
    fixed_time = time.time() - start
    print(f"Fixed Window: {fixed_time:.6f}s")
    
    # Variable window (Longest substring without repeating)
    start = time.time()
    longest_substring_without_repeating(large_string)
    variable_time = time.time() - start
    print(f"Variable Window: {variable_time:.6f}s")
    
    # Optimized variable window
    start = time.time()
    longest_repeating_character_replacement(large_string, 100)
    optimized_time = time.time() - start
    print(f"Optimized Variable: {optimized_time:.6f}s")
```

## Space Complexity Analysis

### Detailed Breakdown

| Pattern | Auxiliary Space | Total Space | Common Pitfalls |
|---------|-----------------|-------------|-----------------|
| **Fixed Window** | O(1) | O(n) | Only uses running sum and pointers |
| **Variable Window (Basic)** | O(1) | O(n) | Pointer variables only |
| **Variable Window (HashMap)** | O(k) | O(n + k) | k = distinct characters |
| **Advanced Patterns** | O(k) | O(n + k) | Frequency maps |

### Memory Usage Patterns
```python
def space_analysis():
    """
    Space Complexity Details:
    
    Fixed Window Patterns:
    - O(1) auxiliary space: running sums, counters
    - No additional data structures needed
    
    Variable Window with HashMaps:
    - O(k) where k = number of distinct elements
    - In practice, k is often small (26 for lowercase letters)
    
    Memory Optimization Strategies:
    1. Use arrays instead of HashMaps for fixed character sets
    2. Reuse data structures when possible
    3. Use bit manipulation for presence checks
    """
    
    def space_optimized_implementations():
        # Array instead of HashMap for lowercase letters
        def optimized_anagram_search(s, p):
            if len(p) > len(s):
                return []
            
            p_count = [0] * 26
            window_count = [0] * 26
            result = []
            
            # Initialize frequency arrays
            for char in p:
                p_count[ord(char) - ord('a')] += 1
            
            left = 0
            for right in range(len(s)):
                # Add current character
                window_count[ord(s[right]) - ord('a')] += 1
                
                # Maintain window size
                if right - left + 1 > len(p):
                    window_count[ord(s[left]) - ord('a')] -= 1
                    left += 1
                
                # Check if window matches pattern
                if right - left + 1 == len(p) and window_count == p_count:
                    result.append(left)
            
            return result
        
        # Bit manipulation for presence checks
        def optimized_character_presence(s):
            left = 0
            max_length = 0
            bit_mask = 0  # Use bits to track character presence
            
            for right in range(len(s)):
                # Set bit for current character
                char_bit = 1 << (ord(s[right]) - ord('a'))
                
                # If character already in window, move left pointer
                while bit_mask & char_bit:
                    left_char_bit = 1 << (ord(s[left]) - ord('a'))
                    bit_mask &= ~left_char_bit  # Clear left character bit
                    left += 1
                
                bit_mask |= char_bit  # Add current character
                max_length = max(max_length, right - left + 1)
            
            return max_length
        
        return optimized_anagram_search, optimized_character_presence
    
    return space_optimized_implementations()
```

## Correctness & Assumptions

### Input Validation & Preconditions
```python
def validated_sliding_window(func):
    """Decorator for sliding window function validation"""
    def wrapper(*args, **kwargs):
        # Common preconditions for sliding window functions
        if not args:
            raise ValueError("Function requires arguments")
        
        # Extract common parameters
        s, k = None, None
        for arg in args:
            if isinstance(arg, str):
                s = arg
            elif isinstance(arg, int) and arg >= 0:
                k = arg
        
        # Validate string inputs
        if s is not None and not isinstance(s, str):
            raise TypeError("String input must be of type str")
        
        # Validate window size
        if k is not None and k < 0:
            raise ValueError("Window size cannot be negative")
        
        # Check for empty strings where inappropriate
        if 'minimum_window_substring' in func.__name__:
            if not args[0] or not args[1]:
                return ""
        
        try:
            result = func(*args, **kwargs)
            
            # Postcondition validation
            if 'max_sum' in func.__name__:
                assert result is not None, "Result should not be None"
                if len(args[0]) >= args[1]:
                    assert result >= 0, "Maximum sum should be non-negative"
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"Sliding window execution failed: {e}")
    
    return wrapper

@validated_sliding_window
def safe_max_sum_subarray(arr, k):
    """Max sum subarray with comprehensive validation"""
    if not arr or k <= 0:
        return 0
    
    if k > len(arr):
        return sum(arr)  # Or raise error based on requirements
    
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum = window_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    # POSTCONDITIONS
    assert max_sum >= window_sum, "Max sum should be >= any window sum"
    assert max_sum <= sum(arr), "Max sum cannot exceed total array sum"
    
    return max_sum

@validated_sliding_window
def safe_minimum_window_substring(s, t):
    """Minimum window substring with validation"""
    from collections import Counter
    
    # PRECONDITIONS
    if not s or not t:
        return ""
    
    if len(t) > len(s):
        return ""
    
    # MAIN ALGORITHM
    target_count = Counter(t)
    required = len(target_count)
    formed = 0
    window_count = {}
    
    left = 0
    min_len = float('inf')
    min_window = ""
    
    for right in range(len(s)):
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1
        
        if char in target_count and window_count[char] == target_count[char]:
            formed += 1
        
        while left <= right and formed == required:
            current_len = right - left + 1
            
            # POSTCONDITION: Verify window contains all characters of t
            current_window = s[left:right + 1]
            if is_valid_substring(current_window, t):
                if current_len < min_len:
                    min_len = current_len
                    min_window = current_window
            
            left_char = s[left]
            window_count[left_char] -= 1
            if left_char in target_count and window_count[left_char] < target_count[left_char]:
                formed -= 1
            left += 1
    
    return min_window if min_len != float('inf') else ""

def is_valid_substring(window, pattern):
    """Verify window contains all characters of pattern"""
    from collections import Counter
    window_count = Counter(window)
    pattern_count = Counter(pattern)
    
    for char, count in pattern_count.items():
        if window_count.get(char, 0) < count:
            return False
    return True
```

### Edge Cases Testing
```python
def test_sliding_window_edge_cases():
    """Comprehensive edge case testing"""
    
    test_cases = [
        # Fixed Window
        (max_sum_subarray_fixed, ([1, 2, 3, 4, 5], 3), 12, "Normal fixed window"),
        (max_sum_subarray_fixed, ([], 3), 0, "Empty array"),
        (max_sum_subarray_fixed, ([1, 2], 3), 3, "Window larger than array"),
        (max_sum_subarray_fixed, ([-1, -2, -3], 2), -3, "Negative numbers"),
        
        # Variable Window
        (longest_substring_without_repeating, ("abcabcbb",), 3, "Normal case"),
        (longest_substring_without_repeating, ("",), 0, "Empty string"),
        (longest_substring_without_repeating, ("aaaa",), 1, "All same characters"),
        (longest_substring_without_repeating, ("pwwkew",), 3, "With repeats"),
        
        # Minimum Window Substring
        (minimum_window_substring, ("ADOBECODEBANC", "ABC"), "BANC", "Normal case"),
        (minimum_window_substring, ("a", "a"), "a", "Single character match"),
        (minimum_window_substring, ("a", "aa"), "", "No solution"),
        (minimum_window_substring, ("", "abc"), "", "Empty string"),
    ]
    
    error_cases = [
        (max_sum_subarray_fixed, ([1, 2, 3], -1), ValueError, "Negative window size"),
        (max_sum_subarray_fixed, ("not_list", 3), TypeError, "Invalid input type"),
    ]
    
    print("Testing normal cases:")
    for func, args, expected, description in test_cases:
        try:
            result = func(*args)
            status = "PASS" if result == expected else f"FAIL (got {result})"
            print(f"  {description:50}: {status}")
        except Exception as e:
            print(f"  {description:50}: ERROR - {e}")
    
    print("\nTesting error cases:")
    for func, args, expected_error, description in error_cases:
        try:
            func(*args)
            print(f"  {description:50}: FAIL - Should have raised {expected_error}")
        except expected_error:
            print(f"  {description:50}: PASS")
        except Exception as e:
            print(f"  {description:50}: FAIL - Wrong error: {e}")
```

## Practical Considerations

### Optimization Techniques

#### 1. Early Termination & Pruning
```python
def optimized_sliding_window_techniques():
    """
    Optimization techniques for sliding window
    """
    
    def early_termination_max_sum(arr, k):
        """Early termination when possible"""
        if len(arr) < k:
            return sum(arr)
        
        window_sum = sum(arr[:k])
        max_sum = window_sum
        
        # If array length equals window size, we're done
        if len(arr) == k:
            return max_sum
        
        for i in range(k, len(arr)):
            window_sum = window_sum + arr[i] - arr[i - k]
            
            # Early termination if we find theoretical maximum
            if window_sum == max_sum * 2:  # Example condition
                return window_sum
            
            max_sum = max(max_sum, window_sum)
        
        return max_sum
    
    def optimized_character_replacement(s, k):
        """Optimized character replacement with early checks"""
        char_count = [0] * 26
        left = 0
        max_count = 0
        max_length = 0
        
        for right in range(len(s)):
            # Update count and max_count
            idx = ord(s[right]) - ord('A')
            char_count[idx] += 1
            max_count = max(max_count, char_count[idx])
            
            # Early check: if current window can't be improved
            current_length = right - left + 1
            if current_length - max_count <= k:
                max_length = max(max_length, current_length)
            else:
                # Need to shrink window
                left_idx = ord(s[left]) - ord('A')
                char_count[left_idx] -= 1
                left += 1
        
        return max_length
    
    def cache_optimized_min_window(s, t):
        """Cache-optimized minimum window"""
        from collections import defaultdict
        
        if not s or not t:
            return ""
        
        target_count = defaultdict(int)
        for char in t:
            target_count[char] += 1
        
        required = len(target_count)
        formed = 0
        window_count = defaultdict(int)
        
        # Precompute character positions for optimization
        filtered_s = []
        for i, char in enumerate(s):
            if char in target_count:
                filtered_s.append((i, char))
        
        left = 0
        min_len = float('inf')
        min_window = ""
        
        for right in range(len(filtered_s)):
            char = filtered_s[right][1]
            window_count[char] += 1
            
            if window_count[char] == target_count[char]:
                formed += 1
            
            while left <= right and formed == required:
                start = filtered_s[left][0]
                end = filtered_s[right][0]
                current_len = end - start + 1
                
                if current_len < min_len:
                    min_len = current_len
                    min_window = s[start:end + 1]
                
                left_char = filtered_s[left][1]
                window_count[left_char] -= 1
                if window_count[left_char] < target_count[left_char]:
                    formed -= 1
                left += 1
        
        return min_window
    
    return (early_termination_max_sum, optimized_character_replacement,
            cache_optimized_min_window)
```

#### 2. Adaptive Window Strategies
```python
def adaptive_sliding_window_strategies():
    """
    Adaptive strategies based on data characteristics
    """
    
    def adaptive_max_sum(arr, k):
        """Choose strategy based on array size and window size"""
        n = len(arr)
        
        if n <= 1000:
            # For small arrays, simple approach
            return max_sum_subarray_fixed(arr, k)
        elif k <= 100:
            # For small windows, use sliding window
            return max_sum_subarray_fixed(arr, k)
        else:
            # For large windows, consider prefix sums
            prefix_sum = [0] * (n + 1)
            for i in range(n):
                prefix_sum[i + 1] = prefix_sum[i] + arr[i]
            
            max_sum = float('-inf')
            for i in range(k, n + 1):
                current_sum = prefix_sum[i] - prefix_sum[i - k]
                max_sum = max(max_sum, current_sum)
            
            return max_sum
    
    def dynamic_window_strategy(s, t):
        """Dynamic strategy selection for substring problems"""
        if len(t) > len(s):
            return ""
        
        # If t is very small, use simpler approach
        if len(t) <= 3:
            for length in range(len(t), len(s) + 1):
                for i in range(len(s) - length + 1):
                    window = s[i:i + length]
                    if all(window.count(char) >= t.count(char) for char in set(t)):
                        return window
            return ""
        else:
            # Use optimized sliding window for larger t
            return minimum_window_substring(s, t)
    
    def memory_optimized_longest_substring(s):
        """Memory-optimized based on character set size"""
        unique_chars = len(set(s))
        
        if unique_chars <= 26:
            # Use array for better performance
            char_index = [-1] * 128  # ASCII range
            left = 0
            max_length = 0
            
            for right in range(len(s)):
                char_code = ord(s[right])
                
                if char_index[char_code] >= left:
                    left = char_index[char_code] + 1
                
                char_index[char_code] = right
                max_length = max(max_length, right - left + 1)
            
            return max_length
        else:
            # Use dictionary for Unicode support
            return longest_substring_without_repeating(s)
    
    return adaptive_max_sum, dynamic_window_strategy, memory_optimized_longest_substring
```

### Cache Performance Analysis
```python
def cache_performance_analysis():
    """
    Cache Performance Characteristics:
    
    Fixed Window Patterns:
    - Excellent cache locality
    - Sequential memory access
    - Predictable access pattern
    
    Variable Window with Arrays:
    - Good cache performance
    - Sequential or strided access
    - Prefetching works well
    
    Variable Window with HashMaps:
    - Moderate cache performance
    - Random access patterns
    - Cache misses more likely
    
    Optimization Strategies:
    1. Use arrays instead of HashMaps when possible
    2. Access memory sequentially
    3. Keep working set small
    4. Use fixed-size arrays for known character sets
    """
    
    def cache_friendly_implementations():
        """Cache-friendly sliding window implementations"""
        
        def cache_friendly_max_sum(arr, k):
            """Array-based with sequential access"""
            if len(arr) < k:
                return sum(arr)
            
            # Precompute first window
            window_sum = 0
            for i in range(k):
                window_sum += arr[i]
            
            max_sum = window_sum
            
            # Sequential access pattern
            for i in range(k, len(arr)):
                window_sum += arr[i] - arr[i - k]
                if window_sum > max_sum:
                    max_sum = window_sum
            
            return max_sum
        
        def cache_friendly_anagram_search(s, p):
            """Array-based for lowercase letters"""
            if len(p) > len(s):
                return []
            
            # Fixed-size arrays for better cache performance
            p_count = [0] * 26
            window_count = [0] * 26
            result = []
            
            for char in p:
                p_count[ord(char) - ord('a')] += 1
            
            left = 0
            for right in range(len(s)):
                # Sequential array access
                window_count[ord(s[right]) - ord('a')] += 1
                
                if right - left + 1 > len(p):
                    window_count[ord(s[left]) - ord('a')] -= 1
                    left += 1
                
                # Fast array comparison
                if right - left + 1 == len(p) and window_count == p_count:
                    result.append(left)
            
            return result
        
        return cache_friendly_max_sum, cache_friendly_anagram_search
    
    return cache_friendly_implementations()
```

### Real-world Data Patterns
```python
def practical_sliding_window_applications():
    """
    Real-world Applications and Patterns
    """
    
    def stock_buy_sell_max_profit(prices):
        """
        Maximum profit from stock buying and selling (one transaction)
        """
        if not prices:
            return 0
        
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            if price < min_price:
                min_price = price
            else:
                max_profit = max(max_profit, price - min_price)
        
        return max_profit
    
    def find_all_anagrams_optimized(s, p):
        """
        Find all anagrams with optimized character handling
        """
        from collections import defaultdict
        
        if len(p) > len(s):
            return []
        
        p_count = defaultdict(int)
        for char in p:
            p_count[char] += 1
        
        window_count = defaultdict(int)
        result = []
        left = 0
        matches = 0
        
        for right in range(len(s)):
            # Add right character
            char_right = s[right]
            if char_right in p_count:
                window_count[char_right] += 1
                if window_count[char_right] == p_count[char_right]:
                    matches += 1
            
            # Check if window is too large
            if right - left + 1 > len(p):
                char_left = s[left]
                if char_left in p_count:
                    if window_count[char_left] == p_count[char_left]:
                        matches -= 1
                    window_count[char_left] -= 1
                left += 1
            
            # Check for anagram
            if matches == len(p_count):
                result.append(left)
        
        return result
    
    def sliding_window_maximum(nums, k):
        """
        Maximum element in each sliding window (using deque)
        """
        from collections import deque
        
        if not nums or k <= 0:
            return []
        
        result = []
        dq = deque()  # stores indices
        
        for i in range(len(nums)):
            # Remove indices outside current window
            if dq and dq[0] < i - k + 1:
                dq.popleft()
            
            # Remove smaller elements from back
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()
            
            dq.append(i)
            
            # Add to result once window reaches size k
            if i >= k - 1:
                result.append(nums[dq[0]])
        
        return result
    
    def longest_turbulent_subarray(arr):
        """
        Longest turbulent subarray (alternating < and >)
        """
        if len(arr) <= 1:
            return len(arr)
        
        max_length = 1
        left = 0
        
        for right in range(1, len(arr)):
            # Check current comparison
            if arr[right] == arr[right - 1]:
                # Reset window
                left = right
            elif right >= 2:
                # Check if pattern continues
                if (arr[right] > arr[right - 1] and arr[right - 1] > arr[right - 2]) or \
                   (arr[right] < arr[right - 1] and arr[right - 1] < arr[right - 2]):
                    left = right - 1
            
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    return (stock_buy_sell_max_profit, find_all_anagrams_optimized,
            sliding_window_maximum, longest_turbulent_subarray)

def sliding_window_design_patterns():
    """
    Common Sliding Window Design Patterns
    """
    
    def fixed_window_template(arr, k):
        """
        Template for fixed-size window problems
        """
        if len(arr) < k:
            return default_value()
        
        # Initialize first window
        window_value = calculate_initial_window(arr, k)
        result = window_value
        
        for i in range(k, len(arr)):
            # Update window by removing left and adding right
            window_value = update_window(window_value, arr[i], arr[i - k])
            result = update_result(result, window_value)
        
        return result
    
    def variable_window_template(arr, condition):
        """
        Template for variable-size window problems
        """
        left = 0
        result = initial_result()
        window_state = initial_state()
        
        for right in range(len(arr)):
            # Expand window by adding right element
            window_state = expand_window(window_state, arr[right])
            
            # Shrink window while condition is violated
            while left <= right and violates_condition(window_state, condition):
                window_state = shrink_window(window_state, arr[left])
                left += 1
            
            # Update result with current valid window
            if satisfies_condition(window_state, condition):
                result = update_result(result, left, right, window_state)
        
        return result
    
    def optimized_variable_window_template(s, t):
        """
        Template for optimized variable window with frequency maps
        """
        from collections import defaultdict
        
        target_map = build_target_map(t)
        required = len(target_map)
        formed = 0
        window_map = defaultdict(int)
        
        left = 0
        result = initial_result()
        
        for right in range(len(s)):
            char = s[right]
            window_map[char] += 1
            
            if meets_requirement(char, window_map, target_map):
                formed += 1
            
            while formed == required:
                # Update result
                result = update_optimized_result(result, left, right)
                
                # Shrink window
                left_char = s[left]
                window_map[left_char] -= 1
                if breaks_requirement(left_char, window_map, target_map):
                    formed -= 1
                left += 1
        
        return result
    
    return (fixed_window_template, variable_window_template,
            optimized_variable_window_template)
```

## Key Takeaways

### When to Use Sliding Window

| Problem Characteristics | Recommended Pattern | Reason |
|------------------------|---------------------|---------|
| **Contiguous subarray/substring** | Fixed/Variable Window | Natural fit for sequential data |
| **Fixed size constraints** | Fixed Window | Constant window size |
| **Variable size with conditions** | Variable Window | Dynamic window adjustment |
| **Frequency/count constraints** | HashMap + Window | Efficient frequency tracking |
| **Optimization problems** | Variable Window | Find min/max satisfying condition |

### Performance Guidelines

1. **Use fixed window** for constant-size subarray problems
2. **Use variable window** for dynamic constraints and optimization
3. **Prefer arrays over HashMaps** for fixed character sets
4. **Implement early termination** when possible
5. **Consider cache locality** in performance-critical code

### Best Practices

- **Clearly define window invariants** (what must be true at each step)
- **Handle edge cases** before main algorithm
- **Use meaningful variable names** (left/right, window_start/window_end)
- **Validate window conditions** during development
- **Test with corner cases** (empty inputs, minimum/maximum sizes)

### Common Pitfalls to Avoid

```python
def sliding_window_anti_patterns():
    """
    Common Sliding Window Mistakes:
    """
    
    # 1. Incorrect window maintenance
    def wrong_max_sum(arr, k):
        left = 0
        max_sum = 0
        for right in range(len(arr)):
            # WRONG: Not maintaining fixed window size
            current_sum = sum(arr[left:right + 1])
            max_sum = max(max_sum, current_sum)
            # Missing window size maintenance
        return max_sum
    
    # 2. Missing bounds checking
    def unsafe_window_shrink(s):
        left = 0
        for right in range(len(s)):
            while condition:
                left += 1
                # WRONG: No check for left <= right
                # Could cause left > right
    
    # 3. Inefficient window updates
    def inefficient_anagram_search(s, p):
        left = 0
        for right in range(len(s)):
            window = s[left:right + 1]
            # WRONG: Recomputing frequency every time
            if sorted(window) == sorted(p):
                return True
            if len(window) >= len(p):
                left += 1
        return False
    
    # 4. Wrong termination condition
    def incomplete_coverage(arr, target):
        left = 0
        current_sum = 0
        for right in range(len(arr)):
            current_sum += arr[right]
            while current_sum >= target:
                # WRONG: Not updating result for all windows
                left += 1
                current_sum -= arr[left]
        return 0  # Might miss valid windows
```

Sliding Window is a powerful technique for solving subarray and substring problems efficiently. The key is maintaining the correct window invariants and carefully managing the expansion and contraction conditions based on the problem constraints.