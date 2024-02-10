# database_manager.py

import sqlite3
import pandas as pd

####
#
#   Ce fichier fais des requêtes pour faire des testes sur la bdd
#
####

class DatabaseManager:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.cur = self.conn.cursor()

    def insert_site(self, site_data):
        try:
            self.cur.execute("INSERT INTO Site VALUES (?, ?, ?, ?, ?)", (site_data['codeSite'], site_data['nomSite'], site_data['typeImplantation'], site_data['typeInfluence'], site_data['codeZas']))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting site: {e}")
            return False

    def get_site(self, code_site):
        self.cur.execute("SELECT * FROM Site WHERE codeSite=?", (code_site,))
        site = self.cur.fetchone()
        if site:
            columns = [description[0] for description in self.cur.description]
            return dict(zip(columns, site))
        else:
            return None

    def delete_site(self, code_site):
        try:
            self.cur.execute("DELETE FROM Site WHERE codeSite=?", (code_site,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting site: {e}")
            return False

    def insert_organisme(self, organisme_data):
        try:
            self.cur.execute("INSERT INTO Organisme VALUES (?)", (organisme_data['nomOrganisme'],))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting organisme: {e}")
            return False

    def insert_mesure(self, mesure_data):
        # Implementer l'insertion pour la table "Mesure" de manière similaire
        pass

    # ... autres méthodes pour interagir avec la base de données

# test_database_manager.py

import pytest
from database_manager import DatabaseManager

DATABASE_FILE = 'base_de_donnee_air_test.db'

@pytest.fixture
def database_manager():
    return DatabaseManager(DATABASE_FILE)

# Les tests restent inchangés
# Assurez-vous d'adapter le fichier "test_database_manager.py" en fonction de l'implémentation réelle de votre classe DatabaseManager.
