import numpy as np
import matplotlib.pyplot as plt

class RocketSim:
    # Define constructor
    def __init__(self, 
                 m: float, 
                 thrust: float, 
                 C_D: float, 
                 A: float, 
                 v_0=0.0, 
                 theta=90.0, 
                 dt=0.1, 
                 T=50.0
                ):
        # Initialize all of our constants
        self.g = 9.81
        self.rho = 0.80 # constant for now

        # Rocket Parameters and Properties
        self.m = m
        self.thrust = thrust
        self.C_D = C_D
        self.A = A
        self.v = v_0 # velocity
        self.h = 0.0 # altitude
        self.theta = np.radians(theta) # launch angle (keep vertical)

        # Time Parameters
        self.dt = dt # change this to be dynamic
        self.T = T # also change this duration of integration

        # Initialize arrays to hold simulation data
        self.times = []
        self.altitudes = []
        self.velocities = []

    # Helper method to calculate drag forces
    def drag(self, v: float):
        return 0.5 * self.rho * (v**2) * self.C_D * self.A

    # Define f(t, h, v) to compute the velocity (dh/dt)
    def f(self, t: float, h: float, v: float):
        # simply returns v
        return v
    
    # Define g(t, h, v) to compute the acceleration (dv/dt)
    def g(self, t: float, h: float, v: float):
        F_D = self.drag(v)
        F_G = self.m * self.g
        F_net = self.thrust - F_G - F_D

        return F_net / self.m
    
    def rk4_step(self, t: float, h: float, v: float):
        # Performs a single Runge-Kutta step

        # Slope 1 Calculation
        s_1h = self.dt * self.f(t, h, v)
        s_1v = self.dt * self.g(t, h, v)

        # Slope 2 Calculation
        s_2h = self.dt * 
    
    # def acceleration(self, v: float):
    #     # calculate individual forces and then net force
    #     F_D = self.drag(v)
    #     F_G = self.m * self.g
    #     F_net = self.thrust - F_G - F_D

    #     return F_net / self.m
    
    # def rk4(self, v_i, h_i):
    #     # calculate slope 1
    #     s_1h = v_i
    #     s_1v = self.acceleration(v_i)

    #     # calculate slope 2
    #     s_2h = v_i + 0.5 * s_1v * self.dt
    #     s_2v = self.acceleration(v_i + 0.5 * s_1v * self.dt)

    #     # calculate slope 3
    #     s_3h = v_i + 0.5 * s_2v * self.dt
    #     s_3v = self.acceleration( v_i + 0.5 * s_2v * self.dt)

    #     # calculate slope 4
    #     s_4h = v_i + 0.5 * s_3v * self.dt
    #     s_4v = self.acceleration(v_i + 0.5 * s_3v * self.dt)

    #     # update h, v using RK4 formula to the next step
    #     h_new = h_i + (self.dt / 6.0) * (s_1h + 2 * s_2h + 2 * s_3h + s_4h)
    #     v_new = v_i + (self.dt / 6.0) * (s_1v + 2 * s_2v + 2 * s_3v + s_4v)

    #     print("h_new: ", h_new)
    #     print("v_new: ", v_new)

    #     return h_new, v_new
    

    def run(self):
        # initialize time, altitude, and velocity
        t = 0.0
        v = self.v
        h = self.h

        while (t <= self.T) and (h >= 0):
            self.times.append(t)
            self.altitudes.append(h)
            self.velocities.append(v)

            h_new, v_new = self.rk4(v, h)

            # update the time
            t += self.dt

        
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

        
if __name__ == '__main__':
    rocket1 = RocketSim(m=50.0,
                        thrust=2000.0,
                        C_D=0.8,
                        A=0.03,
                        T=5.0)
    
    rocket1.run()
    rocket1.visualize()