def maximum_local(lst):
    M = len(lst)//2
    if lst[M-2]>lst[M-1]:
        return maximum_local(lst[:M])
    elif lst[M-1]<lst[M]:
        return maximum_local(lst[M:])
    elif lst[M-2]<lst[M-1]>lst[M]:
        result = lst[M-1]
        return M, result
    
test=[1,3,7,9,10,11,8,7,12,8,2]
(index, value) = maximum_local(test)
print("Index of local maximum:", index)
print("Value of local maximum:", value)


    