activity = tuple[int, int] # (start_time, end_time)

def activity_selection(activities: list[activity]) -> list[activity]:
    time = 0
    res = []
    activities.sort(key=lambda a : a[1])
    for start, end in activities:
        if time <= start :
            res.append((start,end))
            time = end
    return res

print(activity_selection([(0, 3), (1, 4), (5, 7)]))