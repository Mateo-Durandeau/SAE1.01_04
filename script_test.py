import pytest
import sqlite3
import add_data_test  # Assurez-vous d'importer le script approprié

DATABASE_NAME = 'base_de_donnee_air_test.db'

@pytest.fixture
def database_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    yield conn
    conn.close()

def test_ajout_mesure_correcte(database_connection):
    # Teste l'ajout de données correctes
    add_data_test.all_table_add(1, 2023, 1, 1)
    
    # Ajoutez des assertions pour vérifier que les données ont été correctement ajoutées
    # Vous pouvez vérifier le nombre de lignes dans la table Mesure, ou d'autres critères pertinents

def test_ajout_mauvaise_donnee(database_connection):
    # Teste l'ajout de mauvaises données
    add_data_test.add_bad_data()

    # Ajoutez des assertions pour vérifier que les mauvaises données n'ont pas été ajoutées

def test_gestion_doublon(database_connection):
    # Teste la gestion des doublons
    add_data_test.all_table_add(1, 2023, 1, 1)  # Ajout initial

    # Essaye d'ajouter les mêmes données à nouveau
    add_data_test.all_table_add(1, 2023, 1, 1)

    # Ajoutez des assertions pour vérifier que les doublons ont été gérés correctement

def test_coherence(database_connection):
    # Teste la cohérence des données
    add_data_test.add_incoherent_data()

    # Ajoutez des assertions pour vérifier que les données incohérentes n'ont pas été ajoutées

if __name__ == "__main__":
    pytest.main([__file__])
