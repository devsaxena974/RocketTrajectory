'''
    GUI Implementation:

    Uses the PyQT5 library to create a basic GUI where users can input simulation
        and rocket parameters and get back visualizations

    Fields:
        Thrust Profile
        Rocket Mass
        Thrust
        Burn Time
        Fuel Mass
        Drag Coefficient
        Cross-Section Area
        Initial Altitude
        Initial Velocity
        Launch Angle
        Time Step
        Simulation Duration
    
    Outputs:
        Altitude Graph
        Velocity Graph
        Truncation Error Graphs
'''
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMainWindow, QHBoxLayout
)
from PyQt5.QtCore import Qt, QThreadPool, QRunnable, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)

# Import everything needed for the simulation
import matplotlib.pyplot as plt
from src.Simulation import Simulation
from src.Rocket import Rocket
from src.analysis import analyze_convergence
from inc.thrust_profiles import linear_thrust, quarter_thrust, V2_thrust_profile, hellfire_thrust_profile, patriot_thrust_profile, falcon1_thrust_profile

# Preset rocket configs
PRESETS = {
    "Model Rocket 1": {
        "m": 0.14175,
        "thrust": 3.424,
        "burn_time": 0.5,
        "fuel_mass": 0.0001,
        "C_D": 0.8,
        "A": 0.0115,
        "thrust_profile": linear_thrust,
    },
    "Model Rocket 2": {
        "m": 0.05,
        "thrust": 10.0,
        "burn_time": 1.0,
        "fuel_mass": 0.0001,
        "C_D": 0.75,
        "A": 0.004,
        "thrust_profile": quarter_thrust,
    },
    "V2 Rocket": {
        "m": 4000.0,
        "thrust": 270000.0 * 9.8067,
        "burn_time": 60.0,
        "fuel_mass": 8500.0,
        "C_D": 0.5,
        "A": 2.14,
        "thrust_profile": V2_thrust_profile,
    },
     "Hellfire Missile": {
        "m": 49.0,
        "thrust": 5000.0,
        "burn_time": 5.0,
        "fuel_mass": 9.0,
        "C_D": 0.3,
        "A": 0.02,
        "thrust_profile": hellfire_thrust_profile,
    },
    "Patriot Missile": {
        "m": 700.0,
        "thrust": 110000.0,
        "burn_time": 11.0,
        "fuel_mass": 210.0,
        "C_D": 0.4,
        "A": 0.25,
        "thrust_profile": patriot_thrust_profile,
    },
    # "Falcon 1 First Stage": {
    #     "m": 27200.0,  # Falcon 1 empty weight with first stage fuel
    #     "thrust": 327000.0,  # Merlin engine thrust
    #     "burn_time": 170.0,
    #     "fuel_mass": 22000.0,
    #     "C_D": 0.5,
    #     "A": 3.2, 
    #     "thrust_profile": falcon1_thrust_profile,
    # },
}

# Worker signals
class WorkerSignals(QObject):
    finished = pyqtSignal()  # No data, just notify completion

# Simulation worker
class SimulationWorker(QRunnable):
    def __init__(self, sim):
        super().__init__()
        self.sim = sim
        self.signals = WorkerSignals()

    def run(self):
        self.sim.run()
        self.signals.finished.emit()

# Error Analysis worker
class ErrorAnalysisWorker(QRunnable):
    def __init__(self, sim):
        super().__init__()
        self.sim = sim
        #self.dt_values = dt_values
        self.signals = WorkerSignals()
        #self.callback = callback

    def run(self):
        #E_h_array, E_v_array = analyze_convergence(self.sim.rocket, self.sim, self.dt_values)
        #self.callback(E_h_array, E_v_array)
        #error_window = ErrorAnalysisWindow(self.sim, self.dt_values)
        #error_window.show()
        self.signals.finished.emit()
        

# Error Analysis Window
class ErrorAnalysisWindow(QMainWindow):
    def __init__(self, sim, dt_values):
        super().__init__()
        self.setWindowTitle("Error Analysis")
        self.setGeometry(200, 200, 800, 1200)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Matplotlib figure for error analysis
        self.figure = plt.figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        # Perform error analysis
        E_h_array, E_v_array = analyze_convergence(sim.rocket, sim, dt_values)

        # Plot error analysis
        self.figure.clear()

        # Altitude Error Plot
        ax1 = self.figure.add_subplot(2, 1, 1)
        ax1.loglog(dt_values, E_h_array, marker='o', label="Altitude Error")
        ax1.set_xlabel("Time Step Size (s)")
        ax1.set_ylabel("Error")
        ax1.grid(which="both")
        ax1.legend()

        # Velocity Error Plot
        ax2 = self.figure.add_subplot(2, 1, 2)
        ax2.loglog(dt_values, E_v_array, marker='o', label="Velocity Error")
        ax2.set_xlabel("Time Step Size (s)")
        ax2.set_ylabel("Error")
        ax2.grid(which="both")
        ax2.legend()

        # Refresh canvas
        self.canvas.draw()

# Main GUI
class RocketSimulatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rocket Simulator")
        self.setGeometry(100, 100, 1400, 1200)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Thread pool for background tasks
        self.thread_pool = QThreadPool()

        # Loading label
        self.loading_label = QLabel("Loading...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setFont(QFont("Arial", 16))
        self.loading_label.setVisible(False)

        # Left layout: Input form
        self.form_layout = QFormLayout()

        # Preset selection dropdown
        self.preset_dropdown = QComboBox()
        self.preset_dropdown.addItems(["Select a Preset", *PRESETS.keys()])
        self.preset_dropdown.currentTextChanged.connect(self.load_preset)
        self.form_layout.addRow("Preset Configurations:", self.preset_dropdown)

        # Thrust profile dropdown
        self.thrust_profile_dropdown = QComboBox()
        self.thrust_profile_dropdown.addItems(["Linear Decrease", 
                                                "Decrease by 1/4", 
                                                "V2 Thrust Profile",
                                                "Hellfire Thrust Profile",
                                                "Patriot Thrust Profile",
                                                #"Falcon 1 Thrust Profile",
                                            ])
        self.form_layout.addRow("Thrust Profile (Override):", self.thrust_profile_dropdown)

        # Rocket parameters
        self.mass_input = QLineEdit()
        self.thrust_input = QLineEdit()
        self.burn_time_input = QLineEdit()
        self.fuel_mass_input = QLineEdit()
        self.drag_coefficient_input = QLineEdit()
        self.cross_section_input = QLineEdit()

        # Simulation parameters
        self.altitude_input = QLineEdit("0")
        self.velocity_input = QLineEdit("0")
        self.angle_input = QLineEdit("90")
        self.time_step_input = QLineEdit("0.01")
        self.sim_duration_input = QLineEdit("300")

        # Add inputs to form
        self.form_layout.addRow("Rocket Mass (kg):", self.mass_input)
        self.form_layout.addRow("Thrust (N):", self.thrust_input)
        self.form_layout.addRow("Burn Time (s):", self.burn_time_input)
        self.form_layout.addRow("Fuel Mass (kg):", self.fuel_mass_input)
        self.form_layout.addRow("Drag Coefficient:", self.drag_coefficient_input)
        self.form_layout.addRow("Cross-Section Area (m²):", self.cross_section_input)
        self.form_layout.addRow("Initial Altitude (m):", self.altitude_input)
        self.form_layout.addRow("Initial Velocity (m/s):", self.velocity_input)
        self.form_layout.addRow("Launch Angle (°):", self.angle_input)
        self.form_layout.addRow("Time Step (s):", self.time_step_input)
        self.form_layout.addRow("Simulation Duration (s):", self.sim_duration_input)

        # Run button
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        self.form_layout.addWidget(self.run_button)

        # Error analysis button
        self.error_button = QPushButton("Show Error Analysis")
        self.error_button.clicked.connect(self.show_error_analysis)
        self.error_button.setEnabled(False)
        self.form_layout.addWidget(self.error_button)

        # Add loading label
        self.form_layout.addWidget(self.loading_label)
        
        # Add the form layout to the main layout
        self.main_layout.addLayout(self.form_layout, 1)

        # Right layout: Graphs
        self.graph_layout = QVBoxLayout()

        # Matplotlib canvas
        self.figure = plt.figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.graph_layout.addWidget(self.toolbar)
        self.graph_layout.addWidget(self.canvas)

        # Add the graph layout to the main layout
        self.main_layout.addLayout(self.graph_layout, 4)

        self.sim = None

    def load_preset(self, preset_name):
        if preset_name in PRESETS:
            preset = PRESETS[preset_name]
            self.mass_input.setText(str(preset["m"]))
            self.thrust_input.setText(str(preset["thrust"]))
            self.burn_time_input.setText(str(preset["burn_time"]))
            self.fuel_mass_input.setText(str(preset["fuel_mass"]))
            self.drag_coefficient_input.setText(str(preset["C_D"]))
            self.cross_section_input.setText(str(preset["A"]))
        else:
            # Clear inputs if no preset is selected
            self.mass_input.clear()
            self.thrust_input.clear()
            self.burn_time_input.clear()
            self.fuel_mass_input.clear()
            self.drag_coefficient_input.clear()
            self.cross_section_input.clear()

    def run_simulation(self):
        # Gather inputs
        m = float(self.mass_input.text())
        thrust = float(self.thrust_input.text())
        burn_time = float(self.burn_time_input.text())
        fuel_mass = float(self.fuel_mass_input.text())
        C_D = float(self.drag_coefficient_input.text())
        A = float(self.cross_section_input.text())
        h_0 = float(self.altitude_input.text())
        v_0 = float(self.velocity_input.text())
        theta = float(self.angle_input.text())
        dt = float(self.time_step_input.text())
        T = float(self.sim_duration_input.text())

        # Determine thrust profile: override or preset
        thrust_profile_option = self.thrust_profile_dropdown.currentText()
        if thrust_profile_option == "Linear Decrease":
            thrust_profile = linear_thrust
        elif thrust_profile_option == "Decrease by 1/4":
            thrust_profile = quarter_thrust
        elif thrust_profile_option == "V2 Thrust Profile":
            thrust_profile = V2_thrust_profile
        elif thrust_profile_option == "Hellfire Thrust Profile":
            thrust_profile = hellfire_thrust_profile
        elif thrust_profile_option == "Patriot Thrust Profile":
            thrust_profile = patriot_thrust_profile
        elif thrust_profile_option == "Falcon 1 Thrust Profile":
            thrust_profile = falcon1_thrust_profile
        else:
            # Default to preset thrust profile if no override
            thrust_profile = PRESETS.get(self.preset_dropdown.currentText(), {}).get("thrust_profile", linear_thrust)

        # Create Rocket and Simulation objects
        rocket = Rocket(m, thrust, burn_time, fuel_mass, C_D, A, thrust_profile=thrust_profile)
        self.sim = Simulation(rocket, h_0, v_0, theta, 288.15, 101325, dt, T)

        # Run the simulation
        #self.sim.run()

        # Show loading indicator
        self.loading_label.setVisible(True)

        # Run simulation in the background
        worker = SimulationWorker(self.sim)
        worker.signals.finished.connect(self.on_simulation_finished)
        self.thread_pool.start(worker)

        # Enable error analysis button
        self.error_button.setEnabled(True)

    def on_simulation_finished(self):
        # Hide loading indicator and enable error analysis button
        self.loading_label.setVisible(False)
        self.error_button.setEnabled(True)

        # Plot simulation results
        self.figure.clear()
        ax1 = self.figure.add_subplot(2, 1, 1)
        ax1.plot(self.sim.times, self.sim.altitudes, label="Altitude (m)", color="b")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Altitude (m)")
        ax1.grid()

        ax2 = self.figure.add_subplot(2, 1, 2)
        ax2.plot(self.sim.times, self.sim.velocities, label="Velocity (m/s)", color="r")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Velocity (m/s)")
        ax2.grid()

        self.canvas.draw()

    def show_error_analysis(self):
        if self.sim:
            #dt_values = [0.001, 0.01, 0.05, 0.1, 0.2]
            # Show loading indicator
            self.loading_label.setVisible(True)

            
            # Create and start the worker
            #worker = ErrorAnalysisWorker(self.sim, dt_values)
            worker = ErrorAnalysisWorker(self.sim)
            worker.signals.finished.connect(self.on_error_analysis_finished)
            self.thread_pool.start(worker)


    def on_error_analysis_finished(self):

        dt_values = [0.001, 0.01, 0.05, 0.1, 0.2]
        # Hide loading indicator
        self.loading_label.setVisible(False)

        # Open error analysis window and plot results (code omitted for brevity)
        self.error_window = ErrorAnalysisWindow(self.sim, dt_values)
        self.error_window.show()


# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = RocketSimulatorGUI()
    gui.show()
    sys.exit(app.exec_())
