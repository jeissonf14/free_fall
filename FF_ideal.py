import numpy as np

def FF_V(Z0, V0, h, tf):

    # Calculando la posicion y la velocidad cuando una esfera cae en el vacio
    # Caso ideal
    
    # Recalcular la variable pasos para no traérmela
    pasos = int(tf / h)
    
    # Definiendo los vectores donde almacenaré posición y velocidad
    Vv = np.zeros(pasos + 1)
    Zv = np.zeros(pasos + 1)    
    
    # Calcular las posiciones y velocidades en medio sin fricción
    for i in range(1, pasos + 1):
        
        # Cálculo de la velocidad en el vacío
        Vv[i] = V0 + 9.81 * (h * i)
        
        # Cálculo de la posición en el vacío
        Zv[i] = Z0 + V0 * (h * i) + 0.5 * 9.81 * (h * i) ** 2
        
    return (Zv, Vv)