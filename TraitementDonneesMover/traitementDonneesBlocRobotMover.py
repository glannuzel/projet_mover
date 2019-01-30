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
fichier = "log_mover_Gaelle.csv"
# Nombres d'allers-retours
nb_AR = 10

# Récupération du fichier
reader = csv.reader(open(fichier), delimiter=",")
file = list(reader)


def ringTranslator(matrice):
    """ 
    Fonction de translation du repère de l'effecteur au centre de l'anneau utilisé.
    """
    matriceAnneau = np.array([[1, 0, 0, 0.02], #(20.1mm)
                              [0, 1, 0, 0.02], #(20.1mm)
                              [0, 0, 1, 0.085], #(8.5cm)
                              [0, 0, 0, 1]])
    return matrice.dot(matriceAnneau)
        
        
# Récupération des différentes données 
timestamp = []
x_pos = []
y_pos = []
z_pos = []
temps_touche = []
compteur_end = 0
tableau_begin = []
tableau_end = []
begin = False
end = False

# Parcours toutes les données
for index, [temps,
            xixf, yixf, zizf,
            xiyf, yiyf, ziyf,
            xizf, yizf, zizf, 
            x, y, z,
            touche_debfin, touche] in enumerate(file[1:]):
    
    # Reconstitution de la matrice de la pose de l'effecteur
    matrice = np.array([[float(xixf), float(yixf), float(zizf), float(x)],
                        [float(xiyf), float(yiyf), float(ziyf), float(y)],
                        [float(xizf), float(yizf), float(zizf), float(z)],
                        [0, 0, 0, 1]])
    
    # Détermination de la pose de l'anneau exprimée dans le repère de base du robot
    matrice_transformee = ringTranslator(matrice)
    
    x = matrice_transformee[0][3]
    y = matrice_transformee[1][3]
    z = matrice_transformee[2][3]

    # Détermine le début de chaque aller-retour
    if touche_debfin == "BEGINNING":
        if len(tableau_begin) == 0:
            temps_debut = temps
            temps_debut_arduino = touche[5:]
        begin = True
        tableau_begin.append(touche)
        
    # Détermine la fin de chaque aller-retour
    if touche_debfin == "END":
        compteur_end +=1
        tableau_end.append(touche)
        if compteur_end >= nb_AR:
            end = True

    # Prend une donnée toute les 10 ms ou celles lors d'une touche
    if (index % 10 == 0 or touche != '0') and begin and not end :
        timestamp.append(float(temps) - float(temps_debut))
        x_pos.append(x)
        y_pos.append(y)
        z_pos.append(z)
        
        if touche_debfin == "TOUCHED":
            temps_touche.append(float(touche[5:])- float(temps_debut_arduino))
        else:
            temps_touche.append(0)

x_pos = np.array(x_pos).astype(float)
y_pos = np.array(y_pos).astype(float)
z_pos = np.array(z_pos).astype(float)
timestamp =  np.array(timestamp).astype(float)

# Représentation 3d de l'évolution de y et z au cours du temps
ax = Axes3D(fig)
ax.plot3D(timestamp, y_pos, z_pos)
plt.show() 

# Représentation de la position du centre de l'anneau en z par rapport à y
plt.plot(y_pos, z_pos)
plt.title("Position du centre de l'anneau en z par rapport à y")
plt.xlabel("y")
plt.ylabel("z")
plt.show()

# Représentation de la position du centre de l'anneau en x par rapport au temps
plt.plot(timestamp, x_pos)
somme = []
time_prec = 0
temps_debut_misa0 =[]
temps_fin_misa0 =[]
for touche, fin in zip(tableau_begin, tableau_end):
    time = float(touche[5:]) - float(temps_debut_arduino)
    time_fin = float(fin[5:]) - float(temps_debut_arduino)
    temps_debut_misa0.append(time)
    temps_fin_misa0.append(time_fin)

# Représentation de la position des débuts et fins d'aller-retour au cours du temps
    plt.axvline(x=time,color='k')
    plt.axvline(x=time_fin,color='r')
    somme.append(time_fin - time)
    
print("moyenne durée un aller-retour : ", np.asarray(somme).mean())
print("ecart type durée aller-retour : ", np.std(np.asarray(somme)))
print("range de valeur de position en x : ", np.asarray(x_pos).max() - np.asarray(x_pos).min())
print("Valeur moyenne de position en x : ", np.asarray(x_pos).mean())
print("Ecart type de position en x : ", np.asarray(x_pos).std())

# Représentation de la position du centre de l'anneau en x au cours du temps
plt.title("Position du centre de l'anneau en x au cours du temps.")
plt.xlabel("temps")
plt.ylabel("x")
plt.show() 

tourz = np.zeros((len(temps_debut_misa0), len(timestamp)), dtype=float)
toury = np.zeros((len(temps_debut_misa0), len(timestamp)), dtype=float)
tourx = np.zeros((len(temps_debut_misa0), len(timestamp)), dtype=float)
nb_touches = np.zeros(len(temps_debut_misa0), dtype=float)

for index, (deb, fin) in enumerate(zip(temps_debut_misa0, temps_fin_misa0)):
    compteur = 0
    for z, y, temps, touchette in zip(z_pos, y_pos, timestamp, temps_touche):
        if(float(temps) >= float(deb) and float(temps) <= float(fin)):
            if (touchette != 0 ):
                nb_touches[index] += 1
        
            compteur += 1
            tourz[index][compteur] = z
            tourx[index][compteur] = x
            toury[index][compteur] = y
            
moyenne = []
ecarttype = []

# Représentation de la position du centre de l'anneau en y et z au cours du temps zoom partie droite
plt.title("Position du centre de l'anneau en y et z au cours du temps zoom partie droite")
plt.xlabel("y")
plt.ylabel("z")
for index, tour in enumerate(tourz):
    zaffiche = []
    yaffiche = []

    for z, y in zip(tour, toury[index]):
        if (z > 0.48 and y > -0.4 and y < 0.2):
            zaffiche.append(z)
            yaffiche.append(y)
            


    moyenne.append(np.asarray(zaffiche).mean())
    ecarttype.append(np.std(np.asarray(zaffiche)))
    plt.plot(yaffiche, zaffiche)


plt.show()

print("Moyenne  en z sur la partie droite:", moyenne)
print("Ecart type en z sur la partie droite :", ecarttype)
print("Nombre de touches par tours :", nb_touches)

bar_index = []
for i in range(len(nb_touches)):
    bar_index.append(i)
    
# Représentation du nombre de touches par aller-retour
plt.title("Nombre de touches par aller-retour")
plt.xlabel("Numéro de l'essai")
plt.ylabel("Nombre de touches")
plt.bar(bar_index, nb_touches, width=0.8)
plt.show()
