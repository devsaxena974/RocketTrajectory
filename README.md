
# Rocket Simulation Project

## Overview
This project simulates the launch and trajectory of rockets using physics principles, numerical integration (Runge-Kutta 4th order), and customizable thrust profiles. The simulation also includes functionality for analyzing numerical error and convergence.

## Directory Structure
```
├── figures/
├── inc/
├ └── thrust_profiles.py
├── previous_files/
├── writing/
├── Rocket.py           # Defines the Rocket class
├── Simulation.py       # Defines the Simulation class
├── analysis.py         # Provides convergence and error analysis tools
├── test.py             # Main script to run test cases
├── gui.py              # Runs the UI for the simulation
├── requirements.txt
└── README.md           # This documentation
```

---

## Prerequisites
- Python 3.11.1 or higher

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## How to Run the Project

1. **Clone the Repository**
   Download or clone the repository to your local machine:
   ```bash
   git clone <repository_url>
   ```

2. **Run the User Interface**
   Execute 'gui.py' to run the user interface opened in a new window. Input your desired rocket and simulator specs, or choose from one of the presets.:
   ```bash
   python gui.py
   ```

3. **Customize Rocket and Simulation Parameters**
   You can modify parameters using the input fields in the UI to define new rockets or adjust simulation settings. Some preset examples are provided for:
   - A small model rocket
   - A slightly larger model rocket
   - Saturn V
   - V2 rocket
   - Hellfire Missile
   - Patriot Missile

4. **Analyze Convergence**
   To analyze convergence and truncation errors, click the button to run an error analysis on the current configuration:


5. **Visualize Results**
   You should be able to see plots of the altitude and velocity of the rocket over time. Clicking the error analysis button will open a new window with plots of the errors:

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

### `gui.py`
Contains code to run the user interface for the simulation
- Uses PyQT5 to create the windows and other features of the UI
- Imports all code necessary for the simulation from the files above

---

## Example Output
### Altitude and Velocity Plots
Running the hellfire missile simulation produces graphs of altitude and velocity over time.
![alt text](https://github.com/devsaxena974/RocketTrajectory/blob/master/figures/hellfire_gui_1.png)

### Convergence Analysis
Error plots for varying time step sizes demonstrate \( h^4 \) scaling in the RK4 method.

![alt text](https://github.com/devsaxena974/RocketTrajectory/blob/master/figures/hellfire_gui_2.png)
---
