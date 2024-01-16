import csv
import sqlite3
import pandas as pd
from datetime import datetime
import os 
import requests

#############################################################################################
#   READ ME 
#############################################################################################
#  
# 
#       Les fonctions suivantes permettent de charger les données du serveur HTTP : https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/ 
#       Geod'air qui regroupe un ensemble de données sur 4 ans de la concentration de polluants atmoshèriques sur plusieurs sites géo. Dans une base de données crée avec le fichier : script_creation_bdd
#       
#       Les fonctions ce-dessous permettent de lire des fichiers CSV qui contiennent ces données et de les mettres dans le bon type de données dans un tableau de tuples.
#       Elles sont ensuite ajouté dans la base de données avec les modules sqlite3 et des requêtes pour chaque ligne des tableaus crée. 
#
#       Panda assure les requêtes pour la vérification des données sur la data_base 
#       Un système de sauvegarde de nom de fichier upload dans la bdd à été mise en place pour éviter les doublons
#
#       On peut ajouter les données sur 1 jours, 7 jours ou 1 mois --> Ces données doivent être téléchargé en amont, en fichier CSV à partir du fichier : script_requete_download_http.py qui fais des requêtes au serveur http
#
#       fonction qui permettent un fonctionnement automatique sur l'ensemble de la base de donénes. fonctions :  Voir description pour savoir le fonctionnement
#
#           - all_table_add(case, year, month, day):  --> ajout des données dans les 5 tables de la bases de données
#           - affiche_mesure_bdd(): --> vérification des données dans la table 
#           - def file_csv_tables(csv_name): --> Vérification des tableaux sous le bon format 
#
#       # Voir pdf sur la base de données pour plus d'informations
#
#############################################################################################



##############################################################################################
# Variable global || Si changement ne pas oublier de supprimer les anciennes données créee
##############################################################################################


# Si changement de base de données, changer la variable global DATABASE_NAME
DATABASE_NAME = 'base_de_donnee_air_test.db'

# Si changement de fichier de sauvegarde, changer la variable global SAVE_NAME
SAVE_NAME = 'fichier_save_name.csv'



##############################################################################################
# Lecture fichiers csv   
##############################################################################################

def read_csv(name):
    tab = []
    with open(name, 'r', newline='', encoding='utf-8') as fichier:
        lecteur_csv = csv.reader(fichier, delimiter=';')
        for ligne in lecteur_csv:
            tab.append(ligne)
    return tab


##############################################################################################
#  Ajout des données du fichier csv dans un tableau
##############################################################################################

def add_values_table(tab, tab_table, tab_final, tab_selec):

    # Parcours d'une ligne du fichier CSV
    for lignes in tab: 
        # Exctraction des champs pour une table précis dans un tableau
        for number in tab_table:
            values = lignes[number]
            tab_selec.append(values)
        # Ajout dans le tableau final pour l'ajout des données dans la table
        tab_final.append(tab_selec)
        # reinitialisatoin du tableau pour faire une nouvelle ligne
        tab_selec = []


##############################################################################################
# Création de tableaux tuples  --> pour ajout dans le base de données avec une REQUETE 
##############################################################################################

def selection(name_csv, selection_tables):
    """
    Cette fonction retourne un tableau des champs à remplir dans les tables selon la base de données AIR
    selection de la table 
    1 = Mesure 
    2 = organisme 
    3 = Polluant 
    4 = Site
    5 = Zas
    """

    tab = read_csv(name_csv)
    tab_selec = []
    tab_final = []

    ### selection des champs
    tab_mesure = [0, 1, 5, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    tab_organisme = [2]
    tab_polluant = [8]
    tab_site = [5, 6, 7, 9, 3]
    tab_zas = [3, 4, 2]


    if (selection_tables == 1):
        add_values_table(tab, tab_mesure, tab_final, tab_selec)
    if (selection_tables == 2):
        add_values_table(tab, tab_organisme, tab_final, tab_selec)
    if (selection_tables == 3):
        add_values_table(tab, tab_polluant, tab_final, tab_selec)
    if (selection_tables == 4):
        add_values_table(tab, tab_site, tab_final, tab_selec)
    if (selection_tables == 5):
        add_values_table(tab, tab_zas, tab_final, tab_selec)


    del tab_final[0]

    # mise en forme des sous tableau en forme de tuples ma compréhension
    sous_tableau_tuples = [tuple(ligne) for ligne in tab_final]

    return sous_tableau_tuples

##############################################################################################
# changement de type sur les données mesures pour le bon format 
##############################################################################################


def types_tuples_mesure(table_final):
    """ Cette fonction permet de transformer les types qui ne sont pas des str pour les avoir sous le bon format dans la table mesure (La seul qui a des types hors str)"""
    typed_table = []

    for elements in table_final:
        debut = str(elements[0])
        fin = str(elements[1])
        # transformation des types des dates au format iso 8601
        debut = datetime.strptime(debut, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        fin = datetime.strptime(fin, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        # création du tuple d'une ligne de données 
        typed_row = (
            debut,  # debut
            fin,  # fin
            str(elements[2]),  # codeSite
            str(elements[3]),  # nomPolluant
            str(elements[4]),  # discriminant
            str(elements[5]),  # reglementaire
            str(elements[6]),  # typeEvaluation
            str(elements[7]),  # procedureMesure
            str(elements[8]),  # typeValeur
            float(elements[9]) if elements[9] else 0.0,  # valeur
            float(elements[10]) if elements[10] else 0.0,  # valeurBrute
            str(elements[11]),  # unite
            str(elements[12]),  # tauxSaisie
            str(elements[13]),  # couvertureTemporelle
            str(elements[14]),  # couvertureDonnees
            str(elements[15]),  # codeQualite
            int(elements[16])
        )
        typed_table.append(typed_row)

    return typed_table

##############################################################################################
# Verification des données dans les tableaux de tuples
##############################################################################################


def file_csv_tables(csv_name):
    tab_mesure = selection(csv_name, 1)
    tab_organisme = selection(csv_name, 2)
    tab_polluant = selection(csv_name, 3)
    tab_Site = selection(csv_name, 4)
    tab_zas = selection(csv_name, 5)

    tab_mesure = types_tuples_mesure(tab_mesure)

    print(tab_mesure[0])
    print(tab_organisme[0])
    print(tab_polluant[0])
    print(tab_Site[0])
    print(tab_zas[0])

##############################################################################################
# ajout des noms dans le fichier sauvegarde.    
##############################################################################################


def write_fichier_save(name_tab):
    with open(SAVE_NAME, 'a', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier, delimiter=';') 
        writer.writerows([[name] for name in name_tab])

    print('Ligne écrite avec succès dans : ', SAVE_NAME)


##############################################################################################
# Création du nom des fichiers 
##############################################################################################
    
    
def test_day(day, year, month):
    """ Définition du nom de fichier à télécharger """
    return f"save/FR_E2_{year}-{month:02d}-{day:02d}.csv"


def tab_crea_auto(case, year, number_month, day_start):
    """ Création des noms pour l'automatisation de l'ajout des données dans les tables/bases de données """
    # tableau qui sauvegarde les noms des fichiers 
    tab = []

    # verification des mois pair impair et fevrier 
    if number_month == 2: 
        max_jours = 28
    elif (number_month % 2) != 0:
        max_jours = 31
    else:
        max_jours = 30

    if case == 1: 
        name = test_day(day_start, year, number_month)
        tab.append(name)
    elif case == 2: 
        for i in range(1, max_jours + 1):
            name = test_day(i, year, number_month)
            tab.append(name)
    elif case == 3:
        for i in range(1, 7 + 1):
            day = i + day_start - 1
            name = test_day(day, year, number_month)
            tab.append(name)

    ############
    #  ouverture du fichier de sauvegarde pour verifier si un fichier csv à deja été mis dans la base de données            
    ############
                
    # Créer le fichier de sauvegarde s'il n'existe pas
    if not os.path.exists(SAVE_NAME):
        open(SAVE_NAME, 'w').close()

    # tableau qui sauvegarde le nom des fichiers deja upload dans la bdd            
    tab_save = []

    # Lecture du fichier de sauvegarde
    with open(SAVE_NAME, 'r', newline='', encoding='utf-8') as fichier:
        lecteur_csv = csv.reader(fichier, delimiter=';')
        for ligne in lecteur_csv:
            tab_save.append(ligne)

    # Liste temporaire pour stocker les noms à conserver
    temp_tab = []

    # Parcourir les noms
    for i in range(len(tab)):
    # Vérifier si le nom est dans la liste de sauvegarde
        nom_trouve = False
        for name in tab_save:
            if name[0] == tab[i]:
                nom_trouve = True
                break
    
        # Si le nom n'a pas été trouvé, l'ajouter à la liste temporaire
        if not nom_trouve:
            temp_tab.append(tab[i])

   
    # Réaffectation de la liste tab avec la liste temporaire filtrée
    if tab_save != []:
        tab = temp_tab

    print("Données ajouté dans la bdd : ", tab)

    # Ecriture des fichier qui viennt d'être ajouté dans le fichier de sauvegarde
    write_fichier_save(tab)

    return tab




##############################################################################################
# insertion des données dans les tables avec 3 cas possibles.  
##############################################################################################

def mesure_case_add(tab):


    # Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insérer les données dans la table existante
    insert_query = '''
        INSERT INTO Mesure (
            debut, fin, codeSite, nomPolluant, discriminant,
            reglemantaire, typeEvaluation, procedureMesure, typeValeur,
            valeur, valeurBrute, unite, tauxSaisie, couvertureTemporelle,
            couvertureDonnees, codeQualite, validite
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    for csv_name in tab:
        # Sélectionner les données à partir du fichier CSV
        tab_mesure = selection(csv_name, 1)
        tab_mesure = types_tuples_mesure(tab_mesure)

        # Insérer les données dans la base de données
        cursor.executemany(insert_query, tab_mesure)

    print("Données mesure ajouté ! ")
    # Valider la transaction et fermer la connexion
    conn.commit()
    conn.close()

def organisme_case_add(tab):


    # Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insérer les données dans la table existante
    insert_query = '''
        INSERT OR IGNORE INTO Organisme (nomOrganisme) VALUES (?)
    '''

    for csv_name in tab:
        # Sélectionner les données à partir du fichier CSV
        tab_organisme = selection(csv_name, 2)

        # Insérer les données dans la base de données
        cursor.executemany(insert_query, tab_organisme)

    print("Données organisme ajouté ! ")
    # Valider la transaction et fermer la connexion
    conn.commit()
    conn.close()

def polluant_case_add(tab):


    # Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insérer les données dans la table existante
    insert_query = '''
        INSERT OR IGNORE INTO Polluant (nomPolluant) VALUES (?);
    '''

    for csv_name in tab:
        # Sélectionner les données à partir du fichier CSV
        tab_polluant = selection(csv_name, 3)

        # Insérer les données dans la base de données
        cursor.executemany(insert_query, tab_polluant)

    print("Données Polluant ajouté ! ")
    # Valider la transaction et fermer la connexion
    conn.commit()
    conn.close()

def site_case_add(tab):


    # Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insérer les données dans la table existante
    insert_query = '''
        INSERT OR IGNORE INTO Site (codeSite, nomSite, typeImplantation, typeInfluence, codeZas) VALUES (?, ?, ?, ?, ?);
    '''

    for csv_name in tab:
        # Sélectionner les données à partir du fichier CSV
        tab_site = selection(csv_name, 4)

        # Insérer les données dans la base de données
        cursor.executemany(insert_query, tab_site)

    # Valider la transaction et fermer la connexion
    print("Données Site ajouté ! ")    
    conn.commit()
    conn.close()

def zas_case_add(tab):

    # # Étape 1: Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # # Étape 2: Création de la requete 
    insert_query = '''
        INSERT OR IGNORE INTO Zas (codeZas, nomZas, nomOrganisme) VALUES (?, ?, ?);
    '''

    for csv_name in tab:
        # Sélectionner les données à partir du fichier CSV
        tab_zas = selection(csv_name, 5)

        # Insérer les données dans la base de données
        cursor.executemany(insert_query, tab_zas)

    print("Données Zas ajouté ! ")
    # Valider la transaction et fermer la connexion
    conn.commit()
    conn.close()

def case_add(tab):
    # # Étape 1: Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

#############################################################################################
    ### Different cas : ##### 1 = 1 jour ##### 2 = 1 mois ##### 3 = 7 jours ##
    ## ajout des données des 5 tables
#############################################################################################

def all_table_add(case, year, month, day):
    tab = tab_crea_auto(case, year, month, day)

    mesure_case_add(tab)
    organisme_case_add(tab)
    polluant_case_add(tab)
    site_case_add(tab)
    zas_case_add(tab)

    delete_file()


##############################################################################################
# supprésion des fichiers sur l'ordinateur présent dans la bdd
##############################################################################################


def delete_file():

    try:
        # Liste tous les fichiers dans le répertoire
        files = os.listdir('save')

        for file_name in files:
            try:
                # Construction du chemin complet du fichier
                file_path = os.path.join('save', file_name)

                # Vérification si le chemin est un fichier (et non un sous-répertoire)
                if os.path.isfile(file_path):
                    # Suppression du fichier
                    os.remove(file_path)
                    print(f"Fichier {file_name} supprimé avec succès.")
                else:
                    print(f"{file_name} n'est pas un fichier et n'a pas été supprimé.")
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier {file_name}: {str(e)}")

        print("Suppression des fichiers terminée.")
    except Exception as e:
        print(f"Erreur lors de la récupération de la liste des fichiers : {str(e)}")








##############################################################################################
# Requete pour verifier si les données sont présentent dans la bdd    
##############################################################################################

def affiche_mesure_bdd():
    # Étape 1: Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    
    # Étape 2: Utilisation de Pandas pour lire les données directement depuis la base de données
    try:
        t1 = pd.read_sql_query("SELECT * FROM Mesure limit 10", conn)
        t2 = pd.read_sql_query("SELECT * FROM Organisme limit 10", conn)
        t3 = pd.read_sql_query("SELECT * FROM Polluant limit 10", conn)
        t4 = pd.read_sql_query("SELECT * FROM Site limit 10", conn)
        t5 = pd.read_sql_query("SELECT * FROM Zas limit 10", conn)

        # Affichage du DataFrame
        print("############################################################")
        print(t1)
        print("############################################################")
        print(t2)
        print("############################################################")
        print(t3)
        print("############################################################")
        print(t4)
        print("############################################################")
        print(t5)
        print("############################################################")
    
    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SELECT * :", e)
    
    finally:
        # Étape 3: Fermeture de la connexion
        conn.close()




##############################################################################################
# Appel fonction principal     
##############################################################################################
        


##
#
# nom des tables dans l'ordre de mise en place des données : Mesure Organisme Polluant Site Zas
#
## Different cas : ##### 1 = 1 jour ##### 2 = 1 mois ##### 3 = 7 jours ####
#
# Si les fichiers ne sont pas téléchargé il faut le faire dans le script : script_requete_download_http.py
#
##
        
if __name__ == '__main__':


    # choix des paramètres pour l'upload des données
    choix = 2
    annee = 2023
    mois = 12
    jour = 1
    
    #all_table_add(choix, annee, mois, jour)
    #tab = tab_crea_auto(1, annee, mois, jour)
    

    # verification    
    #affiche_mesure_bdd()
    
