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

fichier = "log_mover_test2.csv"

reader = csv.reader(open(fichier), delimiter=",")
file = list(reader)

#result = np.array(x).astype("float")
        
        
# Récupération des différentes données 
timestamp = []
x_pos = []
y_pos = []
z_pos = []
temps_touche = []

print(file[1])
print("ok")
begin = False
end = False

for index, [temps, x, y, z, touche_debfin, touche] in enumerate(file[1:]):
    if touche_debfin == "BEGINNING":
        temps_debut = temps
        begin = True
        
    if touche_debfin is "END":
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
plt.ylabel("z")

plt.show() 


print("ok")
        