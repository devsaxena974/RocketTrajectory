'''
    Simulation Class
    State Variables:
        Rocket = rocket
        Initial Altitude = h_0 (m)
        Initial Velocity = v_0 (m/s)
        Launch Angle = theta (degrees)
        Air Density = rho (kg/m^2)
        Air Temperature = temp (Kelvin)
        Barometric Air Pressure = pressure (Pascals)
        Gravitational Constant = G (m/s^2)
        Step size = dt (s)
        Simulation End Time = T (s)

        Array to hold times = times []
        Array to hold altitudes = altitudes []
        Array to hold velocities = velocities []

    Functions:
        air_density(self, t, h):
            Calculates the air density in the atmosphere based on rocket altitude

        drag(self, v):
            Calculate drag forces on the rocket at current velocity

        f(self, t, h, v):
            Computes velocity (dh/dt)

        g(self, t, h, v):
            Computes acceleration (dv/dt)

        rk4_step(self, t, h, v):
            Performs a single Runge-Kutta 4th order step

        run(self):
            Runs the simulation using rk4_step for the entire time duration

        visualize(self):
            Generates plots using simulation data
'''
import numpy as np
import matplotlib.pyplot as plt

from Rocket import Rocket

class Simulation:
    # Constructor
    def __init__(   self,
                    rocket: Rocket,
                    h_0: float,
                    v_0: float,
                    theta: float,
                    temp: float,
                    pressure: float,
                    dt: float,
                    T: float
                ):
        
        # Define all our state variables
        self.rocket = rocket
        self.h_0 = np.float64(h_0)
        self.v_0 = np.float64(v_0)
        self.theta = np.radians(theta)
        self.temp = np.float64(temp)
        self.pressure = np.float64(pressure)
        self.rho = np.float64(0.0) # We will define later using a function
        self.G = np.float64(9.8067)

        # Time parameters
        self.dt = np.float64(dt)
        self.T = np.float64(T)
        
        # Define arrays to hold simulation data
        self.times = []
        self.altitudes = []
        self.velocities = []

    # Function to calculate air density (rho) based on altitude
    #   - uses the International Standard Atmosphere model
    def air_density(self, h):
        # First define some constants
        air_gas_const = np.float64(287.05) # given in J/kg K)
        temp_lapse_rate = np.float64(-0.0065) # rate at which temp decreases with altitude given in K/m
        pressure_sea_lvl = self.pressure
        temp_sea_lvl = self.temp

        # Calculate the temperature at current altitude
        cur_temp = temp_sea_lvl + (temp_lapse_rate * h)

        # Calculate pressure using barometric formula
        exp = -self.G / (air_gas_const * temp_lapse_rate)
        cur_pressure = pressure_sea_lvl * (cur_temp / temp_sea_lvl) ** exp

        # Calculate air density using ideal gas law
        rho = cur_pressure / (air_gas_const * cur_temp)

        return rho
    
    # Function to calculate drag forces on the rocket
    def drag(self, h, v):
        # compute the air density value first
        self.rho = self.air_density(h)
        # now we can calculate the drag forces based on the formula
        return 0.5 * self.rho * (v**2) * self.rocket.C_D * self.rocket.A
    
    # Define f(t, h, v) to compute the velocity (dh/dt)
    def f(self, t, h, v):
        # simply returns v
        return v

    # Define g(t, h, v) to compute the acceleration (dv/dt)
    def g(self, t, h, v):
        # Recalculate thrust based on time
        self.rocket.thrust = self.rocket.thrust_at_time(t, dt=self.dt)

        F_D = self.drag(h, v)
        F_G = self.rocket.m * self.G

        # Thrust only applied during engine burn time
        # if t <= self.burn_time:
        #     F_net = self.thrust - F_G - F_D
        # else:
        #     F_net = -F_G - F_D
        F_net = self.rocket.thrust - F_G - F_D

        return F_net / self.rocket.m
    
    def rk4_step(self, t, h, v):
        # Performs a single Runge-Kutta 4th order method step

        # Slope 1 Calculation
        s_1h = self.dt * self.f(t, h, v)
        s_1v = self.dt * self.g(t, h, v)

        # Slope 2 Calculation
        s_2h = self.dt * self.f((t+0.5*self.dt), (h+0.5*s_1h), (v+0.5*s_1v))
        s_2v = self.dt * self.g((t+0.5*self.dt), (h+0.5*s_1h), (v+0.5*s_1v))

        # Slope 3 Calculation
        s_3h = self.dt * self.f((t+0.5*self.dt), (h+0.5*s_2h), (v+0.5*s_2v))
        s_3v = self.dt * self.g((t+0.5*self.dt), (h+0.5*s_2h), (v+0.5*s_2v))

        # Slope 4 Calculation
        s_4h = self.dt * self.f((t+self.dt), (h+s_3h), (v+s_3v))
        s_4v = self.dt * self.g((t+self.dt), (h+s_3h), (v+s_3v))

        # Then, update t_{i+1}, h_{i+1}, v_{i+1}
        t_1 = t + self.dt
        h_1 = h + (1./6.) * (s_1h + 2*s_2h + 2*s_3h + s_4h)
        v_1 = v + (1./6.) * (s_1v + 2*s_2v + 2*s_3v + s_4v)

        return t_1, h_1, v_1
    
    # Run the RK4 Steps for the Desired Time Duration
    def run(self):
        # initialize time, altitude, and velocity
        t = 0.0
        v = self.v_0
        h = self.h_0

        while (t <= self.T) and (h >= -0.00000001):
            self.times.append(t)
            self.altitudes.append(h)
            self.velocities.append(v)

            # if v <= 0 and t > self.rocket.burn_time:
            #     print("Apogee reached!")

            # Check to see if rocket has escaped earth's atmosphere
            if h > 99779.3:
                print("Exited Earth's Atmosphere!")
                break

            # Update variables based on rk4 output for next loop run
            t, h, v = self.rk4_step(t, h, v)

    # Function to visualize output
    def visualize(self):
        print(self.times)
        print(self.altitudes)
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(self.times, self.altitudes, label="Altitude (m)", color="b")
        plt.xlabel("Time (s)")
        plt.ylabel("Altitude (m)")
        plt.title("Rocket Altitude over Time")
        plt.grid()

        plt.subplot(1, 2, 2)
        plt.plot(self.times, self.velocities, label="Velocity (m/s)", color="r")
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (m/s)")
        plt.title("Rocket Velocity over Time")
        plt.grid()

        plt.tight_layout()
        plt.show()
