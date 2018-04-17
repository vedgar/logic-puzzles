# https://arachnoid.com/randomness/equities_simulation_listing.html

import random

investor_count = 10 ** 5
initial_balance = 10 ** 4
delta = .05  # maximum price change per period
years = 20
year_periods = 52

growth_factor = 1 + .12 / year_periods
random.seed(12345)
investors = [initial_balance] * investor_count
bh_balance = initial_balance

for y in range(years):
    for w in range(year_periods):
        print(end='.')
        bh_balance *= growth_factor
        for i in range(len(investors)):
            investors[i] *= 1 + random.uniform(-1, 1) * delta * growth_factor
    print()
    
millionaires = sum(b >= 1e6 for b in investors)
winners = sum(b > bh_balance for b in investors)
losers = sum(b < bh_balance for b in investors)
worst = min(investors)
best = max(investors)
print(f"{investor_count} investors, initial balance ${initial_balance:.2f}")
print(f"Buy & hold ${bh_balance:.2f}, worst ${worst:.2f}, best ${best:.2f}")
print(f"{millionaires} millionaires, {winners} winners, {losers} losers")
