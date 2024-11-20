from RocketSim import RocketSim
from Rocket import Rocket
from Simulation import Simulation

def modelRocketTest1():
    rocket = RocketSim(m=0.14175,
                        thrust=3.424,
                        burn_time=0.5,
                        burn_rate=0.0002,
                        fuel_mass=0.0001,
                        C_D=0.8,
                        A=0.0115,
                        T=10.0)
    
    rocket.run()
    rocket.visualize()

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
    
    
    
def SaturnVTest():
    rocket = RocketSim(m = 2800000.0,
                        thrust = 34500000.0,
                        burn_time = 168.0,
                        burn_rate = 1208.3,
                        fuel_mass = 203000.0,
                        C_D = 0.80,
                        A = 34.3589,
                        T = 1200.0)
    
    rocket.run()
    rocket.visualize()

if __name__ == '__main__':
    #modelRocketTest1()

    modelRocketTest2()

    #SaturnVTest()
    
