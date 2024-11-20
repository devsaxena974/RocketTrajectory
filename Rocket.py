'''
    Rocket Class
    State Variables:
        Rocket Mass = m (kg)
        Engine Thrust = thrust (N)
        Engine Burn Time = burn_time (s)
        Fuel Mass = fuel_mass (kg)
        Engine Burn Rate = fuel_mass / burn_time (kg/s)
        Rocket Drag Coefficient = C_D (unitless)
        Rocket Cross Sectional Nose Area = A (m^2)

    Functions:
        thrust_at_time(t):
            Returns the thrust at time t based on burn rate and "thrust curve"

        fuel_status(t):
            Returns the amount of engine fuel left
'''

import numpy as np

class Rocket:

    # Constructor
    def __init__(
                    self,
                    m: float,
                    thrust: float,
                    burn_time: float,
                    fuel_mass: float,
                    C_D: float,
                    A: float
                ):
        # Cast everything to a numpy float 64-bit
        self.m = np.float64(m) + np.float64(fuel_mass)
        self.thrust = np.float64(thrust)
        self.burn_time = np.float64(burn_time)
        self.fuel_mass = np.float64(fuel_mass)
        self.burn_rate = np.float64(fuel_mass / burn_time)
        self.C_D = np.float64(C_D)
        self.A = np.float64(A)

    # Function to calculate amount of engine fuel left
    def fuel_status(self, t, dt):
        if t <= self.burn_time:
            # Reduce mass based on burn rate and time step
            self.m -= self.burn_rate * dt
            fuel_left = max(0.0, self.fuel_mass - self.burn_rate * t)
            return fuel_left
        else:
            # If t is past burn_time, fuel has been depleted
            return 0.0

    # Function to Calculate thrust at time t
    def thrust_at_time(self, t, dt):
        fuel = self.fuel_status(t, dt)
        # Determine thrust at t based on thrust curve
        if fuel > 0.0:
            # linearly decreasing thrust
            return self.thrust * (1 - t / self.burn_time)
        else:
            return 0.0
        
