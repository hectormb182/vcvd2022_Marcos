import math

gravity = 9.81  # [m/s**2]


# send the friction coefficient
def get_friction_coefficient(road, condition):
    if road == "concrete" and condition == "dry":
        return 0.5
    elif road == "concrete" and condition == "wet":
        return 0.35
    elif road == "ice" and condition == "dry":
        return 0.15
    elif road == "ice" and condition == "wet":
        return 0.08
    elif road == "water" and condition == "aquaplaning":
        return 0.05
    elif road == "gravel" and condition == "dry":
        return 0.35
    elif road == "sand" and condition == "dry":
        return 0.3
    else:
        return 0


# Calculate de deceleration => Total Force = mass * acc => - F_friction = mass * acc =>
# -mu * gravity (* inclination) = acc
def get_deceleration(friction_coefficient, inclination):
    inclination = math.radians(inclination)
    dec = -1 * friction_coefficient * gravity * (math.cos(inclination) + math.sin(inclination))
    return round(dec, 2)


def get_position(time, pos_initial, velocity, acc):
    pos_final = pos_initial + velocity * time + (0.5 * acc * time ** 2)
    return round(pos_final, 2)


def get_velocity(vel_initial, acc, time,):
    vel_final = (time * acc) + vel_initial
    return round(vel_final, 2)
