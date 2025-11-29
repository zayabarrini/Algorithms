# Sorting Algorithms: Complete Guide

## Explanation

Sorting is the process of arranging elements in a specific order (typically ascending or descending). Different sorting algorithms use various strategies with different time/space tradeoffs.

## Common Sorting Algorithms

### 1. Bubble Sort
**Strategy**: Repeatedly swap adjacent elements if they are in wrong order

```python
def bubble_sort(arr):
    """
    Bubble Sort Implementation
    Time: O(n²) | Space: O(1)
    """
    n = len(arr)
    
    for i in range(n):
        # Last i elements are already in place
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swapping, array is sorted
        if not swapped:
            break
    return arr
```

### 2. Selection Sort
**Strategy**: Find minimum element and place it at beginning

```python
def selection_sort(arr):
    """
    Selection Sort Implementation
    Time: O(n²) | Space: O(1)
    """
    n = len(arr)
    
    for i in range(n):
        # Find minimum element in remaining unsorted array
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap the found minimum with first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr
```

### 3. Insertion Sort
**Strategy**: Build sorted array one element at a time

```python
def insertion_sort(arr):
    """
    Insertion Sort Implementation
    Time: O(n²) | Space: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move elements greater than key one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
    return arr
```

### 4. Merge Sort
**Strategy**: Divide and conquer - split, sort, merge

```python
def merge_sort(arr):
    """
    Merge Sort Implementation
    Time: O(n log n) | Space: O(n)
    """
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer (merge)
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### 5. Quick Sort
**Strategy**: Divide and conquer using pivot element

```python
def quick_sort(arr):
    """
    Quick Sort Implementation
    Time: O(n log n) average, O(n²) worst | Space: O(log n)
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]  # Choose middle element as pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# In-place version (better space complexity)
def quick_sort_inplace(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition and get pivot index
        pi = partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        quick_sort_inplace(arr, low, pi - 1)
        quick_sort_inplace(arr, pi + 1, high)
    
    return arr

def partition(arr, low, high):
    pivot = arr[high]  # Choose last element as pivot
    i = low - 1  # Index of smaller element
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

### 6. Heap Sort
**Strategy**: Use heap data structure to sort

```python
def heap_sort(arr):
    """
    Heap Sort Implementation
    Time: O(n log n) | Space: O(1)
    """
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)
    
    return arr

def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    left = 2 * i + 1
    right = 2 * i + 2
    
    # If left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # If right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # Change root if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
```

## Time Complexity Analysis

### Comparative Analysis

| Algorithm | Best Case | Average Case | Worst Case | In Practice |
|-----------|-----------|--------------|------------|-------------|
| **Bubble Sort** | Ω(n) | Θ(n²) | O(n²) | Good for small, nearly sorted data |
| **Selection Sort** | Ω(n²) | Θ(n²) | O(n²) | Good for small arrays, minimal swaps |
| **Insertion Sort** | Ω(n) | Θ(n²) | O(n²) | Excellent for small/partially sorted data |
| **Merge Sort** | Ω(n log n) | Θ(n log n) | O(n log n) | Consistent, good for large datasets |
| **Quick Sort** | Ω(n log n) | Θ(n log n) | O(n²) | Fastest in practice, good cache performance |
| **Heap Sort** | Ω(n log n) | Θ(n log n) | O(n log n) | Guaranteed O(n log n), in-place |

### Mathematical Insights

**O(n²) algorithms**: 
- Bubble: n + (n-1) + ... + 1 = n(n-1)/2 ≈ n²/2 comparisons
- Selection: Always n(n-1)/2 comparisons
- Insertion: Best case n-1, worst case n(n-1)/2 comparisons

**O(n log n) algorithms**:
- Merge Sort: Height log n, each level processes n elements
- Quick Sort: Average case splits array in half each time
- Heap Sort: Building heap O(n), each extraction O(log n)

### Real-world Performance
```python
import time
import random

def benchmark_sorts():
    sizes = [100, 1000, 5000, 10000]
    
    for size in sizes:
        arr = [random.randint(1, 1000) for _ in range(size)]
        
        algorithms = {
            'Bubble': bubble_sort,
            'Selection': selection_sort, 
            'Insertion': insertion_sort,
            'Merge': merge_sort,
            'Quick': quick_sort,
            'Heap': heap_sort
        }
        
        print(f"\nArray size: {size}")
        for name, algo in algorithms.items():
            test_arr = arr.copy()
            start = time.time()
            algo(test_arr)
            elapsed = time.time() - start
            print(f"{name:10}: {elapsed:.4f}s")
```

## Space Complexity Analysis

### Detailed Breakdown

| Algorithm | Auxiliary Space | Total Space | Common Pitfalls |
|-----------|-----------------|-------------|-----------------|
| **Bubble Sort** | O(1) | O(n) | In-place, minimal memory |
| **Selection Sort** | O(1) | O(n) | In-place, only needs temp variables |
| **Insertion Sort** | O(1) | O(n) | In-place, good for memory-constrained |
| **Merge Sort** | O(n) | O(n) | Needs auxiliary array, not in-place |
| **Quick Sort** | O(log n) | O(n) | Recursion stack, worst case O(n) |
| **Heap Sort** | O(1) | O(n) | In-place, modifies original array |

### Memory Usage Patterns
```python
def memory_analysis():
    """
    Memory usage patterns:
    
    In-place sorts (Bubble, Selection, Insertion, Heap):
    - Modify original array
    - O(1) auxiliary space
    - Good for large datasets
    
    Out-of-place sorts (Merge):
    - Create new arrays
    - O(n) auxiliary space  
    - Preserves original data
    
    Quick Sort:
    - In-place but uses recursion stack
    - Average O(log n), worst O(n) stack depth
    """
    pass
```

## Correctness & Assumptions

### Input Validation
```python
def validated_sort(arr, algorithm):
    """
    Sorting with comprehensive input validation
    """
    # PRECONDITIONS
    if not isinstance(arr, list):
        raise TypeError("Input must be a list")
    
    if not all(isinstance(x, (int, float)) for x in arr):
        raise TypeError("All elements must be numeric")
    
    if len(arr) == 0:
        return arr  # Empty array is sorted
    
    # MAIN SORTING
    result = algorithm(arr.copy())  # Don't modify original
    
    # POSTCONDITIONS
    assert len(result) == len(arr), "Length must be preserved"
    assert all(result[i] <= result[i+1] for i in range(len(result)-1)), "Must be sorted"
    
    return result
```

### Edge Cases Testing
```python
def test_edge_cases():
    """Comprehensive edge case testing"""
    
    test_cases = [
        [],                    # Empty array
        [1],                   # Single element
        [1, 1, 1],            # All duplicates
        [5, 4, 3, 2, 1],      # Reverse sorted
        [1, 2, 3, 4, 5],      # Already sorted
        [1, 3, 2],            # Small unsorted
        [float('inf'), 1, -float('inf')],  # Extreme values
        [1, 2, 3, 2, 1],      # With duplicates
    ]
    
    algorithms = [bubble_sort, selection_sort, insertion_sort, 
                  merge_sort, quick_sort, heap_sort]
    
    for i, test_arr in enumerate(test_cases):
        print(f"\nTest case {i+1}: {test_arr}")
        
        for algo in algorithms:
            try:
                result = algo(test_arr.copy())
                is_sorted = all(result[j] <= result[j+1] for j in range(len(result)-1))
                print(f"{algo.__name__:15}: {'PASS' if is_sorted else 'FAIL'}")
            except Exception as e:
                print(f"{algo.__name__:15}: ERROR - {e}")
```

## Practical Considerations

### Constant Factors & Optimization
```python
def optimized_insertion_sort(arr):
    """Optimized insertion sort with sentinel and binary search"""
    if len(arr) <= 1:
        return arr
    
    # Find minimum and place at beginning (sentinel)
    min_idx = 0
    for i in range(1, len(arr)):
        if arr[i] < arr[min_idx]:
            min_idx = i
    arr[0], arr[min_idx] = arr[min_idx], arr[0]
    
    # Insertion sort with sentinel
    for i in range(2, len(arr)):
        key = arr[i]
        
        # Binary search for insertion position
        left, right = 0, i
        while left < right:
            mid = (left + right) // 2
            if key < arr[mid]:
                right = mid
            else:
                left = mid + 1
        
        # Shift elements
        for j in range(i, left, -1):
            arr[j] = arr[j - 1]
        arr[left] = key
    
    return arr
```

### Cache Performance Analysis
```python
def cache_analysis():
    """
    Cache Performance Characteristics:
    
    Good Cache Performance:
    - Insertion Sort: Sequential access pattern
    - Merge Sort: Sequential merges
    - Quick Sort: Good locality in partitioning
    
    Poor Cache Performance:
    - Selection Sort: Random access for min element
    - Heap Sort: Random access in heap operations
    
    Hybrid Approach (Timsort used in Python):
    - Use insertion sort for small chunks
    - Use merge sort for combining chunks
    - Exploits natural runs in data
    """
    pass
```

### Real-world Data Patterns
```python
def adaptive_sort(arr):
    """Choose sorting algorithm based on data characteristics"""
    
    n = len(arr)
    
    # Very small arrays
    if n <= 10:
        return insertion_sort(arr)
    
    # Check if already sorted
    if all(arr[i] <= arr[i+1] for i in range(n-1)):
        return arr  # Already sorted
    
    # Check if reverse sorted
    if all(arr[i] >= arr[i+1] for i in range(n-1)):
        return arr[::-1]  # Reverse
    
    # Check for many duplicates
    unique_ratio = len(set(arr)) / n
    if unique_ratio < 0.1:  # Many duplicates
        return counting_sort(arr) if min(arr) >= 0 else merge_sort(arr)
    
    # Default to quick sort for general case
    return quick_sort(arr)

def counting_sort(arr):
    """Efficient for integers with small range"""
    if not arr:
        return arr
    
    min_val, max_val = min(arr), max(arr)
    count = [0] * (max_val - min_val + 1)
    
    for num in arr:
        count[num - min_val] += 1
    
    result = []
    for i, freq in enumerate(count):
        result.extend([i + min_val] * freq)
    
    return result
```

## Hybrid Algorithms & Modern Approaches

### Timsort (Python's built-in sort)
```python
def timsort_analysis():
    """
    Timsort - Python's built-in sorting algorithm:
    
    Key Features:
    - Hybrid of Merge Sort and Insertion Sort
    - Finds natural "runs" (already sorted sequences)
    - Uses insertion sort for small chunks (< 64 elements)
    - Stable sort (preserves order of equal elements)
    - Adaptive to real-world data patterns
    
    Performance:
    - Best case: O(n) for already sorted data
    - Average case: O(n log n)
    - Worst case: O(n log n)
    - Space: O(n) auxiliary
    """
    pass

# Using Python's built-in sort (Timsort)
def python_builtin_sort(arr):
    return sorted(arr)  # Uses Timsort

# In-place version
arr.sort()  # Also Timsort
```

## Key Takeaways

### When to Use Which Algorithm

| Scenario | Recommended Algorithm | Reason |
|----------|---------------------|---------|
| **Small arrays (< 50)** | Insertion Sort | Low constant factors, adaptive |
| **Nearly sorted data** | Insertion Sort | O(n) best case, minimal operations |
| **Large arrays, general case** | Quick Sort | Fast average case, good cache performance |
| **Guaranteed O(n log n)** | Merge Sort/Heap Sort | Consistent performance |
| **Memory constrained** | Heap Sort | O(1) auxiliary space |
| **Stability required** | Merge Sort/Insertion Sort | Preserves equal element order |
| **Integers with small range** | Counting Sort | O(n + k) time |

### Best Practices
1. **Use built-in sort** for most applications (highly optimized)
2. **Consider data characteristics** when choosing algorithm
3. **Profile with real data** - theoretical complexity ≠ real performance
4. **Consider stability** if equal elements should maintain order
5. **Memory constraints** may dictate algorithm choice

### Performance Rules of Thumb
- **n < 50**: Simple O(n²) sorts often faster due to constants
- **50 < n < 1000**: Quick Sort generally fastest
- **n > 1000**: Merge/Heap Sort for guaranteed O(n log n)
- **Special cases**: Use specialized algorithms (Counting, Radix for integers)