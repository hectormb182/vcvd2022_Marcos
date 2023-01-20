gravity = 9.81  # [m/s^2]


# Get final position function
# if the vehicle must stop => kinetic energy must be equal to friction energy
# Wf = Friction_energy * (final_position - initial_position) =
# = friction_coefficient * mass * gravity * (final_position - initial_position)
# Wk = (mass * velocity_initial^2) / 2
# Wf = Wk => final_position = ((velocity_initial^2) / 2 * gravity * friction_coefficient) + initial_position
def get_final_pos(v_i, f_c, p_i):
    p_f = ((v_i * v_i) / (2 * gravity * f_c)) + p_i
    return p_f


def get_break_time(p_f, p_i, v_i):
    t = (p_f - p_i) / (1.5 * v_i)
    return t


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


# Physic formulas:
def get_friction_force(mass, friction_coefficient):
    f_r = friction_coefficient * mass * gravity
    return f_r


def get_velocity(time, v_i, acceleration):
    v_f = (time * acceleration) + v_i
    return v_f


def get_acceleration(time, v_f, v_i):
    a = (v_f - v_i) / time
    return a


def get_position(time, position_initial, velocity, acceleration):
    position_final = position_initial + velocity * time + (0.5 * acceleration * time ** 2)
    return position_final


# Conservation of energy formulas
def get_kinetic_energy(mass, velocity):
    w_kin = (mass * velocity) * 0.5
    return w_kin

