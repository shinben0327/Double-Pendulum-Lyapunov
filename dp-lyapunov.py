"""
*******************************************************
Calculation and visualization of average maximum lyapunov exponent for a double pendulum system

Created for Extended Essay
"Effect of pendulum mass on the chaos motion of a double pendulum"

Original code from the source above has been used in Lines 27-64
'The double pendulum problem' by matplotlib.org
https://matplotlib.org/stable/gallery/animation/double_pendulum.html
Accessed 3 Aug 2021

Written using Python 3.8
*******************************************************
"""

# import libraries required for this program
from numpy import sin, cos
from math import log
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.integrate as integrate

# giving variable values
G = 9.81  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
L = L1 + L2  # maximal length of the combined pendulum
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg
t_stop = 30  # how many seconds to simulate


# defining the double pendulum motion equations obtained through calculations
def derivs(state, t):
    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    delta = state[2] - state[0]
    den1 = (M1 + M2) * L1 - M2 * L1 * cos(delta) * cos(delta)
    dydx[1] = ((M2 * L1 * state[1] * state[1] * sin(delta) * cos(delta)
                + M2 * G * sin(state[2]) * cos(delta)
                + M2 * L2 * state[3] * state[3] * sin(delta)
                - (M1 + M2) * G * sin(state[0]))
               / den1)

    dydx[2] = state[3]

    den2 = (L2 / L1) * den1
    dydx[3] = ((- M2 * L2 * state[3] * state[3] * sin(delta) * cos(delta)
                + (M1 + M2) * G * sin(state[0]) * cos(delta)
                - (M1 + M2) * L1 * state[1] * state[1] * sin(delta)
                - (M1 + M2) * G * sin(state[2]))
               / den2)

    return dydx


# create a time array from 0..t_stop sampled at 0.02 second steps
dt = 0.02
t = np.arange(0, t_stop, dt)


# create an array of th1 for each time frame
# th1, w1: angle (degrees) and angular velocity (degrees per second) of pendulum 1
# th2, w2: angle (degrees) and angular velocity (degrees per second) of pendulum 2
def th1_array(th1, w1, th2, w2):
    state = np.radians([th1, w1, th2, w2])  # convert degrees to radians
    y = integrate.odeint(derivs, state, t)  # integrate ODE using SciPy library
    th1_array_result = y[:, 0]  # extract only the list of th1 from the result
    return th1_array_result


# find the difference of th1 between two neighbouring trajectories
# m1, m2: mass of pendulum 1 and 2 (kg)
# dth: difference of initial angle for the two neighbouring trajectories
def trajectory_difference(th1, th2, m1, m2, dth):
    global M1, M2
    M1 = m1
    M2 = m2
    trajectory_A = th1_array(th1, 0, th2, 0)
    trajectory_B = th1_array(th1 + dth, 0, th2 + dth, 0)
    trajectory_difference_result = abs(trajectory_A - trajectory_B)
    return trajectory_difference_result


# calculate the lyapunov exponent for all values of N within the domain of simulation
def lyapunov_single(difference):
    lyapunov = [0]
    for N_value in range(1, len(difference)):
        exponent = (1 / N_value) * log((difference[N_value] / difference[0]))
        lyapunov.append(exponent)
    return lyapunov


# make arrays of M1 and M2 to iterate through for independent variable
M1_array = []
M2_array = []
for i in range(1, 61):
    M1_array.append(float(i) * 0.5)
    M2_array.append(float(i) * 0.5)

# make an array of angles to be used for average lyapunov exponent calculation
angles_array = []
for i in range(1, 10):
    angles_array.append(float(i) * 10.0)

result_2d_matrix = []

# calculate the average maximum lyapunov exponent for all initial values
for mass1 in tqdm(M1_array):
    temp_result = []
    for mass2 in M2_array:
        lyapunov_sum = 0
        for angle in angles_array:
            diff_list = trajectory_difference(angle, angle, mass1, mass2, 0.01)
            maximum_lyapunov = max(lyapunov_single(diff_list))
            lyapunov_sum += maximum_lyapunov
        temp_result.append(lyapunov_sum / len(angles_array))
    result_2d_matrix.append(temp_result)

# convert to Pandas DataFrame
final_result = pd.DataFrame(result_2d_matrix, M1_array, M2_array)
print(final_result)

# create heatmap
plt.subplots(figsize=(12,9))
heat_map = sns.heatmap(final_result, annot=False)
heat_map.set_xticklabels(heat_map.get_xticklabels(), rotation=90, horizontalalignment='center')

plt.xlabel("M2 (kg)")
plt.ylabel("M1 (kg)")
heat_map.xaxis.tick_top()
heat_map.xaxis.set_label_position('top')

plt.show()
