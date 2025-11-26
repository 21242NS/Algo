coins = [1, 2, 5, 10, 20, 50, 100, 200]
def change(value: int) -> list[int]:
    result = []
    for coin in reversed(coins):#O(n log(n))
        if value >= coin: #O(n)
            n = value // coin
            value -= n * coin
            result.extend([coin] * n)
    return result
# complexity O(n log(n))
print(change(455))