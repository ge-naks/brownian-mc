import numpy as np
import matplotlib.pyplot as plt

def gen_t(T, dT):
    t = []
    for i in range(int(T/dT)):
        t.append(i)
    return t


def gen_x(initial_wealth, T, dT, a, b, B):
    x = [initial_wealth]
    overflow = [0]
    period = 500
    for i in range(1, int(T/dT)):
        curr_x = 0
        curr_overflow = 0
        dW = np.random.normal(0, np.sqrt(dT), 1)
        dW = dW[0]
        dX = a * dT + b * dW
        curr_x = x[i-1] + dX

        if curr_x > B:
            curr_overflow = curr_x - B
            overflow.append(curr_overflow)
            curr_x = B
            x.append(curr_x)
        elif curr_x > 0 and curr_x < B:
            x.append(curr_x)
            overflow.append(0)
        elif curr_x < 0:
            overflow.append(0)
            period = i
            break
    
    return [x, overflow, period]
    

def run_B(initial_wealth, T, dT, a, b, B_vals):
    num_runs = 100
    all_overflow = []
    all_periods = []
    
    for i in range(num_runs):
        B = B_vals[i]
        temp = gen_x(initial_wealth, T, dT, a, b, B)
        all_overflow.append(sum(temp[1]))
        all_periods.append(temp[2])
    return [all_overflow, all_periods]


def run_B_for_avg(initial_wealth, T, dT, a, b, B):
    num_runs = 100
    all_overflow = []
    all_periods = []
    
    for i in range(num_runs):
        temp = gen_x(initial_wealth, T, dT, a, b, B)
        all_overflow.append(sum(temp[1]))
        all_periods.append(temp[2])
    return [all_overflow, all_periods]

def sim_wealth(initial_wealth, T, dT, a, b, B):
    t = gen_t(T, dT)
    re = gen_x(initial_wealth, T, dT, a, b, B)
    x = re[0]
    overflow = re[1]


    while(len(x) != int(T/dT)):
        x.append(0)

    while(len(overflow) != int(T/dT)):
        overflow.append(0)
    total_overflow = sum(overflow)
    fig, ax = plt.subplots() 
    ax.plot(t, x)  
    ax.set_xlabel('T')
    ax.set_ylabel('Wealth')
    ax.set_title("Dynamic Wealth Evolution")
    
    #these commented out lines will automatically make the graphs 
    # full screen so that the text at the bottom is not squished, 
    # undesirable behavior that i will fix... eventually

    #manager = plt.get_current_fig_manager()
    #manager.full_screen_toggle()
    
    plt.show()


def sim_avg_per(initial_wealth, T, dT, a, b, B_vals, n):
   all_period = [i * 0 for i in range(100)]
   for i in range(n):
       temp = run_B(initial_wealth, T, dT, a, b, B_vals)
       avg_per = temp[1]
       for j in range(len(avg_per)):
           all_period[j] = all_period[j] + avg_per[j]
   for i in range(len(all_period)):
       all_period[i] = all_period[i] / n
   fig, ax = plt.subplots()  
   ax.plot(B_vals, all_period)  
   ax.set_xlabel('B Values')
   ax.set_ylabel('Average Periods Survived')
   ax.set_title('Wealth Survivability')
   plt.show()


def sim_B(initial_wealth, T, dT, a, b, B_vals, n):
    avg_overflow = [i * 0 for i in range(100)]
    for i in range(n):
        temp = run_B(initial_wealth, T, dT, a, b, B_vals)
        all_overflow = temp[0]
        for j in range(len(all_overflow)):
            avg_overflow[j] =  avg_overflow[j] + all_overflow[j]

    for i in range(len(all_overflow)):
        avg_overflow[i] = avg_overflow[i] / n
    
    max_x = max(avg_overflow)
    optimal_B = B_vals[avg_overflow.index(max_x)]
    temp = run_B_for_avg(initial_wealth, T, dT, a, b, optimal_B)
    data = temp[1]


    counts, bins = np.histogram(data)
    plt.stairs(counts, bins)
    plt.xlabel('Number of Survived Periods')
    plt.ylabel('Frequency')
    plt.title('B* Period Frequency')
    plt.xticks(fontsize=5)
    fig, ax = plt.subplots()  
    ax.plot(B_vals, avg_overflow)  
    ax.set_xlabel('B Values')
    ax.set_ylabel('Average Overflow')
    ax.set_title('B* Optimization')

    txt1 = "Optimal B value at:" + str(optimal_B)
    txt2 = "Max drawdown of:" + str(max_x)

    fig.text(.5, .005, txt1, ha = 'center')
    fig.text(.5, .05, txt2, ha = 'center')
    
    #these commented out lines will automatically make the graphs 
    # full screen so that the text at the bottom is not squished, 
    # undesirable behavior that i will fix... eventually

    #manager = plt.get_current_fig_manager()
    #manager.full_screen_toggle()
    plt.show()

def binary_search(arr, low, high, x):
 
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if arr[mid] == x:
            return True
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return False





#do not change
B_vals = [i * .1 for i in range(100)]

# sample values, can change parameterizations
initial_wealth = 1
T = 5
dT = .01
a = 1
b = 1
n = 100
B = 2.5

#sim_avg_per(initial_wealth, T, dT, a, b, B_vals, n)
sim_B(initial_wealth , T, dT, a, b, B_vals, n)
#sim_wealth(initial_wealth, T, dT, a, b, B)



