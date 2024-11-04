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

# Simulation loop
while time <= total_time and altitude >= 0:
    # Calculate the drag force
    drag_force = 0.5 * rho * velocity**2 * drag_coefficient * cross_sectional_area

    # Calculate the net force
    weight = mass * g
    net_force = thrust - weight - drag_force

    # Calculate acceleration (F = ma)
    acceleration = net_force / mass

    # Update velocity and altitude using Euler's method
    velocity += acceleration * dt
    altitude += velocity * dt

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
plt.title("Rocket Altitude over Time")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(times, velocities, label="Velocity (m/s)", color="r")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Rocket Velocity over Time")
plt.grid()

plt.tight_layout()
plt.show()
