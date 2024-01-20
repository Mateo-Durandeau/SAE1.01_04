# script_test.py

import pytest
import sqlite3
import pandas as pd 
from database_manager import DatabaseManager
#from add_data_test import DatabaseManager


####
#
#   Ce fichier fais des tests avec pytest sur l'intégrité des données. par exemple tests l'ajout de mauvaises données ou du mauvais type.
####

DATABASE_FILE = 'base_de_donnee_air_test.db'

@pytest.fixture
def database_manager():
    return DatabaseManager(DATABASE_FILE)

def test_insert_site(database_manager):
    site_data = {
        'codeSite': '001',
        'nomSite': 'Site Test',
        'typeImplantation': 'Type A',
        'typeInfluence': 'Type X',
        'codeZas': 'Z001'
    }
    result = database_manager.insert_site(site_data)
    assert result == True

def test_get_site(database_manager):
    site = database_manager.get_site('001')
    assert site['nomSite'] == 'Site Test'
    assert site['typeImplantation'] == 'Type A'

def test_delete_site(database_manager):
    result = database_manager.delete_site('001')
    assert result == True

def test_insert_organisme(database_manager):
    organisme_data = {'nomOrganisme': 'Org Test'}
    result = database_manager.insert_organisme(organisme_data)
    assert result == True

def test_coherence_mesure(database_manager):
    site_data = {'codeSite': '001', 'nomSite': 'Site Test', 'typeImplantation': 'Type A', 'typeInfluence': 'Type X', 'codeZas': 'Z001'}
    organisme_data = {'nomOrganisme': 'Org Test'}
    polluant_data = {'nomPolluant': 'Polluant Test'}

    database_manager.insert_site(site_data)
    database_manager.insert_organisme(organisme_data)
    database_manager.insert_polluant(polluant_data)

    mesure_data = {
        'debut': '2024-01-20 12:00:00',
        'fin': '2024-01-20 13:00:00',
        'codeSite': '001',
        'nomPolluant': 'Polluant Test',
        'discriminant': 'Test',
        'reglementaire': 'Oui',
        'typeEvaluation': 'Type A',
        'procedureMesure': 'Proc A',
        'typeValeur': 'Type B',
        'valeur': 25.5,
        'valeurBrute': 30.0,
        'unite': 'mg/m³',
        'tauxSaisie': '100%',
        'couvertureTemporelle': '24h',
        'couvertureDonnees': '100%',
        'codeQualite': 'A',
        'validite': 1
    }

    result = database_manager.insert_mesure(mesure_data)
    assert result == True

def test_type_donnees_site(database_manager):
    site_data = {
        'codeSite': '001',
        'nomSite': 'Site Test',
        'typeImplantation': 'Type A',
        'typeInfluence': 'Type X',
        'codeZas': 'Z001'
    }
    result = database_manager.insert_site(site_data)
    assert result == True

    inserted_site = database_manager.get_site('001')
    assert isinstance(inserted_site['codeSite'], str)
    assert isinstance(inserted_site['nomSite'], str)
    assert isinstance(inserted_site['typeImplantation'], str)
    assert isinstance(inserted_site['typeInfluence'], str)
    assert isinstance(inserted_site['codeZas'], str)

def test_ajout_donnees_corrompues(database_manager):
    mesure_data_corrompue = {
        'debut': '2024-01-20 12:00:00',
        'fin': '2024-01-20 13:00:00',
        'codeSite': '001',
        'nomPolluant': 'Polluant Test',
        'discriminant': 'Test',
        'reglementaire': 'Oui',
        # ... (données manquantes ou incorrectes)
    }

    with pytest.raises(Exception):
        database_manager.insert_mesure(mesure_data_corrompue)
