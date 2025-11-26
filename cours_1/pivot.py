def quicksort(numbers) :
    if len(numbers) < 2:
        return numbers
    pivot = numbers[0]
    A = quicksort([x for x in numbers[1:] if x <= pivot])
    B = quicksort([x for x in numbers[1:] if x > pivot])

    return A +[pivot]+ B
list_numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
sorted_numbers = quicksort(list_numbers)
print("Sorted list:", sorted_numbers)


    