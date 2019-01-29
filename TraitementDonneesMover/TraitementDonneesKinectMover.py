# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 12:36:39 2019

@author: effie

Ce module permet de récupérer un fichier csv obtenu à partir d'un rosbag des
noeuds /PointCloudCorrectedTF ou /PointCloudCorrected et de les mettre sous 
la forme d'un fichier csv exploitable contenant uniquement les positions
des articulations, les longueurs des différents segments corporels et les
angles articulaires.
Les colonnes du dataframe sont constituées comme si après :
    A_B_C_D
    avec A le type de donnée (pos pour position, ang pour angle et long pour longueur)
    B l'axe concerné (x pour axe x, y pour axe y, z pour axe z et m si le terme n'est pas nécessaire)
    C aritulation/ partie du corps concernée
    D latéralisation (l pour gauche, r pour droit et m pour milieu)
"""
import pandas as pd

### Variables à modifier ###
code_sujet = '001'
fichier_traite = "_slash_PointCloudCorrectedTF.csv"
emplacement_fichier_csv = 'C:\\Users\\effie\\Desktop\\TestMover\\' # Attention doubler les \
nom_fichier_csv = 'montest_' + code_sujet

df1 = pd.read_csv(fichier_traite)

df1.rename(columns={'rosbagTimestamp' : 'keep_timestamp',
                     
                    'position':'keep_pos_x_ankle_l',

                     'position':'keep_pos_x_ankle_l',
                     'x':'keep_pos_y_ankle_l',
                     'y':'keep_pos_z_ankle_l',
                     
                     'name.1':'keep_pos_x_foot_l',
                     'position.1':'keep_pos_y_foot_l',
                     'x.1':'keep_pos_z_foot_l',
                     
                     '-.2':'keep_pos_x_ankle_r',
                     'name.2':'keep_pos_y_ankle_r',
                     'position.2':'keep_pos_z_ankle_r',
                     
                     'fiabilite.2':'keep_pos_x_foot_r',
                     '-.3':'keep_pos_y_foot_r',
                     'name.3':'keep_pos_z_foot_r',
                     
                     'z.3':'keep_pos_x_elbow_l',
                     'fiabilite.3':'keep_pos_y_elbow_l',
                     '-.4':'keep_pos_z_elbow_l',

                     'y.4':'keep_pos_x_elbow_r',
                     'z.4':'keep_pos_y_elbow_r',
                     'fiabilite.4':'keep_pos_z_elbow_r',
                     
                     'x.5':'keep_pos_x_hand_l',
                     'y.5':'keep_pos_y_hand_l',
                     'z.5':'keep_pos_z_hand_l',
                     ###
                     'position.6':'keep_pos_x_handtip_l',
                     'x.6':'keep_pos_y_handtip_l',
                     'y.6':'keep_pos_z_handtip_l',
                     
                     'name.7':'keep_pos_x_thumb_l',
                     'position.7':'keep_pos_y_thumb_l',
                     'x.7':'keep_pos_z_thumb_l',
                     
                     '-.8':'keep_pos_x_hand_r',
                     'name.8':'keep_pos_y_hand_r',
                     'position.8':'keep_pos_z_hand_r',
                     
                     'fiabilite.8':'keep_pos_x_handtip_r',
                     '-.9':'keep_pos_y_handtip_r',
                     'name.9':'keep_pos_z_handtip_r',
                     
                     'z.9':'keep_pos_x_thumb_r',
                     'fiabilite.9':'keep_pos_y_thumb_r',
                     '-.10':'keep_pos_z_thumb_r',

                     'y.10':'keep_pos_x_head_m',
                     'z.10':'keep_pos_y_head_m',
                     'fiabilite.10':'keep_pos_z_head_m',
                     
                     'x.11':'keep_pos_x_hip_l',
                     'y.11':'keep_pos_y_hip_l',
                     'z.11':'keep_pos_z_hip_l',

                     ###
                     'position.12':'keep_pos_x_hip_r',
                     'x.12':'keep_pos_y_hip_r',
                     'y.12':'keep_pos_z_hip_r',
                     
                     'name.13':'keep_pos_x_knee_l',
                     'position.13':'keep_pos_y_knee_l',
                     'x.13':'keep_pos_z_knee_l',
                     
                     '-.14':'keep_pos_x_knee_r',
                     'name.14':'keep_pos_y_knee_r',
                     'position.14':'keep_pos_z_knee_r',
                     
                     'fiabilite.14':'keep_pos_x_shoulder_l',
                     '-.15':'keep_pos_y_shoulder_l',
                     'name.15':'keep_pos_z_shoulder_l',
                     
                     'z.15':'keep_pos_x_shoulder_r',
                     'fiabilite.15':'keep_pos_y_shoulder_r',
                     '-.16':'keep_pos_z_shoulder_r',

                     'y.16':'keep_pos_x_spinbase_m',
                     'z.16':'keep_pos_y_spinbase_m',
                     'fiabilite.16':'keep_pos_z_spinbase_m',
                     
                     'x.17':'keep_pos_x_spinmid_m',
                     'y.17':'keep_pos_y_spinmid_m',
                     'z.17':'keep_pos_z_spinmid_m',
                     
                     ###
                     'position.18':'keep_pos_x_spinshoulder_m',
                     'x.18':'keep_pos_y_spinshoulder_m',
                     'y.18':'keep_pos_z_spinshoulder_m',
                     
                     'name.19':'keep_pos_x_neck_m',
                     'position.19':'keep_pos_y_neck_m',
                     'x.19':'keep_pos_z_neck_m',
                     
                     '-.20':'keep_pos_x_wrist_l',
                     'name.20':'keep_pos_y_wrist_l',
                     'position.20':'keep_pos_z_wrist_l',
                     
                     'fiabilite.20':'keep_pos_x_wrist_r',
                     '-.21':'keep_pos_y_wrist_r',
                     'name.21':'keep_pos_z_wrist_r',
                     
                     
                     ## Fin pos début angles
                     'name.43':'keep_matrice_nom',
                     'position.43':'keep_matrice_valeur'                                                               
                     }, 
                 inplace=True)

# Enlève les colonnes que l'on ne veut pas
for colonne in df1.columns:
 if colonne.split('_')[0] != 'keep':
     df1 = df1.drop([colonne], axis = 1)

# Enlève le flag keep des colonnes à garder
 else :
    df1.rename(columns={colonne : colonne[5:]}, 
                 inplace=True)

# Récupération des tableaux de longueur et d'angle
ar = []
indexeur = []
temp =[]
for index in df1['timestamp'][:]:
    indexeur.append(index)
for data in df1['matrice_valeur']:
    for item in data.split(','):
        if item[0]=='[':
            item = item[1:]
        if item[-1] == ']':
            item = item[:-1]
        temp.append(item)
    ar.append(temp)
    temp = []

col = ['long_x_spinbase_m', 'long_y_spinbase_m', 'long_z_spinbase_m',
       'long_x_base_m', 'long_y_base_m', 'long_z_base_m',
       'long_FE_thorax_m', 'long_IL_thorax_m',
       'long_FE_tete_m', 'long_IL_tete_m',
       'ang_PR_clavicule_r', 'ang_ED_clavicule_r',
       'ang_PE_epaule_r', 'ang_E_epaule_r', 'ang_RA_epaule_r',
       'ang_FE_coude_r',
       'ang_FE_poignet_r', 'ang_E_poignet_r',
       'ang_PR_clavicule_l', 'ang_ED_clavicule_l',
       'ang_PE_epaule_l', 'ang_E_epaule_l', 'ang_RA_epaule_l',
       'ang_FE_coude_l',
       'ang_FE_poignet_l', 'ang_E_poignet_l',
       'long_m_abdomen_m', 'long_m_thorax_m', 'long_m_tete_m', 'long_m_clavicule_m',
       'long_m_humerus_m','long_m_radius_m', 'long_m_main_m',
       'ang_FE_hanche_r', 'ang_AA_hanche_r', 'ang_RA_hanche_r',
       'ang_FE_genou_r',
       'ang_FE_hanche_l', 'ang_AA_hanche_l', 'ang_RA_hanche_l',
       'ang_FE_genou_l',
       'long_A_pelvis_m', 'long_L_pelvis_m', 'long_ML_pelvis_m',
       'long_m_femur_m', 'long_m_tibia_m'       
       ]

df2 = pd.DataFrame(ar, index = indexeur, columns = col)

# DataFrame fixant le nom du sujet
nom_sujet = pd.DataFrame(len(indexeur)*[code_sujet],index = indexeur, columns = ['nom_sujet'])

# Manipulations pour joindre les deux dataframes
df1 = df1.set_index('timestamp')
df1 = df1.drop(['matrice_nom', 'matrice_valeur'], axis = 1)
dataframe_finale = pd.concat([nom_sujet, df1, df2], axis=1, sort=False)

# Enregistrement sous format csv
chemin = ''+emplacement_fichier_csv+nom_fichier_csv+'.csv'
dataframe_finale.to_csv(chemin, index=True, sep=',', encoding='utf-8')
