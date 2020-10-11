import numpy as np

from funciones import Cd
from funciones import Fi
from funciones import dv_dz


def FreeFall(rho_f, rho_p, nu, D):
    
    # Constantes que no van a ser cambiadas por el usuario
    Z0 = 0                 # Altura inicial m
    V0 = 0                 # Velocidad inicial m/s
    h = 0.001              # Paso de tiempo s
    tf = 3                 # Tiempo final de simulacion s

    # Calculo de parametros principales que pueden ser realizados una sola vez
    RHO = rho_f / rho_p
    A = 1 + RHO * 0.5
    B = (1 - RHO) * 9.81
    C = 0.75 * RHO / (D / 1000)
    pasos = int(tf / h)
    
    # Crear los vectores donde voy a solucionar
    T = np.linspace(0, tf, pasos + 1)
    V = np.zeros_like(T)
    Z = np.zeros_like(T)
    Zv = np.zeros_like(T)
    Vv = np.zeros_like(T)
    
    # Imponer condiciones iniciales
    V[0] = V0
    Z[0] = Z0
    
    # Empezando el bucle temporal (la carne del asunto)
    for i in range(1, pasos + 1):

        # Calculando el coeficiente de arrastre por medio de la funcion externa
        CD = Cd(V[i - 1], D, nu)

        # Calculando los incrementales dentro de una funcion usando RK4
        # Metidos en una matriz para que pueda pasar los 8 valores necesarios
        vel = V[i - 1]
        DV, DZ = dv_dz(h, A, B, C, (D / 1000), CD, vel)

        # Con los valores incrementales calculados, se procede a calcular el siguiente 
        # valor de la funcion numericamente 
        Z[i] = Z[i - 1] + (1 / 6) * (DZ[0] + 2 * (DZ[1] + DZ[2]) + DZ[3])
        V[i] = V[i - 1] + (1 / 6) * (DV[0] + 2 * (DV[1] + DV[2]) + DV[3])

    return T, Z, V