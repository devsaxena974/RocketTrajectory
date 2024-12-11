'''
    test

        Test file to initialize rocket and simulator objects and run them
'''
from src.Rocket import Rocket
from src.Simulation import Simulation

def modelRocketTest1():
    rocket = Rocket(m=0.14175,
                        thrust=3.424,
                        burn_time=0.5,
                        fuel_mass=0.0001,
                        C_D=0.8,
                        A=0.0115)
    
    sim = Simulation(rocket,
                      h_0=0.0,
                      v_0=0.0,
                      theta=90.0,
                      temp=288.15,
                      pressure=101325.0,
                      dt=0.01,
                      T=4.0)
    
    sim.run()
    sim.visualize()

    sim.analysis()

def modelRocketTest2():
    # First we create a rocket
    rocket = Rocket(m=0.05,
                        thrust=10.0,
                        burn_time=1.0,
                        fuel_mass=0.0001,
                        C_D=0.75,
                        A=0.004)
    
    # Now we create a simulator
    sim2 = Simulation(rocket,
                      h_0=0.0,
                      v_0=0.0,
                      theta=90.0,
                      temp=288.15,
                      pressure=101325.0,
                      dt=0.1,
                      T=20.0)
    
    sim2.run()
    sim2.visualize()

    sim2.analysis(dt_values=[0.01, 0.05, 0.1])
    
    
    
def SaturnVTest():
    SaturnV = Rocket(m = 137000.0,
                        thrust = 34500000.0,
                        burn_time = 168.0,
                        fuel_mass = 203000.0,
                        C_D = 0.80,
                        A = 34.3589)
    
    sim = Simulation(SaturnV,
                      h_0=0.0,
                      v_0=0.0,
                      theta=90.0,
                      temp=288.15,
                      pressure=101325.0,
                      dt=0.01,
                      T=12000.0)
    
    sim.run()
    sim.visualize()

    sim.analysis()

def V2Test():
    # Define the thrust profile
    def V2_thrust_profile(t, burn_time, max_thrust):
        if t < 0 or t > burn_time:
            print("No thrust")
            return 0.0  # No thrust before or after burn
        elif t < burn_time * 0.1:
            print("Rapid thrust")
            # Rapid thrust increase in the first 10% of burn time
            return max_thrust * (t / (burn_time * 0.1))
        else:
            print("Gradually decreasing thrust")
            # Gradual decrease after reaching peak
            decay_factor = 1 - ((t - burn_time * 0.1) / (burn_time * 0.9))**2
            return max_thrust * decay_factor

    V2 = Rocket(
        m = 4000.0,
        thrust = 270000.0 * 9.8067,
        burn_time = 60.0,
        fuel_mass = 8500.0,
        C_D = 0.5,
        A = 2.14,
        thrust_profile=V2_thrust_profile
    )

    sim = Simulation(
        rocket = V2,
        h_0=0.0,
        v_0=0.0,
        theta=90.0,
        temp=288.15,
        pressure=101325.0,
        dt=0.1,
        T=600.0
    )

    sim.run()
    sim.visualize()

    # analyze convergence
    sim.analysis()

if __name__ == '__main__':
    #modelRocketTest1()

    modelRocketTest2()

    #SaturnVTest()

    #V2Test()