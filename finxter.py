jobs = list('ABCDE')
n = len(jobs)
happens_before = [tuple('AB'), tuple('BD'), tuple('DE')]
processors = {0: {}, 1: {}}

def list_scheduler():
    assigned_jobs = []
    for i in range(n):
        next_processor = 0
        min_time = len(processors[0])
        for p in processors:
            if len(processors[p]) < min_time:
                min_time = t

        next_job = jobs[i]
        for k in range(min_time + 1, n):
            if k not in processors[next_processor]:
                processors[next_processor][k] = next_job
