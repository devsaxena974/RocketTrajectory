import numpy as np
import matplotlib.pyplot as plt

class RocketSim:
    # Define constructor
    def __init__(self, 
                 m, 
                 thrust,
                 burn_time,
                 burn_rate,
                 fuel_mass,
                 C_D, 
                 A, 
                 v_0=0.0, 
                 theta=90.0, 
                 dt=0.1, 
                 T=50.0
                ):
        # Initialize all of our constants
        self.G = np.float64(9.81)
        self.rho = np.float64(1.2249) # constant for now

        # Rocket Parameters and Properties
        self.m = np.float64(m) + np.float64(fuel_mass) # Accounts for rocket and fuel mass
        self.thrust = np.float64(thrust)
        self.burn_time = burn_time # duration of rocket engine providing thrust
        self.burn_rate = burn_rate # rate at which the fuel is consumed
        self.fuel_mass = fuel_mass # mass of fuel carried by rocket
        self.C_D = np.float64(C_D)
        self.A = np.float64(A)
        self.v = np.float64(v_0) # velocity
        self.h = np.float64(0.0) # altitude
        self.theta = np.radians(theta) # launch angle (keep vertical)

        # Time Parameters
        self.dt = dt # change this to be dynamic
        self.T = np.float64(T) # also change this duration of integration

        # Initialize arrays to hold simulation data
        self.times = []
        self.altitudes = []
        self.velocities = []

    # Helper method to calculate drag forces
    def drag(self, v):
        return 0.5 * self.rho * (v**2) * self.C_D * self.A

    # Define f(t, h, v) to compute the velocity (dh/dt)
    def f(self, t, h, v):
        # simply returns v
        return v
    
    # Define g(t, h, v) to compute the acceleration (dv/dt)
    def g(self, t, h, v):
        # Recalculate rocket mass based on fuel burn rate
        if t <= self.burn_time:
            self.m -= self.burn_rate * self.dt

        F_D = self.drag(v)
        F_G = self.m * self.G

        # Thrust only applied during engine burn time
        if t <= self.burn_time:
            F_net = self.thrust - F_G - F_D
        else:
            F_net = -F_G - F_D

        return F_net / self.m
    
    def rk4_step(self, t, h, v):
        # Performs a single Runge-Kutta step

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
        v = self.v
        h = self.h

        while (t <= self.T) and (h >= -1.0):
            self.times.append(t)
            self.altitudes.append(h)
            self.velocities.append(v)

            if v <= 0 and t > self.burn_time:
                print("Apogee reached!")

            # Update variables based on rk4 output for next loop run
            t, h, v = self.rk4_step(t, h, v)

        
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

        
# if __name__ == '__main__':
#     '''
#         TEST with Saturn V Rocket Specifications (rocket1):
#         Mass = 2.8 million kg
#         Thrust = 34.5 million Newtons
#         A = 34.3589 m^2
#         C_D = we don't know (can only be found experimentally)
#     '''

#     '''
#         TEST with Diamondback model rocket with Estes A8 engine (rocket2):
#         Mass = 0.14175 kg
#         Thrust = 3.424 Newtons
#         A = 0.01151 m^2
#         C_D = 0.3
#     '''

#     # rocket1 = RocketSim(m = 2800000.0,
#     #                     thrust = 34500000.0,
#     #                     C_D = 0.50,
#     #                     A = 34.3589,
#     #                     T = 1200.0)

#     rocket2 = RocketSim(m=0.14175,
#                         thrust=3.424,
#                         burn_time=0.5,
#                         burn_rate=0.0002,
#                         fuel_mass=0.0001,
#                         C_D=0.8,
#                         A=0.0115,
#                         T=10.0)
    
#     rocket2.run()
#     rocket2.visualize()