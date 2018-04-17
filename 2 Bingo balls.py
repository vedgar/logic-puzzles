import statistics
def expectmax(n):
    balls = range(1, 1+n)
    results = [b for a in balls for b in balls if a < b]
    return round(statistics.mean(results), 3)
for n in range(2,10):
    print(n, expectmax(n), 2*(n+1)/3, sep='\t')
print(expectmax(75))
