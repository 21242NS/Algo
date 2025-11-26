def find_max_min(numbers):
    if len (numbers)==1:
        return numbers[0], numbers[0]
    M = len(numbers)//2
    A = find_max_min(numbers[:M])
    B = find_max_min(numbers[M:])
    
   
    return min(A[0],B[0]), max(A[1],B[1])
list_numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
minimum, maximum = find_max_min(list_numbers)
result = maximum - minimum
print("Difference between max and min:", result)
print("Minimum:", minimum)
print("Maximum:", maximum)