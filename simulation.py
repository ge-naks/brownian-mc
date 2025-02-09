import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

def gen_wealth(initial_wealth, T, dT, a, b, ceiling):
    periods_survived = int(T / dT)
    wealth = np.zeros(periods_survived)
    wealth[0] = initial_wealth
    overflow = 0
    noise = np.random.normal(0, np.sqrt(dT), periods_survived)
    for i in range(1, periods_survived):
        dX = a * dT + b * noise[i]
        curr_wealth = wealth[i - 1] + dX

        if curr_wealth > ceiling:
            overflow += curr_wealth - ceiling
            curr_wealth = ceiling
            wealth[i] = curr_wealth
        elif 0 < curr_wealth < ceiling:
            wealth[i] = curr_wealth
        else:
            periods_survived = i
            break
    return [wealth, periods_survived, overflow]

def gen_one_plt(initial_wealth, T, dT, a, b, ceiling):
    wealth, periods_survived, overflow = gen_wealth(initial_wealth, T, dT, a, b, ceiling)
    time = [i for i in range(int(T / dT))]
    plt.suptitle(f'Parameters of a = {a}, b = {b}, ceiling = {ceiling}')
    plt.title(f'Survived {periods_survived} periods and generated {round(overflow, 3)} overflow')
    plt.xlabel("Time")
    plt.ylabel("Wealth")
    plt.plot(time, wealth)
    plt.show()
    return overflow


def optimize_ceiling(initial_wealth, T, dT, a, b, N, max_ceiling = 100, ceiling_step = .1):
    ceilings = [i * ceiling_step for i in range(max_ceiling)]
    overflow_per_ceiling = np.zeros(max_ceiling)
    survival_per_ceiling = np.zeros(max_ceiling)
    optimal_ceiling = 0
    avg_over_at_opt = 0
    for i in range(len(ceilings)):
        curr_ceiling_overflow = 0
        curr_ceiling_survival = 0
        for _ in range(N):
            iter_result = gen_wealth(initial_wealth, T, dT, a, b, ceilings[i])
            curr_ceiling_overflow += iter_result[2]
            curr_ceiling_survival += iter_result[1]
        overflow_per_ceiling[i] = curr_ceiling_overflow / N
        survival_per_ceiling[i] = curr_ceiling_survival / N
        if (curr_ceiling_overflow / N ) > avg_over_at_opt:
            avg_over_at_opt = curr_ceiling_overflow / N
            optimal_ceiling = ceilings[i]
    

    plt.figure(figsize=(13, 6))

    # First subplot - Overflow vs Ceiling
    plt.subplot(1, 3, 1)
    plt.plot(ceilings, overflow_per_ceiling, color=sns.color_palette("muted")[0])
    plt.title(f'Optimal ceiling at {round(optimal_ceiling, 1)}. Avg. overflow of {round(avg_over_at_opt, 3)}')
    plt.xlabel("Ceiling")
    plt.ylabel("Avg. Overflow")
    
    # Second subplot - Survival vs Ceiling
    plt.subplot(1, 3, 2)
    plt.plot(ceilings, survival_per_ceiling, color=sns.color_palette("muted")[1])
    plt.xlabel("Ceiling")
    plt.ylabel("Avg. Survival")
    
    # Third subplot - Histogram of Survival
    plt.subplot(1, 3, 3)
    counts, bins = np.histogram(survival_per_ceiling)
    plt.stairs(counts, bins, color=sns.color_palette("muted")[2])
    plt.xlabel("Survival")
    plt.ylabel("Frequency")
    plt.suptitle('Ceiling vs Avg. Overflow & Avg. Survival')
    plt.show()
    return optimal_ceiling