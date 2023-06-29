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
            break
    
    return [x, overflow]
    

def run_B(initial_wealth, T, dT, a, b, B_vals):
    num_runs = 100
    all_overflow = []

    for i in range(num_runs):
        B = B_vals[i]
        temp = gen_x(initial_wealth, T, dT, a, b, B)
        all_overflow.append(sum(temp[1]))
    return all_overflow

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
    
    fig, ax = plt.subplots()  # Create a figure and axes object
    ax.plot(t, x)  # Plot the data on the axes

    # Optionally, you can add labels and a title to the plot
    ax.set_xlabel('T')
    ax.set_ylabel('Wealth')
    ax.set_title("Dynamic Wealth Evolution")

    st.pyplot(fig)
    st.text("Totale Drawdown produced:" + str(total_overflow))

def sim_B(initial_wealth, T, dT, a, b, B_vals, n):

    avg_overflow = [i * 0 for i in range(100)]

    

    for i in range(n):
        all_overflow = run_B(initial_wealth, T, dT, a, b, B_vals)
        for j in range(len(all_overflow)):
            avg_overflow[j] =  avg_overflow[j] + all_overflow[j]

    for i in range(len(all_overflow)):
        avg_overflow[i] = avg_overflow[i] / n
    
    max_x = max(avg_overflow)
    optimal_B = B_vals[avg_overflow.index(max_x)]

    fig, ax = plt.subplots()  # Create a figure and axes object  
    ax.plot(B_vals, avg_overflow)  # Plot the data on the axes
    ax.set_xlabel('B Values')
    ax.set_ylabel('Average Overflow')
    ax.set_title('B* Optimization')

    st.pyplot(fig)
    st.text("Optimal B value is:" + str(optimal_B))
    st.text("Produces max wealth of:" + str(max_x))

st.title("Parameterization Tool")

st.subheader("Some sample values: Initial Wealth = 1, a = 1, T = 5 b = 1, dT = .01, n = 100, B = 3.5")

iw = st.number_input("Enter Initial Wealth")
a = st.number_input("Enter A")
T = st.number_input("Enter T (horizon)")
b = st.number_input("Enter b")
dT = st.number_input("Enter dT")
n = st.number_input("Enter Simulation count")
B = st.number_input("Enter B value")
st.button("run", on_click=sim_B, args= (iw, T, dT, a, b, B_vals, int(n)))
st.button("run instance", on_click=sim_wealth, args= (iw, T, dT, a, b, B))

st.write("Made by George Nakhla")




