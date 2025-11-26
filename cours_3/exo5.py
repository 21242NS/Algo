job = tuple[int, int, int] # (id, deadline, profit)

def job_sequencing(jobs: list[job]) -> list[int | None]:
    jobs.sort(key=lambda a:(a[1],-a[2]))
    res = []
    for job in jobs:
        if len(res)==0:
            res.append(job)
        else : 
            for i in range(len(res)) :
                if res[i][1]==job[1]:
                    if res[i][2]<job[2]:
                        res.pop(i)
                        res.insert(i, job)
                        break
                    else :
                        break
                else :
                    if job not in res:
                        res.append(job)
    return res

print(job_sequencing([(0, 4, 20), (1, 1, 10), (2, 1, 40), (3, 2, 30), (4, 6, 100)]))