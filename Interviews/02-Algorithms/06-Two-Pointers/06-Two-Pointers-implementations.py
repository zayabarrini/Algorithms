def two_sum_sorted(arr, target):
    """
    Find two numbers in sorted array that sum to target
    Pointers start at opposite ends
    """
    left, right = 0, len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]

        if current_sum == target:
            return [left, right]  # or return [arr[left], arr[right]]
        elif current_sum < target:
            left += 1  # Need larger sum
        else:
            right -= 1  # Need smaller sum

    return []  # No solution found


def valid_palindrome(s):
    """
    Check if string is palindrome using two pointers
    """
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric characters
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


def container_with_most_water(heights):
    """
    Find maximum area between two lines
    """
    left, right = 0, len(heights) - 1
    max_area = 0

    while left < right:
        # Calculate area
        width = right - left
        height = min(heights[left], heights[right])
        area = width * height
        max_area = max(max_area, area)

        # Move pointer with smaller height
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_area


def remove_duplicates_sorted(arr):
    """
    Remove duplicates from sorted array in-place
    Slow pointer tracks position for next unique element
    """
    if not arr:
        return 0

    slow = 0  # Position for next unique element

    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]

    return slow + 1  # Length of array with duplicates removed


def minimum_window_substring(s, t):
    """
    Find minimum window in s that contains all characters of t
    """
    from collections import Counter

    if not s or not t:
        return ""

    target_count = Counter(t)
    required = len(target_count)
    formed = 0
    window_count = {}

    left = 0
    min_len = float("inf")
    min_window = ""

    for right in range(len(s)):
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1

        # Check if current character completes a requirement
        if char in target_count and window_count[char] == target_count[char]:
            formed += 1

        # Try to contract window from left
        while left <= right and formed == required:
            # Update minimum window
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_window = s[left : right + 1]

            # Remove left character from window
            left_char = s[left]
            window_count[left_char] -= 1
            if (
                left_char in target_count
                and window_count[left_char] < target_count[left_char]
            ):
                formed -= 1

            left += 1

    return min_window


def longest_substring_without_repeating(s):
    """
    Find longest substring without repeating characters
    """
    char_index = {}  # Store last index of each character
    left = 0
    max_length = 0

    for right in range(len(s)):
        current_char = s[right]

        # If character seen before and within current window
        if current_char in char_index and char_index[current_char] >= left:
            left = char_index[current_char] + 1

        char_index[current_char] = right
        max_length = max(max_length, right - left + 1)

    return max_length


def has_cycle(head):
    """
    Detect cycle in linked list using Floyd's Tortoise and Hare
    """
    if not head or not head.next:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False


def find_duplicate_number(nums):
    """
    Find duplicate number in array (Floyd's cycle detection)
    """
    # Phase 1: Find intersection point
    slow = nums[0]
    fast = nums[0]

    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find entrance to cycle
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow


def middle_of_linked_list(head):
    """
    Find middle node of linked list
    """
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow


def merge_sorted_arrays(arr1, arr2):
    """
    Merge two sorted arrays using three pointers
    """
    m, n = len(arr1), len(arr2)
    result = [0] * (m + n)

    i = j = k = 0

    while i < m and j < n:
        if arr1[i] <= arr2[j]:
            result[k] = arr1[i]
            i += 1
        else:
            result[k] = arr2[j]
            j += 1
        k += 1

    # Copy remaining elements
    while i < m:
        result[k] = arr1[i]
        i += 1
        k += 1

    while j < n:
        result[k] = arr2[j]
        j += 1
        k += 1

    return result


def intersection_of_two_arrays(arr1, arr2):
    """
    Find intersection of two sorted arrays
    """
    i = j = 0
    result = []

    while i < len(arr1) and j < len(arr2):
        if arr1[i] == arr2[j]:
            # Avoid duplicates in result
            if not result or result[-1] != arr1[i]:
                result.append(arr1[i])
            i += 1
            j += 1
        elif arr1[i] < arr2[j]:
            i += 1
        else:
            j += 1

    return result


def benchmark_two_pointers():
    """Benchmark different two-pointer patterns"""
    import time
    import random

    # Test data
    sorted_arr = sorted(random.sample(range(100000), 50000))
    large_string = "a" * 100000 + "b" * 100000

    print("Two Pointers Performance:")

    # Opposite ends (Two Sum)
    start = time.time()
    two_sum_sorted(sorted_arr, sorted_arr[0] + sorted_arr[-1])
    opposite_time = time.time() - start
    print(f"Opposite Ends: {opposite_time:.6f}s")

    # Same direction (Remove duplicates)
    start = time.time()
    remove_duplicates_sorted(sorted_arr.copy())
    same_dir_time = time.time() - start
    print(f"Same Direction: {same_dir_time:.6f}s")

    # Fast & slow (Cycle detection simulation)
    start = time.time()
    has_cycle(None)  # Simple case
    fast_slow_time = time.time() - start
    print(f"Fast & Slow: {fast_slow_time:.6f}s")


def space_analysis():
    """
    Space Complexity Details:

    In-place Patterns:
    - Opposite ends: O(1) auxiliary
    - Same direction: O(1) auxiliary
    - Fast & slow: O(1) auxiliary
    - Only use a few integer variables

    Out-of-place Patterns:
    - Multiple arrays: O(m+n) for result
    - Some sliding windows: O(k) for frequency maps

    Memory Optimization:
    - Prefer in-place operations when possible
    - Reuse existing arrays
    - Use generators for large datasets
    """

    def space_optimized_examples():
        # In-place modification (O(1) auxiliary)
        def remove_duplicates_inplace(arr):
            if not arr:
                return 0
            slow = 0
            for fast in range(1, len(arr)):
                if arr[fast] != arr[slow]:
                    slow += 1
                    arr[slow] = arr[fast]
            return slow + 1

        # Out-of-place (O(n) auxiliary)
        def remove_duplicates_new_array(arr):
            return list(set(arr))  # Creates new array

        return remove_duplicates_inplace, remove_duplicates_new_array

    return space_optimized_examples()


def validated_two_sum_sorted(arr, target):
    """
    Two Sum with comprehensive validation
    """
    # PRECONDITIONS
    if not isinstance(arr, list):
        raise TypeError("Input must be a list")

    if len(arr) < 2:
        raise ValueError("Array must have at least 2 elements")

    if not all(isinstance(x, (int, float)) for x in arr):
        raise TypeError("All elements must be numeric")

    # Check if sorted
    if not all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)):
        raise ValueError("Array must be sorted")

    # MAIN ALGORITHM
    left, right = 0, len(arr) - 1

    while left < right:
        # Check for integer overflow (for very large numbers)
        current_sum = arr[left] + arr[right]

        if current_sum == target:
            # POSTCONDITIONS
            assert left != right, "Indices must be different"
            assert 0 <= left < len(arr), "Left index out of bounds"
            assert 0 <= right < len(arr), "Right index out of bounds"
            assert arr[left] + arr[right] == target, "Sum must equal target"

            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    # No solution found
    return []


def safe_sliding_window(s, t):
    """
    Sliding window with input validation
    """
    # PRECONDITIONS
    if s is None or t is None:
        raise ValueError("Input strings cannot be None")

    if not isinstance(s, str) or not isinstance(t, str):
        raise TypeError("Inputs must be strings")

    if len(t) == 0:
        return ""  # Empty pattern matches empty window

    # MAIN ALGORITHM
    from collections import Counter

    target_count = Counter(t)
    required = len(target_count)

    # POSTCONDITIONS (verified during execution)
    left = 0
    formed = 0
    window_count = {}
    min_len = float("inf")
    min_window = ""

    for right in range(len(s)):
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1

        if char in target_count and window_count[char] == target_count[char]:
            formed += 1

        while left <= right and formed == required:
            # Validate window contains all characters of t
            current_window = s[left : right + 1]
            if is_valid_window(current_window, t):
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_window = current_window

            left_char = s[left]
            window_count[left_char] -= 1
            if (
                left_char in target_count
                and window_count[left_char] < target_count[left_char]
            ):
                formed -= 1
            left += 1

    return min_window if min_len != float("inf") else ""


def is_valid_window(window, pattern):
    """Helper to validate window contains pattern"""
    from collections import Counter

    window_count = Counter(window)
    pattern_count = Counter(pattern)

    for char, count in pattern_count.items():
        if window_count.get(char, 0) < count:
            return False
    return True


def test_two_pointer_edge_cases():
    """Comprehensive edge case testing"""

    test_cases = [
        # Two Sum Sorted
        ([1, 2, 3, 4], 7, [2, 3], "Normal case"),
        ([1, 2], 3, [0, 1], "Two elements"),
        ([1, 1], 2, [0, 1], "Duplicate elements"),
        ([1, 2, 3], 10, [], "No solution"),
        ([], 5, [], "Empty array"),
        # Remove Duplicates
        ([1, 1, 2], 2, "Simple duplicates"),
        ([1, 2, 3], 3, "No duplicates"),
        ([1], 1, "Single element"),
        ([], 0, "Empty array"),
        # Valid Palindrome
        ("racecar", True, "Simple palindrome"),
        ("A man, a plan, a canal: Panama", True, "With punctuation"),
        ("", True, "Empty string"),
        ("abc", False, "Not palindrome"),
    ]

    error_cases = [
        (two_sum_sorted, ("not_list", 5), TypeError, "Invalid input type"),
        (two_sum_sorted, ([3, 1, 2], 5), ValueError, "Unsorted array"),
    ]

    print("Testing normal cases:")
    for i, (inputs, expected, description) in enumerate(test_cases):
        try:
            if len(inputs) == 2:  # Two Sum
                arr, target = inputs
                result = two_sum_sorted(arr, target)
                status = "PASS" if result == expected else "FAIL"
            else:  # Other functions
                result = (
                    remove_duplicates_sorted(inputs)
                    if isinstance(inputs, list)
                    else valid_palindrome(inputs)
                )
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


def optimized_two_pointers():
    """
    Optimization techniques for two pointers
    """

    def two_sum_early_termination(arr, target):
        """Early termination when possible"""
        left, right = 0, len(arr) - 1

        while left < right:
            current_sum = arr[left] + arr[right]

            if current_sum == target:
                return [left, right]
            elif current_sum < target:
                left += 1
                # Early check: if smallest possible sum exceeds target
                if left < right and arr[left] + arr[right] > target:
                    break
            else:
                right -= 1
                # Early check: if largest possible sum below target
                if left < right and arr[left] + arr[right] < target:
                    break

        return []

    def sliding_window_optimized(s, t):
        """Optimized sliding window with character skipping"""
        from collections import Counter

        if not s or not t:
            return ""

        target_count = Counter(t)
        required = len(target_count)

        # Preprocessing: filter s to only include characters in t
        filtered_s = []
        for i, char in enumerate(s):
            if char in target_count:
                filtered_s.append((i, char))

        left = 0
        formed = 0
        window_count = {}
        min_len = float("inf")
        min_window = ""

        for right in range(len(filtered_s)):
            char = filtered_s[right][1]
            window_count[char] = window_count.get(char, 0) + 1

            if window_count[char] == target_count[char]:
                formed += 1

            while left <= right and formed == required:
                start_idx = filtered_s[left][0]
                end_idx = filtered_s[right][0]
                current_len = end_idx - start_idx + 1

                if current_len < min_len:
                    min_len = current_len
                    min_window = s[start_idx : end_idx + 1]

                left_char = filtered_s[left][1]
                window_count[left_char] -= 1
                if window_count[left_char] < target_count[left_char]:
                    formed -= 1
                left += 1

        return min_window if min_len != float("inf") else ""

    return two_sum_early_termination, sliding_window_optimized


def adaptive_pointer_strategies():
    """
    Adaptive strategies based on data characteristics
    """

    def adaptive_two_sum(arr, target):
        """Choose strategy based on array characteristics"""
        if len(arr) < 100:
            # For small arrays, brute force might be faster due to constants
            return brute_force_two_sum(arr, target)
        else:
            # For large arrays, use two pointers
            return two_sum_sorted(arr, target)

    def brute_force_two_sum(arr, target):
        """Brute force for small arrays"""
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] + arr[j] == target:
                    return [i, j]
        return []

    def dynamic_sliding_window(s, t):
        """Adjust window strategy based on string lengths"""
        if len(t) > len(s):
            return ""  # No possible solution

        if len(s) < 1000:
            # For small strings, simpler implementation
            return simple_sliding_window(s, t)
        else:
            # For large strings, optimized version
            return minimum_window_substring(s, t)

    def simple_sliding_window(s, t):
        """Simpler implementation for small inputs"""
        from collections import Counter

        target_count = Counter(t)
        min_window = ""

        for i in range(len(s)):
            for j in range(i + len(t), len(s) + 1):
                window = s[i:j]
                window_count = Counter(window)

                # Check if window contains all characters of t
                valid = True
                for char, count in target_count.items():
                    if window_count.get(char, 0) < count:
                        valid = False
                        break

                if valid and (not min_window or len(window) < len(min_window)):
                    min_window = window

        return min_window

    return adaptive_two_sum, dynamic_sliding_window


def cache_performance_analysis():
    """
    Cache Performance Characteristics:

    Opposite Ends Pattern:
    - Excellent cache locality
    - Sequential access from both ends
    - Predictable memory access pattern

    Same Direction Pattern:
    - Good cache locality
    - Sequential forward access
    - Spatial locality benefits

    Fast & Slow Pattern:
    - Variable cache performance
    - Depends on data structure
    - Linked lists have poor locality

    Optimization Tips:
    1. Use arrays over linked lists for better cache performance
    2. Access memory sequentially when possible
    3. Keep working set small to fit in cache
    4. Prefer same-direction patterns for better locality
    """

    def cache_friendly_implementation():
        """Cache-friendly two pointer implementations"""

        def cache_friendly_remove_duplicates(arr):
            """Array-based with sequential access"""
            if not arr:
                return 0

            write_index = 1
            for read_index in range(1, len(arr)):
                if arr[read_index] != arr[read_index - 1]:
                    arr[write_index] = arr[read_index]
                    write_index += 1

            return write_index

        def cache_friendly_two_sum(arr, target):
            """Array-based with predictable access"""
            left, right = 0, len(arr) - 1

            # Prefetch first and last elements
            left_val, right_val = arr[left], arr[right]

            while left < right:
                current_sum = left_val + right_val

                if current_sum == target:
                    return [left, right]
                elif current_sum < target:
                    left += 1
                    left_val = arr[left]  # Sequential access
                else:
                    right -= 1
                    right_val = arr[right]  # Sequential access

            return []

        return cache_friendly_remove_duplicates, cache_friendly_two_sum

    return cache_friendly_implementation()


def practical_two_pointer_applications():
    """
    Real-world Applications and Patterns
    """

    def dutch_national_flag(nums):
        """
        Sort array of 0s, 1s, and 2s in one pass
        Useful for partitioning problems
        """
        low, mid, high = 0, 0, len(nums) - 1

        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:  # nums[mid] == 2
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1

        return nums

    def trap_rain_water(heights):
        """
        Calculate trapped rain water between bars
        """
        if not heights:
            return 0

        left, right = 0, len(heights) - 1
        left_max = right_max = 0
        water = 0

        while left < right:
            if heights[left] < heights[right]:
                if heights[left] >= left_max:
                    left_max = heights[left]
                else:
                    water += left_max - heights[left]
                left += 1
            else:
                if heights[right] >= right_max:
                    right_max = heights[right]
                else:
                    water += right_max - heights[right]
                right -= 1

        return water

    def next_permutation(nums):
        """
        Find next lexicographical permutation
        """
        # Find first decreasing element from right
        i = len(nums) - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        if i >= 0:
            # Find element just larger than nums[i]
            j = len(nums) - 1
            while j >= 0 and nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]

        # Reverse the suffix
        left, right = i + 1, len(nums) - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

        return nums

    def squares_of_sorted_array(nums):
        """
        Return sorted squares of sorted array (may contain negatives)
        """
        n = len(nums)
        result = [0] * n
        left, right = 0, n - 1
        pos = n - 1  # Fill from the end

        while left <= right:
            left_sq = nums[left] * nums[left]
            right_sq = nums[right] * nums[right]

            if left_sq > right_sq:
                result[pos] = left_sq
                left += 1
            else:
                result[pos] = right_sq
                right -= 1
            pos -= 1

        return result

    return (
        dutch_national_flag,
        trap_rain_water,
        next_permutation,
        squares_of_sorted_array,
    )


def two_pointer_design_patterns():
    """
    Common Two Pointer Design Patterns
    """

    def opposite_ends_template(arr, target):
        """
        Template for opposite ends pattern
        """
        left, right = 0, len(arr) - 1

        while left < right:
            # Calculate current state
            current = calculate_current(arr, left, right)

            if meets_condition(current, target):
                return process_solution(left, right)
            elif should_move_left(current, target):
                left += 1
            else:
                right -= 1

        return no_solution_result()

    def same_direction_template(arr):
        """
        Template for same direction pattern
        """
        slow = 0

        for fast in range(len(arr)):
            # Process current fast pointer element
            if should_include(arr, slow, fast):
                # Update slow pointer position
                slow = update_slow_pointer(arr, slow, fast)

        return slow  # or appropriate result

    def fast_slow_template(head):
        """
        Template for fast-slow pattern
        """
        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True  # Cycle detected

        return False

    return opposite_ends_template, same_direction_template, fast_slow_template


def two_pointer_anti_patterns():
    """
    Common Two Pointer Mistakes:
    """

    # 1. Incorrect pointer movement
    def wrong_two_sum(arr, target):
        left, right = 0, len(arr) - 1
        while left < right:
            if arr[left] + arr[right] == target:
                return [left, right]
            # WRONG: always moving both pointers
            left += 1
            right -= 1
        return []

    # 2. Missing bounds checking
    def unsafe_sliding_window(s):
        left = 0
        for right in range(len(s)):
            # Process window
            while condition:  # MISSING: left <= right check
                left += 1  # Could go out of bounds

    # 3. Wrong termination condition
    def infinite_cycle_detection(head):
        slow = fast = head
        while fast:  # WRONG: should check fast and fast.next
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    # 4. Modifying input incorrectly
    def dangerous_inplace_modification(arr):
        slow = 0
        for fast in range(len(arr)):
            if condition:
                arr[slow] = arr[fast]
                slow += 1
        # WRONG: not returning new length or truncating array
        return arr  # Array may have garbage at end
