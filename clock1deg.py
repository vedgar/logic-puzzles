def span(t):
    angles = t % 60 * 6, t % 3600 / 10, t % 43200 / 120
    return max(angles) - min(angles)

print(min(span(t/10000) for t in range(10000, 43199*10000)))


    

