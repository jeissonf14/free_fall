import numpy as np
# ==============================================================================
# Funcion que calcula el coeficiente de arrastre de una esfera en caida libre
# Funciona con Reynolds descde 0 hasta m'as all'a de 3e6
# ==============================================================================
def Cd(u, D, nu):
    
    # Calculando el numero de Reynolds
    Re = u * D / nu
    
    # Definiendo el Coeficiente de arrastr C_d
    if Re == 0: 
        
        Cd = 0
    
    elif np.logical_and(Re > 0, Re <= 1):
        
        Cd = 24 / Re
        
    elif np.logical_and(Re > 1, Re <= 400):
        
        Cd = 24 / Re ** 0.646
        
    elif np.logical_and(Re > 400, Re <= 3e5):
        
        Cd = 0.5
        
    elif np.logical_and(Re > 3e5, Re <= 2e6):
        
        Cd = 0.000366 * Re ** 0.4275
        
    else: 
        
        Cd = 0.18
        
    return Cd

# ==============================================================================
# Funcion para calcular el paso incremental de RK4. 
# Funciona con el codigo de caida libre y es una funcion que es llamada desde 
# la siguiente funcion de este archivo
# ==============================================================================
def Fi(A, B, C, CD, x):
   
    vsq = x ** 2
    Fi = (1 / A) * (B - C * vsq * CD)
    
    return Fi

# ==============================================================================
# Funcion para definir los valores dvi y dzi. La funcion devuelve dos vectores
# que almacenan los valores de los incrementales
# ==============================================================================
def dv_dz(h, A, B, C, D, CD, V): 
    
    # Definiendo el vector donde serán almacenados los valores
    dv = np.zeros(4)
    dz = np.zeros_like(dv)
    
    # Calculo de incrementos para el metodo RK4
    dz[0] = h * V
    dv[0] = h * Fi(A, B, C, CD, V)
    dz[1] = h * (V + 0.5 * dv[0])
    dv[1] = h * (V + 0.5 * dv[0])
    dz[2] = h * (V + 0.5 * dv[1])
    dv[2] = h * Fi(A, B, C, CD, V + 0.5 * dv[1])
    dz[3] = h * (V + dv[2])
    dv[3] = h * Fi(A, B, C, CD, V + dv[2])
    
    return dv, dz