import numpy as np

skin = 0
wellbore_radius = 0.3125
conversion = 0.001127
penetration_direction = 'k'
x_permeability = 0.001
y_permeability = 0.001
z_permeability = 0.0001

x_dimension = 50
y_dimension = 50
z_dimension = 1

if penetration_direction == 'i':
    equivalent_radius = 0.28 * (z_dimension ** 2 * (y_permeability / z_permeability) ** 0.5 + y_dimension ** 2 * (
            x_permeability / y_permeability) ** 0.5) ** 0.5 / ((y_permeability / z_permeability) ** 0.25 + (
            x_permeability / y_permeability) ** 0.25)
    transmissibility = conversion * 2 * np.pi * x_permeability * x_dimension / (
                np.log(equivalent_radius / wellbore_radius) + skin)
elif penetration_direction =='j':
    equivalent_radius = 0.28 * (x_dimension ** 2 * (z_permeability / x_permeability) ** 0.5 + z_dimension ** 2 * (
            x_permeability / z_permeability) ** 0.5) ** 0.5 / ((z_permeability / x_permeability) ** 0.25 + (
            x_permeability / z_permeability) ** 0.25)
    transmissibility = conversion * 2 * np.pi * y_permeability * y_dimension / (
                np.log(equivalent_radius / wellbore_radius) + skin)
elif penetration_direction =='k':
    equivalent_radius = 0.28 * (x_dimension ** 2 * (y_permeability / x_permeability) ** 0.5 + y_dimension ** 2 * (
            x_permeability / y_permeability) ** 0.5) ** 0.5 / ((y_permeability / x_permeability) ** 0.25 + (
            x_permeability / y_permeability) ** 0.25)
    transmissibility = conversion * 2 * np.pi * z_permeability * z_dimension / (
                np.log(equivalent_radius / wellbore_radius) + skin)

print(equivalent_radius)
print(transmissibility)
