# Double Pendulum Lyapunov
Calculation and visualization of average maximum Lyapunov exponent for a double pendulum system

<!-- ABOUT THE PROJECT -->
## About The Project

This project was made for the Extended Essay "Effect of pendulum mass on the chaos motion of a double system", which can be read [here](https://github.com/shinben0327/Double-Pendulum-Lyapunov/blob/053e2cf24e3ef20fbb500136340aa87c97f12045/Effect%20of%20pendulum%20mass%20on%20the%20chaos%20motion%20of%20a%20double%20pendulum%20-%20Jihwan%20Shin.pdf). \
The program calculates and visualizes the average maximum Lyapunov exponent for a double pendulum system with varying initial masses of 0.5-30.0kg for the primary and secondary pendulums. \
Running the program will create a heatmap for all combinations of masses. To download the results as a csv file, use final_result.to_csv('dp_result.csv') after the data frame has been made.

Original code from the source below has been used in Lines 27-64 \
These lines of code implement the equations of motion of the double pendulum. \
'The double pendulum problem' by matplotlib.org \
https://matplotlib.org/stable/gallery/animation/double_pendulum.html \
Accessed 3 Aug 2021

<!-- ABOUT THE PROJECT -->
## Heatmap Example

The result for the heatmap is shown below. \
Changing the parameters in dp-lyapunov.py will give new results.
![alt text](https://github.com/shinben0327/Double-Pendulum-Lyapunov/blob/main/final_result.png?raw=true)
