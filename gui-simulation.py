import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
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
B_vals = [i * .1 for i in range(100)]

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

    st.pyplot(fig)
    st.text("Total Drawdown produced:" + str(total_overflow))

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
   st.pyplot(fig)

def sim_B(initial_wealth, T, dT, a, b, B_vals, n):
    avg_overflow = [i * 0 for i in range(100)]
    for i in range(n):
        temp = run_B(initial_wealth, T, dT, a, b, B_vals)
        all_overflow = temp[0]
        for j in range(len(all_overflow)):
            avg_overflow[j] = avg_overflow[j] + all_overflow[j]

    for i in range(len(all_overflow)):
        avg_overflow[i] = avg_overflow[i] / n
    
    max_x = max(avg_overflow)
    optimal_B = B_vals[avg_overflow.index(max_x)]
    temp = run_B_for_avg(initial_wealth, T, dT, a, b, optimal_B)
    data = temp[1]

    bin_width = 50
    bins = range(0, max(data) + bin_width, bin_width)
    counts, _ = np.histogram(data, bins=bins)

    plt.bar(bins[:-1], counts, width=bin_width)
    plt.xlabel('Number of Survived Periods')
    plt.ylabel('Frequency')
    plt.title('B* Period Frequency')
    plt.xticks(fontsize=8)

    st.pyplot(plt)  # Display the histogram

    fig, ax = plt.subplots()  
    ax.plot(B_vals, avg_overflow)  
    ax.set_xlabel('B Values')
    ax.set_ylabel('Average Overflow')
    ax.set_title('B* Optimization')

    st.pyplot(fig)
    st.text("Optimal B value is:" + str(optimal_B))
    st.text("Produces max wealth of:" + str(max_x))

st.title("Parameterization Tool")

st.subheader("Some sample values have been already provided. You may change them as you wish!")
st.subheader("Note: values of n > 1000 will take a significant amount of time to process. Please be patient")



iw = st.number_input("Enter Initial Wealth", value=(1))
a = st.number_input("Enter A", value=(1))
T = st.number_input("Enter T (horizon)", value=(5))
b = st.number_input("Enter b", value=(1))
dT = st.number_input("Enter dT" , value=(.01))
n = st.number_input("Enter Simulation count", value=(100))
B = st.number_input("Enter B value", value=(2.5))
st.button("Optimize B", on_click=sim_B, args= (iw, T, dT, a, b, B_vals, int(n)))
st.button("Test One B", on_click=sim_wealth, args= (iw, T, dT, a, b, B))
st.button("Simulate Average Survival", on_click=sim_avg_per, args= (iw, T, dT, a, b, B_vals, n))

st.write("Made by George Nakhla")




