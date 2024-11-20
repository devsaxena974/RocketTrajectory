import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.81  # gravitational acceleration (m/s^2)
rho = 1.225  # air density at sea level (kg/m^3)

# Rocket parameters (adjust these as needed)
mass = 50.0  # rocket mass (kg)
thrust = 2000.0  # constant thrust (N)
drag_coefficient = 0.75  # drag coefficient
cross_sectional_area = 0.03  # cross-sectional area (m^2)
initial_velocity = 0.0  # initial velocity (m/s)
launch_angle = 90.0  # launch angle in degrees (90 for vertical)

# Convert angle to radians
launch_angle_rad = np.radians(launch_angle)

# Time parameters
dt = 0.1  # time step (seconds)
total_time = 50.0  # total simulation time (seconds)

# Lists to store simulation data
times = []
altitudes = []
velocities = []

# Initial conditions
velocity = initial_velocity
altitude = 0.0
time = 0.0

# Function to calculate derivatives
def derivatives(altitude, velocity):
    drag_force = 0.5 * rho * velocity**2 * drag_coefficient * cross_sectional_area
    weight = mass * g
    net_force = thrust - weight - drag_force
    acceleration = net_force / mass
    return velocity, acceleration

# Simulation loop using RK4
while time <= total_time and altitude >= 0:
    # RK4 coefficients for altitude and velocity
    k1_v, k1_a = derivatives(altitude, velocity)
    k2_v, k2_a = derivatives(altitude + 0.5 * dt * k1_v, velocity + 0.5 * dt * k1_a)
    k3_v, k3_a = derivatives(altitude + 0.5 * dt * k2_v, velocity + 0.5 * dt * k2_a)
    k4_v, k4_a = derivatives(altitude + dt * k3_v, velocity + dt * k3_a)

    # Update velocity and altitude using the weighted average of the slopes
    velocity += (dt / 6.0) * (k1_a + 2 * k2_a + 2 * k3_a + k4_a)
    altitude += (dt / 6.0) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)

    # Store the current state
    times.append(time)
    altitudes.append(altitude)
    velocities.append(velocity)

    # Update time
    time += dt

# Plot altitude and velocity over time
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(times, altitudes, label="Altitude (m)", color="b")
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.title("Rocket Altitude over Time (RK4)")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(times, velocities, label="Velocity (m/s)", color="r")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Rocket Velocity over Time (RK4)")
plt.grid()

plt.tight_layout()
plt.show()
