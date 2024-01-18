import sqlite3
import pandas as pd


DATABASE_NAME = 'base_de_donnee_air_test.db'

# fonction requete verification.

def affiche_data_bdd():
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



def test_joiture_keys():
    # Étape 1: Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    
    # Étape 2: Utilisation de Pandas pour lire les données directement depuis la base de données
    try:
        t1 = pd.read_sql_query("...", conn)
        
    
    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SELECT * :", e)
    
    finally:
        # Étape 3: Fermeture de la connexion
        conn.close()

def get_name_organisme():
    conn = sqlite3.connect(DATABASE_NAME)
    
    try:
        # Requête pour récupérer les Zas pour un organisme donné
        nom_orga = f'''
            SELECT * FROM Organisme
        '''
        nom_organisme = pd.read_sql_query(nom_orga, conn)
        
        print("#############################################")
        print(nom_organisme)
        print("#############################################")
        
    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SELECT :", e)
    
    finally:
        # Fermeture de la connexion
        conn.close()

def get_zas_by_organisme(nom_organisme):
    # Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    
    try:
        # Requête pour récupérer les Zas pour un organisme donné
        query_zas_by_organisme = f'''
            SELECT Zas.*
            FROM Zas
            INNER JOIN Organisme ON Zas.nomOrganisme = Organisme.nomOrganisme
            WHERE Organisme.nomOrganisme = '{nom_organisme}'
        '''
        df_zas_by_organisme = pd.read_sql_query(query_zas_by_organisme, conn)
        
        print("#############################################")
        print(df_zas_by_organisme)
        print("#############################################")
        
    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SELECT :", e)
    
    finally:
        # Fermeture de la connexion
        conn.close()

def get_site_by_zas(code_zas):
    # Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    
    try:
        # Requête pour récupérer les informations d'un site pour une Zas donnée
        query_site_by_zas = f'''
            SELECT Site.*
            FROM Site
            WHERE Site.codeZas = '{code_zas}'
        '''

        df_site_by_zas = pd.read_sql_query(query_site_by_zas, conn)

        print("#############################################")
        print(df_site_by_zas)
        print("#############################################")

    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SELECT :", e)
    
    finally:
        # Fermeture de la connexion
        conn.close()

def get_polluants_and_valeurs(site_code, date_choisie):
    conn = sqlite3.connect(DATABASE_NAME)
    
    try:
        query_polluants_valeurs = f'''
            SELECT Mesure.nomPolluant, Mesure.valeur
            FROM Mesure
            WHERE Mesure.codeSite = '{site_code}' AND Mesure.debut = '{date_choisie}'
        '''
        df_polluants_valeurs = pd.read_sql_query(query_polluants_valeurs, conn)
        
        print("#############################################")
        print(df_polluants_valeurs)
        print("#############################################")

    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SELECT :", e)
    
    finally:
        conn.close()

def get_mesure_details_by_polluant(variable_mesure, nom_polluant):
    conn = sqlite3.connect(DATABASE_NAME)
    
    try:
        query_mesure_details = f'''
            SELECT Mesure.valeur, Mesure.debut, Site.nomSite, Zas.nomZas, Organisme.nomOrganisme, Polluant.nomPolluant
            FROM Mesure
            INNER JOIN Site ON Mesure.codeSite = Site.codeSite
            INNER JOIN Zas ON Site.codeZas = Zas.codeZas
            INNER JOIN Organisme ON Zas.nomOrganisme = Organisme.nomOrganisme
            INNER JOIN Polluant ON Mesure.nomPolluant = Polluant.nomPolluant
            WHERE Mesure.valeur > {variable_mesure}
            AND Polluant.nomPolluant = '{nom_polluant}'
            ORDER BY Mesure.valeur DESC
        '''
        df_mesure_details = pd.read_sql_query(query_mesure_details, conn)
        
        print('###############################################')
        print(df_mesure_details) 
        print('###############################################')

        return df_mesure_details
        
    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête SELECT :", e)
    
    finally:
        conn.close()




def extract_statistics():
    conn = sqlite3.connect(DATABASE_NAME)
    
    try:
        # Exemple : Calcul de la moyenne des valeurs pour chaque polluant
        query = '''
            SELECT nomPolluant, AVG(valeur) AS moyenne_valeur
            FROM Mesure
            GROUP BY nomPolluant
        '''
        df_statistics = pd.read_sql_query(query, conn)

        # Affichage des statistiques
        print("Statistiques des mesures par polluant :")
        print(df_statistics)

    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête :", e)

    finally:
        conn.close()

def group_by_organisme():
    conn = sqlite3.connect(DATABASE_NAME)
    
    try:
        # Exemple : Regroupement des mesures par organisme
        query = '''
            SELECT Organisme.nomOrganisme, COUNT(*) AS nombre_mesures
            FROM Mesure
            INNER JOIN Site ON Mesure.codeSite = Site.codeSite
            INNER JOIN Zas ON Site.codeZas = Zas.codeZas
            INNER JOIN Organisme ON Zas.nomOrganisme = Organisme.nomOrganisme
            GROUP BY Organisme.nomOrganisme
        '''
        df_grouped = pd.read_sql_query(query, conn)

        # Affichage des regroupements
        print("Regroupement des mesures par organisme :")
        print(df_grouped)

    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête :", e)

    finally:
        conn.close()

def apply_filters():
    conn = sqlite3.connect(DATABASE_NAME)
    
    try:
        # Exemple : Filtre des mesures pour un polluant spécifique et une heure donnée
        polluant_filtre = 'NO2'
        heure_filtre = 12

        query = f'''
            SELECT *
            FROM Mesure
            WHERE nomPolluant = '{polluant_filtre}' AND strftime('%H', debut) = '{heure_filtre}'
        '''
        df_filtered = pd.read_sql_query(query, conn)

        # Affichage des mesures filtrées
        print(f"Mesures filtrées pour le polluant {polluant_filtre} à {heure_filtre} heures :")
        print(df_filtered)

    except sqlite3.Error as e:
        print("Erreur lors de l'exécution de la requête :", e)

    finally:
        conn.close()


def test_scenario():
    extract_statistics()
    group_by_organisme()
    apply_filters()

if __name__ == "__main__":
    test_scenario()
    
