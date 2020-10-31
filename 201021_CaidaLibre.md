```python
# Importando librerias 
%reset -f

# Rutinas que requiere el sistema. 
import numpy as np
import matplotlib.pyplot as plt

# Esto controla el tamaño de las figuras en el script 
plt.rcParams['figure.figsize'] = (16,8)

import ipywidgets as ipw
from ipywidgets import widgets, interact_manual

# Las rutinas que calculan posiciones y velocidades
from F_FreeFall import FreeFall
from FF_ideal import FF_V

# Esto es para poder correr todo en linea
ipw.interact_manual.opts['manual_name'] = "CALCULAR!"
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
```

# **CAÍDA LIBRE DE UNA ESFERA EN UN FLUIDO**




**Variables utilizadas**

A contiunuación se presenta una lista de las variables que se utilizan en el desdarrollo del presente taller con sus respectivas unidades de medida:

$\rho_f \ (kg/m^3) \ = \ $ Densidad del fluido en el que cae la esfera 

$\rho_p \ (kg/m^3) \ = \ $ Densidad de la partícula que cae en el fluido

$D_p \ (mm) \ = \ $ Diámetro de la partícula que cae en el fluido

$\nu_f \ (m^2/s) \ = \ $ Viscosidad cinemática del fluido 

**Suposiciones**

* La posición inicial de la partícula es $z = 0 \ m$ y $z$ aumenta en el sentido del movimiento
* La partícula inicia su movimiento desde el reposo. Es decir, su velocidad inicial es $v_0 = 0 m/s$
* La densidad de la partícula siempre debe ser mayor que la densidad del fluido para garantizar su caída
* La fuerza de fricción ocasionada por el movimiento es proporcional al cuadrado de la velocidad $(F_f \ \alpha \  \lvert v \rvert ^2)$

**Valores iniciales**

Para el desarrollo del presente problema se asume que una esfera de vidrio de diámtro $D_p \ = \ 10 \ mm$ y densidad $\rho_p \ = \ 2200 \ kg/m^3$ cae en agua con densidad $\rho_f \ = \ 1000 \ kg/m^3$ y viscosidad cinemática $\nu_f \ = \ 1,14 \times 10^{-6} \ m^2/s$.

Estos valores se dberán cambiar para observar los cambios en la caída libre de diferentes objetos en diferentes fluidos. El estudiante deberá investigar las diferentes propiedades de los fluidos en cualquier libro de texto de la asignatura. 


```python
# ===========================================================================
# Se define una función que engloba todo y corre el problema de caída libre 
# cuando se definen los valores de los parámetros que se van a variar para
# el desarrollo dle problema
# ===========================================================================
def RUN_ALL(rho_f, rho_p, nu, D):
    
    # Las condiciones iniciales del problema están "hard coded". No se puede
    # cambiar esta situación a menos que se cambien las funciones que hacen 
    # los cálculos (Acá se ponen estas variables que son las mismas de la 
    # rutina de cálculos)
    Z0 = 0
    V0 = 0
    h = 1e-3
    tf = 3
    
    # Se construye la variable ANSW que almacenará los vectores que serán 
    # graficados. EL orden es el siguiente: T, Zi, Vi, Z, V
    ANSW = np.zeros((5, int(tf / h) + 1))
    
    # Esto corre el caso ideal que no tiene fricción (la idea es poder 
    # comparar lo que sucede en los dos casos)
    ANSW[1, :], ANSW[2, :] =  FF_V(Z0, V0, h, tf)
    
    # Esto corre lo referente al caso con fricción y rozamiento
    ANSW[0, :], ANSW[3, :], ANSW[4, :] = FreeFall(rho_f, rho_p, nu, D)
    
    # Llamando a una función que haga gráficas bonitas en cuanto se refiere
    # a colores, fuentes y manejo del espacio
    plotresults(ANSW)
    
```


```python
# ===========================================================================
# Haciendo la figura yu poniéndola bonita para efectos de poder entrar a 
# hacerla en un app. Vamos a ver si la hacemos funcionar. 
# ===========================================================================
def plotresults(ANSW):
    
    # plt.style.use('ggplot')
    fig = plt.figure(facecolor="white");
    # fig = plt.subplots(nrows = 1, ncols = 2, sharey = True)
        
    # Para reducir espacio
    Labels = ["Posición teórica", "Posición real", "Velocidad Teórica", 
             "Velocidad Real"]
    
    # Librería de colores (a lo mejor y no uso ninguno)
    Colors = ["darkmagenta","darkgreen","seagreen","dodgerblue","dimgrey"]
    FaceColors = ["lavenderblush","honeydew","mintcream","aliceblue","whitesmoke"]
    
    # Haciendo las gráficas por separado para que sea fácil poder cambiar
    # No necesito hacer ciclos porque son muy pocas. 
    # Gráfica de posiciones contra tiempo
    ax1 = plt.subplot(1, 2, 1)
    ax1.plot(ANSW[0, :], ANSW[1, :], label=Labels[0],c=Colors[0],lw=3, linestyle=':')
    ax1.plot(ANSW[0, :], ANSW[3, :], label=Labels[1],c=Colors[0],lw=3)
    ax1.set_ylim([0, 4])
    ax1.set_xlim([0, 2.5])
    ax1.set_facecolor(FaceColors[0])
    # ax1.text(45,(ANSW[0,0]+ANSW[0,-1])/2,"Posición",\
    #          fontdict={'weight':'bold','size':10,'color':Colors[0]})
    
    # Gráfica de velocidades
    ax2 = plt.subplot(1, 2, 2)
    ax2.plot(ANSW[0, :], ANSW[2, :], label=Labels[2],c=Colors[3],lw=3, linestyle=':')
    ax2.plot(ANSW[0, :], ANSW[4, :], label=Labels[3],c=Colors[3],lw=3)
    ax2.set_ylim([0, 4])
    ax2.set_xlim([0, 2.5])
    ax2.set_facecolor(FaceColors[3])
    # ax2.text(45,(ANSW[0,0]+ANSW[0,-1])/2,"Velocidad",\
    #          fontdict={'weight':'bold','size':10,'color':Colors[1]})
    
    # Mostrando los resultados en el notebook
    plt.show()
```


```python
# ===========================================================================
# Funcion que corre todo lo que he progrmado y hace que salgan los sliders 
# para determinar los diferentes parámetros que gobiernan el fenómeno de la 
# caída libre de cuerpos en un fluido (desde el reposo)
# ===========================================================================

# Descripción de los sliders 
DESCR = [r"$\rho_f \ (kg/m^3)$",\
         r"$\rho_p \ (kg/m^3)$",\
         r"$\nu_f \ (m^2/s)$",\
         r"$D_p \ (mm)$"]

# Correr todo y poner los sliders en la pantalla
interact_manual(RUN_ALL, \
rho_f=widgets.FloatText(description=DESCR[0], min=600, max=2000, value=1000 , step=10, readout_format='.1f'),\
rho_p=widgets.FloatText(description=DESCR[1], min=2000, max=1e4, value=2200 , step=10, readout_format='.1f'),\
nu=widgets.FloatText(description=DESCR[2], value=1.14e-6 , disabled=False, readout_format='E'),\
D=widgets.FloatText(description=DESCR[3], min=0.1, max=100 , value=10   , step=.1, readout_format='.1f'));
```


    interactive(children=(FloatText(value=1000.0, description='$\\rho_f \\ (kg/m^3)$', step=10.0), FloatText(value…



```python
# Imprimiendo las dependencias para que esto pueda funcionar. 
%load_ext watermark

# python, ipython, packages, and machine characteristics
%watermark -v -m -p numpy,matplotlib,watermark 

# date
print (" ")
%watermark -u -n -t -z
```

    CPython 3.7.8
    IPython 7.16.1
    
    numpy 1.16.2
    matplotlib 3.0.2
    watermark 2.0.2
    
    compiler   : GCC 7.5.0
    system     : Linux
    release    : 4.19.112+
    machine    : x86_64
    processor  : x86_64
    CPU cores  : 8
    interpreter: 64bit
     
    last updated: Sat Oct 31 2020 18:19:43 UTC

