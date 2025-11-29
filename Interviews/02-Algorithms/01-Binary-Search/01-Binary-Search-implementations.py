def binary_search(arr, target):
    """
    Basic iterative binary search implementation

    Args:
        arr: sorted list of elements
        target: element to search for

    Returns:
        index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# Recursive implementation
def binary_search_recursive(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_leftmost(arr, target):
    """Find leftmost occurrence of target"""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def binary_search_rightmost(arr, target):
    """Find rightmost occurrence of target"""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            result = mid
            left = mid + 1  # Continue searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def validated_binary_search(arr, target):
    """Binary search with input validation"""

    # PRECONDITIONS
    if not arr:
        raise ValueError("Array cannot be empty")

    if not all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)):
        raise ValueError("Array must be sorted")

    # MAIN ALGORITHM
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid  # POSTCONDITION: target found at index mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # POSTCONDITION: target not in array


def test_edge_cases():
    test_cases = [
        # (array, target, expected)
        ([1], 1, 0),  # Single element, found
        ([1], 2, -1),  # Single element, not found
        ([], 1, -1),  # Empty array
        ([1, 3, 5], 1, 0),  # Target at beginning
        ([1, 3, 5], 5, 2),  # Target at end
        ([1, 3, 5], 3, 1),  # Target in middle
        ([1, 3, 5], 0, -1),  # Target less than all
        ([1, 3, 5], 6, -1),  # Target greater than all
        ([1, 2, 2, 2, 3], 2, 2),  # Duplicates (behavior depends on variant)
    ]

    for arr, target, expected in test_cases:
        result = binary_search(arr, target)
        assert result == expected, f"Failed for {arr}, target {target}"


def optimized_binary_search(arr, target):
    """Optimized version with reduced comparisons"""
    left, right = 0, len(arr) - 1

    while right - left > 1:
        mid = left + (right - left) // 2  # Avoids overflow

        if arr[mid] < target:
            left = mid
        else:
            right = mid

    # Final comparisons
    if arr[left] == target:
        return left
    if arr[right] == target:
        return right
    return -1


def adaptive_search(arr, target):
    """Adaptive approach based on data characteristics"""

    # For very small arrays, use linear search
    if len(arr) <= 64:
        for i, val in enumerate(arr):
            if val == target:
                return i
        return -1

    # For mostly sequential access patterns
    if is_mostly_sequential_access():
        return interpolation_search(arr, target)

    # Default to binary search
    return binary_search(arr, target)


def interpolation_search(arr, target):
    """Better for uniformly distributed data"""
    left, right = 0, len(arr) - 1

    while left <= right and arr[left] <= target <= arr[right]:
        if left == right:
            return left if arr[left] == target else -1

        # Estimate position using interpolation
        pos = left + ((target - arr[left]) * (right - left)) // (arr[right] - arr[left])

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1

    return -1


import time
import random


def benchmark_searches():
    sizes = [100, 1000, 10000, 100000]

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = random.choice(arr)  # Existing element

        # Time binary search
        start = time.time()
        for _ in range(1000):
            binary_search(arr, target)
        binary_time = time.time() - start

        # Time linear search (for comparison)
        start = time.time()
        for _ in range(1000):
            linear_search(arr, target)
        linear_time = time.time() - start

        print(f"Size {size:6d}: Binary {binary_time:.4f}s, Linear {linear_time:.4f}s")


def linear_search(arr, target):
    """Linear search for comparison"""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
