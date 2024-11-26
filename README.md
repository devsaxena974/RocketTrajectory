
# Rocket Simulation Project

## Overview
This project simulates the launch and trajectory of rockets using physics principles, numerical integration (Runge-Kutta 4th order), and customizable thrust profiles. The simulation also includes functionality for analyzing numerical error and convergence.

## Directory Structure
```
project/
├── figures/
├── previous_files/
├── Rocket.py           # Defines the Rocket class
├── Simulation.py       # Defines the Simulation class
├── analysis.py         # Provides convergence and error analysis tools
├── test.py             # Main script to run test cases
└── README.md           # This documentation
```

---

## Prerequisites
- Python 3.7 or higher
- Required libraries:
  - `numpy`
  - `matplotlib`

Install dependencies using:
```bash
pip install numpy matplotlib
```

---

## How to Run the Project

1. **Clone the Repository**
   Download or clone the repository to your local machine:
   ```bash
   git clone <repository_url>
   cd project
   ```

2. **Run the Test Cases**
   Test cases for different rocket models are in `main.py`. Execute the script to run all or individual test cases:
   ```bash
   python test.py
   ```

3. **Customize Rocket and Simulation Parameters**
   You can modify parameters in `test.py` to define new rockets or adjust simulation settings. Examples are provided for:
   - A small model rocket
   - A slightly larger model rocket
   - Saturn V
   - V2 rocket

4. **Analyze Convergence**
   To analyze convergence and truncation errors, call the `analysis()` method on the `Simulation` object:
   ```python
   sim.analysis(dt_values=[0.001, 0.01, 0.05, 0.1, 0.2])
   ```

5. **Visualize Results**
   The `visualize()` method generates altitude and velocity plots:
   ```python
   sim.visualize()
   ```

---

## Adding a Custom Thrust Profile
Thrust profiles can be defined as Python functions and passed during `Rocket` instantiation. Example for a linearly decreasing profile:
```python
def linear_thrust(t, burn_time, max_thrust):
    return max(0.0, max_thrust * (1 - t / burn_time))

rocket = Rocket(
    m=500,
    thrust=1e6,
    burn_time=120,
    fuel_mass=300,
    C_D=0.5,
    A=10,
    thrust_profile=linear_thrust
)
```

---

## File Descriptions

### `Rocket.py`
Defines the `Rocket` class. Key features:
- Mass, thrust, burn time, and drag parameters.
- `thrust_at_time`: Computes thrust based on the current time and custom thrust profile.
- `fuel_status`: Tracks remaining fuel and adjusts rocket mass.

### `Simulation.py`
Defines the `Simulation` class. Key features:
- Models rocket motion using the RK4 numerical integration method.
- Calculates drag and air density dynamically.
- Provides visualization and error analysis functions.

### `analysis.py`
Contains functions for error and convergence analysis:
- `analyze_convergence`: Computes truncation errors for different time step sizes.
- `plot_convergence`: Plots the errors as log-log graphs.

---

## Example Output
### Altitude and Velocity Plots
Running the V2 test produces graphs of altitude and velocity over time.

### Convergence Analysis
Error plots for varying time step sizes demonstrate \( h^4 \) scaling in the RK4 method.

---
