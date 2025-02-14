import numpy as np
import matplotlib.pyplot as plt

def gen_wealth(initial_wealth, T, dT, a, b, ceiling):
    periods_survived = int(T / dT)
    wealth = np.zeros(periods_survived)
    wealth[0] = initial_wealth
    overflow = 0
    noise = np.random.normal(0, np.sqrt(dT), periods_survived)
    for i in range(1, periods_survived):
        d_wealth = a * dT + b * noise[i]
        curr_wealth = wealth[i - 1] + d_wealth

        if curr_wealth > ceiling:
            overflow += curr_wealth - ceiling
            wealth[i] = ceiling
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




def gen_wealth_vectorized(initial_wealth, T, dT, a, b, ceiling, N):
    periods = int(T / dT)
    wealth = np.full(N, initial_wealth, dtype=np.float32)
    survived = N
    overflow = 0

    for _ in range(1, periods):
        d_wealth = a * dT + b * np.random.normal(0, np.sqrt(dT), N)
        alive = wealth > 0
        wealth[alive] += d_wealth[alive]
        overflow += np.sum(np.maximum(wealth - ceiling, 0))
        wealth[wealth > ceiling] = ceiling
        survived += np.count_nonzero(alive)

    return overflow / N, survived / N



def optimize_ceiling(initial_wealth, T, dT, a, b, N, max_ceiling, step_size):
    ceil = np.arange(0, max_ceiling, step_size)
    overflow_per = np.zeros(len(ceil))
    survival_per = np.zeros(len(ceil))

    for i, c in enumerate(ceil):
        overflow_per[i], survival_per[i] = gen_wealth_vectorized(initial_wealth, T, dT, a, b, c, N)
    optimal_ceil = ceil[np.argmax(overflow_per)]
    opt_avg = np.argmax(overflow_per)
    plt.subplot(1, 2, 1)
    plt.plot(ceil, overflow_per)
    plt.title(f'Optimal ceiling at {round(optimal_ceil, 1)}. Avg. overflow of {round(opt_avg, 3)}')
    plt.xlabel("Ceiling")
    plt.ylabel("Avg. Overflow")


    plt.subplot(1, 2, 2)
    plt.plot(ceil, survival_per)
    plt.xlabel("Survival")
    plt.ylabel("Frequency")
    plt.suptitle('Ceiling vs Avg. Overflow & Avg. Survival')
    plt.show()

