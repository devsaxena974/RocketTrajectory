'''
    Rocket Class
    State Variables:
        Rocket Mass = m (kg)
        Max Engine Thrust = thrust (N)
        Engine Burn Time = burn_time (s)
        Fuel Mass = fuel_mass (kg)
        Engine Burn Rate = fuel_mass / burn_time (kg/s)
        Rocket Drag Coefficient = C_D (unitless)
        Rocket Cross Sectional Nose Area = A (m^2)
        Rocket Engine Thrust Profile = function()

    Functions:
        default_thrust_profile(t, burn_time, thrust):
            Returns a default profile that decreases engine thrust linearly

        thrust_at_time(t, dt):
            Returns the thrust at time t based on burn rate and "thrust curve"

        fuel_status(t, dt):
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
                    A: float,
                    thrust_profile=None
                ):
        # Cast everything to a numpy float 64-bit
        self.dry_mass = np.float64(m)
        self.m = np.float64(m)
        self.m += np.float64(fuel_mass)
        self.thrust = np.float64(thrust)
        self.burn_time = np.float64(burn_time)
        self.fuel_mass = np.float64(fuel_mass)
        self.burn_rate = np.float64(fuel_mass / burn_time)
        self.C_D = np.float64(C_D)
        self.A = np.float64(A)
        self.thrust_profile = thrust_profile if thrust_profile else self.default_thrust_profile

    # Function to set the default thrust profile if one is not provided
    def default_thrust_profile(self, t: float, burn_time: float, max_thrust: float):
        # Decrease thrust linearly
        if (t >= 0) and (t <= burn_time):
            return max_thrust * (1 - t / burn_time)
        # else return 0.0
        return 0.0

    # Function to calculate amount of engine fuel left
    def fuel_status(self, t: float, dt: float):
        #dry_mass = self.m - self.fuel_mass
        if t <= self.burn_time:
            # Reduce mass based on burn rate and time step
            self.m = max(self.dry_mass, self.m - self.burn_rate * dt)
            fuel_left = max(0.0, self.fuel_mass - self.burn_rate * t)
            return fuel_left
        else:
            # If t is past burn_time, fuel has been depleted
            self.m = self.dry_mass
            return 0.0

    # Function to Calculate thrust at time t
    def thrust_at_time(self, t: float, dt: float):
        fuel = self.fuel_status(t, dt)
        print("Time step: ", t)
        # Determine thrust at t based on thrust curve
        return self.thrust_profile(t, self.burn_time, self.thrust)
