'''
    Defines engine thrust profiles for various preset rockets
'''

def linear_thrust(t: float, burn_time: float, max_thrust: float):
    return max(0.0, max_thrust * (1 - t / burn_time))

def quarter_thrust(t: float, burn_time: float, max_thrust: float):
    return max(0.0, max_thrust * (1 - 0.25 * t / burn_time))

def V2_thrust_profile(t: float, burn_time: float, max_thrust: float):
    if t < 0 or t > burn_time:
        return 0.0
    elif t < burn_time * 0.1:
        return max_thrust * (t / (burn_time * 0.1))
    else:
        decay_factor = 1 - ((t - burn_time * 0.1) / (burn_time * 0.9))**2
        return max_thrust * decay_factor
    
def hellfire_thrust_profile(t: float, burn_time: float, max_thrust: float):
    # Rapid linear decrease due to short burn time
    return max(0.0, max_thrust * (1 - t / burn_time))

def patriot_thrust_profile(t: float, burn_time: float, max_thrust: float):
    # Slightly more gradual decrease
    if t < burn_time * 0.2:
        # Rapid increase in the first 20% of burn time
        return max_thrust * (t / (burn_time * 0.2))
    else:
        # Gradual decrease after the peak
        decay_factor = 1 - ((t - burn_time * 0.2) / (burn_time * 0.8))**1.5
        return max_thrust * decay_factor

def falcon1_thrust_profile(t: float, burn_time: float, max_thrust: float):
    # Almost constant thrust with a slight linear decrease
    return max(0.0, max_thrust * (1 - 0.1 * t / burn_time))