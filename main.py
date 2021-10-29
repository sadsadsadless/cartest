import math

e_max = 600000.0    # максимальная энергия торможения
l_critical = 20.0   # за сколько м до стены нужно остановиться


def E(m, v):
    return m * v * v / 2


def V(e, m):
    return math.sqrt(2 * e / m) if e > 0 else 0.0


def defuzzy(e):
    return e * e_max


def fuzzy(e):
    return e / e_max if e < e_max else 1.0


def fuzzy_controller(v, l, m):
    current_e = E(m, v)
    time = math.ceil(current_e / e_max)
    time = time if time != 0 else 1.0
    if v * time / 2 > l - l_critical:
        return 1.0
    elif v * time > l - l_critical:
        t_stop = 2 * (l - l_critical) / v
        return fuzzy(current_e / t_stop)
    else:
        return 0.0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # variables
    M = 1500.0        # масса машины, кг
    v = 50.0    # начальная скорость, м/с
    l = 500.0  # начальное расстояние, м

    t = 0
    while True:
        stop_energy = defuzzy(fuzzy_controller(v, l, M))
        print(f'step: {t},\t v: {v},\t l: {l},\t energy: {E(M, v)},\t stop energy: {stop_energy}')
        v1 = V(E(M, v) - stop_energy, M)
        v1 = 0.0 if v1 < 0.0 else v1
        l -= (v + v1) / 2
        v = v1
        t += 1
        if round(v) <= 0:
            print(f'-- machine stopped, l:{l}')
            break
        if round(l) <= 0:
            print(f'crashed, v:{v}')
            break