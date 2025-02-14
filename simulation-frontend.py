import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from simulation import gen_one_plt, optimize_ceiling

sns.set_theme(style="whitegrid")


def clear_plots():
    if 'fig' in st.session_state:
        plt.close(st.session_state.fig)

def main():
    st.title("Wealth Simulation")
    st.subheader("Made by George Nakhla")
    initial_wealth = st.number_input("Initial Wealth", value=1)
    T = st.number_input("Total Time (T)", value = 5, min_value=1)
    dT = st.number_input("Time Delta (dT)", value=0.01, min_value=0.005)
    a = st.number_input("Parameter a", value=1)
    b = st.number_input("Parameter b", value=1)
    ceiling = st.number_input("Ceiling", value=2, min_value=1)
    N = st.number_input("Number of simulations for optimization", value=100, min_value=1)
    max_ceiling = st.number_input("Maximum Ceiling Value", value=10, min_value=1)
    step_size = st.number_input("Ceiling Step Size", value=0.1, min_value=.01)

    if st.button("Run Single Wealth Simulation"):
        clear_plots()
        gen_one_plt(initial_wealth, T, dT, a, b, ceiling)
        st.session_state.fig = plt.gcf()
        st.pyplot(st.session_state.fig)

    # Run the optimize_ceiling function
    if st.button("Run Ceiling Optimization"):
        clear_plots()  # Clear any existing plots first
        optimize_ceiling(initial_wealth, T, dT, a, b, N, max_ceiling, step_size)
        st.session_state.fig = plt.gcf()
        st.pyplot(st.session_state.fig)

if __name__ == "__main__":
    main()
