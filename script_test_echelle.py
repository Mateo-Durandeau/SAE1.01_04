import pytest
import script_donnes_csv_data
import script_requete_download_http

import sqlite3


####
#
#   Ce script effectue des testes de perfomances sur l'ajout de données dans la base de données
#
####

def delete_all_data(database_name):
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()

        # Suppression de toutes les données de toutes les tables
        cur.execute('DELETE FROM Site;')
        cur.execute('DELETE FROM Zas;')
        cur.execute('DELETE FROM Organisme;')
        cur.execute('DELETE FROM Polluant;')
        cur.execute('DELETE FROM Mesure;')

        # Valider la transaction
        conn.commit()

        print("Toutes les données ont été supprimées avec succès.")

    except sqlite3.Error as e:
        print("Erreur lors de la suppression des données :", e)

    finally:
        # Fermeture de la connexion
        if conn:
            conn.close()





@pytest.mark.benchmark(group="download_and_insert")
def test_case(benchmark):
    #case = 6
    nombre_jour = 30
    year = 2021
    month = 7
    day = 1
    

    # Utilisez la fonction benchmark pour mesurer le temps d'exécution
    result = benchmark(choix_v2, nombre_jour, year, month, day)

    # Assurez-vous que la fonction benchmark a renvoyé une valeur
    assert result is not None, "Le benchmark n'a pas renvoyé de résultats valides"


def choix(case, year, month, day):
    delete_all_data('base_de_donnee_air_test.db')
    
    if case == 1:
        script_requete_download_http.download_day(year, month, day)
        script_donnes_csv_data.all_table_add(1, year, month, day)
    elif case == 2:
        script_requete_download_http.month_download(year, month)
        script_donnes_csv_data.all_table_add(2, year, month, day)
    elif case == 3:
        script_requete_download_http.download_week(year, month, day)
        script_donnes_csv_data.all_table_add(3, year, month, day)

    elif case == 4 : # 15 jours 
        script_requete_download_http.download_week(year, month, day)
        script_donnes_csv_data.all_table_add(3, year, month, day)
        day += 7
        script_requete_download_http.download_week(year, month, day)
        script_donnes_csv_data.all_table_add(3, year, month, day)

    elif case == 5: # 3 semaines
        script_requete_download_http.download_week(year, month, day)
        script_donnes_csv_data.all_table_add(3, year, month, day)
        day += 7
        script_requete_download_http.download_week(year, month, day)
        script_donnes_csv_data.all_table_add(3, year, month, day)
        day += 7
        script_requete_download_http.download_week(year, month, day)
        script_donnes_csv_data.all_table_add(3, year, month, day)

    
def choix_v2(nombre_jour, year, month, day):
    day = day
    day_test = day
    for i in range(0, nombre_jour):
        script_requete_download_http.download_day(year, month, day_test)
        script_donnes_csv_data.all_table_add(1, year, month, day_test)
        day_test += 1

if __name__ == '__main__':
    # Lorsque le script est exécuté directement, il utilise pytest.main() pour exécuter les tests
    pytest.main([__file__])
