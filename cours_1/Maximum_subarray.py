def Max_subarray(number):
    if len(number)<2:
        return max(number[0], 0)
    M = len(number)//2
    left_max = Max_subarray(number[:M])
    right_max = Max_subarray(number[M:])
    cross_max = number[M]
    for i in [-1,1]:
        attempt = cross_max
        for x in number[M+i::i]:
            attempt+=x
            cross_max = max(cross_max, attempt)
    return max(left_max, right_max, cross_max)
nums = [-2,1,-3,4,-1,2,1,-5,4]
result = Max_subarray(nums)
print("Maximum subarray sum:", result)