from matplotlib import pyplot as plt
import numpy as np
from bsplines import *
from boor import Boor
from draggable_plot import *
from repositorioDatos import RepositorioDatos

def calcularInvNTNyNT(l, p, T, m, U, n): #Arreglar si hay k
    N = np.zeros(((m-1,n - l - 1)))

    for i in range(0, m -1):
      for k in range(0, n - l - 1):
        N[i][k] = basisFunction(k + 1, p, T[i + 1], U)

    N = np.array(N)
    NT = np.transpose(N)
    NTN = np.dot(NT, N)
 
    invNTN = np.linalg.inv(NTN)

    return [invNTN, NT]


p = int(input("Dé el grado del B-spline: "))
n = int(input("Mayor índice de puntos de control: "))

repo = RepositorioDatos()
Q = repo.obtenerPuntosQ()
Q= np.array(Q)
k=0
l=0
T = calculaT(Q)

m = len(Q) -1

U = calcularU(k, l, T, p, m, n)

[invNTN,NT] = calcularInvNTNyNT(l, p, T, m, U, n)

R = np.dot(NT,Q[1:-1])

numElemen = len(Q)
Pi = np.dot(invNTN,R)
if len(Q[0])==2:
  P = np.zeros((n+1,2), float) #Inicialización del vector de Puntos de Control
else:
  P = np.zeros((n+1,3), float)


contElement = 0
for i in range(len(P)): #Implementación sin derivadas 
  if i == 0:
    for j in range(len(P[i])):
      P[i][j] = Q[i][j]
  elif i == len(P)-1:
    for j in range(len(P[i])):
      P[-1][j] = Q[-1][j]
  else:
    for j in range(len(P[i])):
      P[i][j] = Pi[contElement][j]
    contElement += 1

grado = p
U = U[p:-p] #Reducción puntos repetidos

if len(Q[0]) ==2:
  (X, Y) = Boor(grado, P, U)
  plt.scatter(P[:,0], P[:,1],marker='o', color = 'black', label="Puntos de control") 
  plt.scatter(Q[:,0], Q[:,1],marker='X', color = 'green', label="Datos Q") 
  plt.plot(X,Y, color='purple', label="Curva B-spline") 
  plt.legend(loc="best")
  plt.title("Curva B-spline")
  plt.show()
else:
  (X, Y, Z) = Boor(grado, P, U)
  X = np.array([X])
  Y = np.array([Y])
  Z = np.array([Z])
  fig = plt.figure()
  ax1 = fig.add_subplot(111, projection='3d')
  ax1.plot_wireframe(X, Y, Z, color='purple', label="Curva B-spline") #Curva B-spline en tres dimensiones
  ax1.scatter(P[:,0], P[:,1], P[:,2], marker='o', color = 'black', label="Puntos de control") 
  ax1.scatter(Q[:,0], Q[:,1], Q[:,2],marker='X', color = 'green', label="Datos Q") 
  plt.legend(loc="best")
  plt.title("Curva B-spline")
  plt.show()  


