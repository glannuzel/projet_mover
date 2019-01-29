# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:05:29 2019

@author: effie
"""

import matplotlib.pyplot as plt
import csv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Nom fichier à lire

fichier = "log_mover_Effie2.csv"

reader = csv.reader(open(fichier), delimiter=",")
file = list(reader)



def ringTranslator(matrice):
    matriceAnneau = np.array([[1, 0, 0, 0.02], #(20.1mm)
                              [0, 1, 0, 0.02], #(20.1mm)
                              [0, 0, 1, 0.085], #(8.5cm)
                              [0, 0, 0, 1]])
    return matrice.dot(matriceAnneau)
#result = np.array(x).astype("float")
        
        
# Récupération des différentes données 
timestamp = []
x_pos = []
y_pos = []
z_pos = []
temps_touche = []

print(file[1])
print("ok")
compteur_end = 0
tableau_begin = []
begin = False
end = False
nb_AR = 10
for index, [temps,
            xixf, yixf, zizf,
            xiyf, yiyf, ziyf,
            xizf, yizf, zizf, 
            x, y, z,
            touche_debfin, touche] in enumerate(file[1:]):
    matrice = np.array([[float(xixf), float(yixf), float(zizf), float(x)],
                        [float(xiyf), float(yiyf), float(ziyf), float(y)],
                        [float(xizf), float(yizf), float(zizf), float(z)],
                        [0, 0, 0, 1]])
    
    matrice_transformee = ringTranslator(matrice)
    
    x = matrice_transformee[0][3]
    y= matrice_transformee[1][3]
    z = matrice_transformee[2][3]

    
    if touche_debfin == "BEGINNING":
        if len(tableau_begin) == 0:
            temps_debut = temps
        begin = True
        tableau_begin.append(touche)
        
    if touche_debfin is "END":
        compteur_end +=1
        if compteur_end >= nb_AR:
            end = True

    if (index % 10 == 0 or touche is not 0) and begin and not end :
        timestamp.append(float(temps) - float(temps_debut))
        x_pos.append(x)
        y_pos.append(y)
        z_pos.append(z)
        temps_touche.append(touche)


print(timestamp[1])
x_pos = np.array(x_pos).astype(float)
y_pos = np.array(y_pos).astype(float)
z_pos = np.array(z_pos).astype(float)

timestamp =  np.array(timestamp).astype(float)
ax = Axes3D(fig)

print(len(timestamp[int(len(timestamp)*7/8):]))
print(len(timestamp))



ax.plot3D(timestamp, y_pos, z_pos)

plt.show() 

plt.plot(y_pos, z_pos)

plt.title("Position de l'effecteur du robot en y et z au cours du temps")
plt.xlabel("y")
plt.ylabel("z")

plt.show()
    
plt.plot(timestamp, x_pos)

plt.title("Position de l'effecteur du robot en x au cours du temps.")
plt.xlabel("temps")
plt.ylabel("x")

plt.show() 


print("ok")
        