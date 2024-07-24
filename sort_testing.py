n = int(input(f"Enter the desired number of elements: "))

global_number_list = [i for i in range(1, n + 1)]

comparison_count = 0

swap_count = 0


def enhanced_quick_sort(lower_bound, upper_bound):
    def median_of_three(arr, low, high):
        mid = (low + high) // 2
        a, b, c = arr[low], arr[mid], arr[high]
        if a > b:
            a, b = b, a
        if a > c:
            a, c = c, a
        if b > c:
            b, c = c, b
        return b

    def partition(low, high):
        pivot_value = median_of_three(global_number_list, low, high)
        left = low
        right = high

        while left <= right:
            # Move left index to the right as long as it points to values less than the pivot
            while global_number_list[left] < pivot_value:
                left += 1
                comparison_count += 1
            # Move right index to the left as long as it points to values greater than the pivot
            while global_number_list[right] > pivot_value:
                right -= 1
                comparison_count += 1
            # If indices have not crossed, swap the elements
            if left <= right:
                global_number_list[left], global_number_list[right] = global_number_list[right], global_number_list[
                    left]
                left += 1
                right -= 1

        return left

    global global_number_list, comparison_count, swap_count

    if lower_bound < upper_bound:
        number_list = global_number_list[lower_bound:upper_bound + 1]
        pivot = median_of_three(number_list, 0, len(number_list) - 1)
        first_half = []
        second_half = []

        for i in range(len(number_list) - 1):
            comparison_count += 1
            if number_list[i] <= pivot:
                first_half.append(number_list[i])
            else:
                second_half.append(number_list[i])

        global_number_list[lower_bound:upper_bound + 1] = first_half + [pivot] + second_half

        pivot_index = lower_bound + len(first_half)

        enhanced_quick_sort(lower_bound, pivot_index - 1)
        enhanced_quick_sort(pivot_index + 1, upper_bound)

#