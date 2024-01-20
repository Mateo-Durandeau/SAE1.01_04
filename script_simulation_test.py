import sqlite3
import pandas as pd


####
#
#   Ce fichier fais des requêtes sur la base de données pour vérifier sa validité.
#
####

DATABASE_NAME = 'base_de_donnee_air_test.db'

def get_day_year_avg():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        requete_pd = f'''
        SELECT strftime('%Y', debut) as annee,
        nomPolluant,
        AVG(valeur) as moyenne_polluant
        FROM Mesure
        WHERE strftime('%m-%d', debut) = '01-01'
        GROUP BY annee, nomPolluant
        ORDER BY annee, nomPolluant;
        '''

        reponse_requete = pd.read_sql_query(requete_pd, conn)
        
        print('###############################################')
        print(reponse_requete) 
        print('###############################################')

        return reponse_requete
        
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
            LIMIT 5
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

def max_day():
    conn = sqlite3.connect(DATABASE_NAME)
    
    
    try:
        query_mesure_details = f'''
      WITH ranked_pollutants AS (
    SELECT
        debut,
        nomPolluant,
        valeur,
        ROW_NUMBER() OVER (PARTITION BY nomPolluant ORDER BY valeur DESC) as row_num
    FROM Mesure
            )
            SELECT
                debut,
                nomPolluant,
                valeur
            FROM ranked_pollutants
            WHERE row_num = 1
            ORDER BY debut, nomPolluant;


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




def simuler_scenario(nom_polluant, code_site, date_debut, date_fin):
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('base_de_donnee_air_test.db')
    cur = conn.cursor()

    # Extraction de la moyenne, du minimum et du maximum
    cur.execute('''
        SELECT
            AVG(valeur) as moyenne,
            MIN(valeur) as minimum,
            MAX(valeur) as maximum
        FROM Mesure
        WHERE
            nomPolluant = ? AND
            codeSite = ? AND
            debut BETWEEN ? AND ?;
    ''', (nom_polluant, code_site, date_debut, date_fin))

    resultats = cur.fetchone()
    moyenne, minimum, maximum = resultats

    # Affichage des résultats
    print(f"Statistiques pour le polluant {nom_polluant} au site {code_site} du {date_debut} au {date_fin}:")
    print(f"Moyenne: {moyenne:.2f}")
    print(f"Minimum: {minimum:.2f}")
    print(f"Maximum: {maximum:.2f}")

    # Fermeture de la connexion à la base de données
    conn.close()

# Exécution du scénario avec des paramètres spécifiques
simuler_scenario('NO2', 'FR01011', '2022-01-01 00:00:00', '2022-01-01 23:59:59')

stap_mesure = 250
polluant = 'NO'

get_day_year_avg()
get_mesure_details_by_polluant(stap_mesure, polluant)
#max_day()

