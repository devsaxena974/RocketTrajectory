import numpy as np
import matplotlib.pyplot as plt

from Simulation import Simulation
from Rocket import Rocket

# Analyze convergence of rk4 implementation using different dt values
def analyze_convergence(rocket: Rocket, sim: Simulation, dt_values):

    # Helper method to calculate the local truncation error
    def truncation_error(t, h, v, sim: Simulation):
        t_m, h_m, v_m = sim.rk4_step(t, h, v)
        t_f, h_f, v_f = sim.rk4_step(t_m, h_m, v_m)

        _, h_next, v_next = sim.rk4_step(t, h, v)

        # Now we find the difference between the two
        E_h = np.abs(h_f - h_next)
        E_v = np.abs(v_f - v_next)

        return E_h, E_v
    
    rocket = Rocket(
                        m=0.05,
                        thrust=10.0,
                        burn_time=1.0,
                        fuel_mass=0.0001,
                        C_D=0.75,
                        A=0.004
                    )
    
    sim = Simulation(rocket,
                      h_0=0.0,
                      v_0=0.0,
                      theta=90.0,
                      temp=288.15,
                      pressure=101325.0,
                      dt=0.1,
                      T=20.0)
    
    E_h_arr = []
    E_v_arr = []
    t_arr = []

    for dt in dt_values:
    
        t = 0.0
        h = sim.h_0
        v = sim.v_0
        sim.dt = dt

        E_h_max = 0.0
        E_v_max = 0.0

        # Go up to t=1.0 and store error results
        while t <= 1.0:
            E_h, E_v = truncation_error(t, h, v, sim)

            E_h_max = max(E_h_max, E_h)
            E_v_max = max(E_v_max, E_v)

            t, h, v = sim.rk4_step(t, h, v)

        E_h_arr.append(E_h)
        E_v_arr.append(E_v)

    return E_h_arr, E_v_arr

def plot_convergence(dt_values, E_h_arr, E_v_arr):
    plt.figure(figsize=(10, 5))

    # Log-log plot of dt vs. altitude error
    plt.subplot(1, 2, 1)
    plt.loglog(dt_values, E_h_arr, marker="o", label="Altitude Error")
    plt.xlabel("Time Step Size (dt)")
    plt.ylabel("Max Local Truncation Error")
    plt.title("Altitude Error vs. Time Step")
    plt.grid(True, which="both")
    plt.legend()

    # Log-log plot of dt vs. velocity error
    plt.subplot(1, 2, 2)
    plt.loglog(dt_values, E_v_arr, marker="o", label="Velocity Error")
    plt.xlabel("Time Step Size (dt)")
    plt.ylabel("Max Local Truncation Error")
    plt.title("Velocity Error vs. Time Step")
    plt.grid(True, which="both")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    dt_values = [0.001, 0.01, 0.05, 0.1, 0.2]
    E_h_arr, E_v_arr = analyze_convergence(dt_values)

    plt.figure(figsize=(10, 5))

    # Log-log plot of dt vs. altitude error
    plt.subplot(1, 2, 1)
    plt.loglog(dt_values, E_h_arr, marker="o", label="Altitude Error")
    plt.xlabel("Time Step Size (dt)")
    plt.ylabel("Max Local Truncation Error")
    plt.title("Altitude Error vs. Time Step")
    plt.grid(True, which="both")
    plt.legend()

    # Log-log plot of dt vs. velocity error
    plt.subplot(1, 2, 2)
    plt.loglog(dt_values, E_v_arr, marker="o", label="Velocity Error")
    plt.xlabel("Time Step Size (dt)")
    plt.ylabel("Max Local Truncation Error")
    plt.title("Velocity Error vs. Time Step")
    plt.grid(True, which="both")
    plt.legend()

    plt.tight_layout()
    plt.show()