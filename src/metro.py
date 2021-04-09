import math
import time
import networkx as nx
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from data import *

# (H) Devuelve el tiempo calculado a partir de la distancia calculada a partir de las coordenadas
def coorTiemp(est1, est2):
    #Distancia entre coordenadas * Variable para pasar de coordenadas a km * Variable para pasar de km a m * Variable para pasar de m a s (los trenes van a 80km/h o 22.222m/s)
    return math.sqrt((getCoorLat(est1)-getCoorLat(est2))**2 + (getCoorLong(est1)-getCoorLong(est2))**2) * 87.736 * 1000 / 22.222

def getCoorLat(est):
    return coor[est][0]

def getCoorLong(est):
    return coor[est][1]

#Creación de grafo
G = nx.Graph()
for x in l:
    # (G) Se pasan los km de distancia a m y luego a s y se le suma al resultado el tiempo de espera entre estaciones (60 segundos)
    G.add_edge(x[0], x[1], weight=(x[2] * 1000 / 22.222) + 60)

#Algoritmo A*
def astar(est1, est2):
    return nx.astar_path(G, est1, est2, heuristic=coorTiemp, weight="weight")

#Devuelve una impresión a limpio de trayecto con horas y cambios de línea
def astarPrint(sol):
    hora = datetime.now()
    i = 1
    lineaActual = lineaNueva(sol[0], sol[1])
    printo = ''
    printo += ('Tiempo estimado de trayecto: ' + time.strftime('%H:%M', tTotal(sol)) + ' \n\n')

    printo += ('• ' + '[' + hora.strftime("%H:%M") + '] ' + sol[0] + '\n|\n|‣‣‣ Suba a la línea ' + lineaActual + '\n')

    while i < len(sol)-1:
        hora = nHora(sol[i-1], sol[i], hora)
        printo += ('|\n• ' + '[' + hora.strftime("%H:%M") + '] '+ sol[i] + '\n')
        if transbordo(lineaActual, sol[i+1]):
            lineaActual = lineaNueva(sol[i], sol[i+1])
            printo += ('|\n|‣‣‣ Cambie a la línea ' + lineaActual + '\n')
        i += 1

    hora = nHora(sol[i-1], sol[i], hora)
    printo += ('|\n○ ' + '[' + hora.strftime("%H:%M") + '] ' + sol[i] + '\n')
    return printo

#Devuelve el tiempo total del trayecto
def tTotal(sol):
    total = 0
    i = 0
    while i < len(sol)-1:
        total += G.get_edge_data(sol[i], sol[i+1]).get('weight')
        i+=1
    total = time.gmtime(total)
    return total

#Devuelve la hora estimada de llegada a la estación
def nHora(est1, est2, hora):
    sec = G.get_edge_data(est1, est2)
    nHora = hora + timedelta(seconds=sec.get('weight'))
    return nHora

#Devuelve true si es necesario cambiar de línea
def transbordo(lineaActual, estSig):
    for x in coor[estSig][2]:
        if(str(x) == lineaActual):
            return False
    return True

#Devuelve la línea inicial
def lineaNueva(est1, est2):
    for x in coor[est1][2]:
        for y in coor[est2][2]:
            if(x == y):
                return str(x)
            

#Pruebas
#print(coorTiemp('Kiffisia', 'KAT'))
#print(coorTiemp('Kalithea', 'Moschato'))
#print(coorTiemp('Piroeus', 'Airport'))
#print(coorTiemp('Airport', 'Piroeus'))
#print(coorTiemp('Airport', 'Airport'))
#
#print(realDist('Megaro Moussikis', 'Evangelismos'))
#print(realDist('Evangelismos', 'Megaro Moussikis'))
#print(realDist('Monastiraki', 'Thissio'))
#print(realDist('Monastiraki', 'Syntagma'))
#
#print(getBrotherNodes('Syntagma'))
#print(getBrotherNodes('Kiffisia'))
#print(getBrotherNodes('KAT'))

#nx.draw(G, with_labels=True)
#plt.show()
#nx.draw_planar(G, with_labels=True)
#plt.show()

#sol = astar('Sepolia', 'Akropoli')
#print(sol)
#print('')
#astarPrint(sol)
#sol = astar('Kiffisia', 'Airport')
#print(sol)
#print('')
#astarPrint(sol)