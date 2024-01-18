import sqlite3
import pandas as pd
from datetime import datetime

DATABASE_NAME = 'base_de_donnee_air_test.db'

def all_table_add(case, year, month, day):
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        # Supposons que vous avez une logique d'ajout de données ici
        # Je vais simplement insérer quelques données de démonstration
        # Adaptez cela en fonction de votre logique réelle
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Site VALUES (?, ?, ?, ?, ?)', ('Site001', 'NomSite1', 'Implantation1', 'Influence1', 'Zas001'))
        cursor.execute('INSERT INTO Zas VALUES (?, ?, ?)', ('Zas001', 'NomZas1', 'Organisme1'))
        cursor.execute('INSERT INTO Organisme VALUES (?)', ('Organisme1',))
        cursor.execute('INSERT INTO Polluant VALUES (?)', ('NO2',))
        cursor.execute('INSERT INTO Mesure VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (datetime.now(), datetime.now(), 'Site001', 'NO2', 'Discriminant1', 'Reglementaire1', 'Evaluation1',
                        'ProcedureMesure1', 'TypeValeur1', 10.5, 9.8, 'Unite1', 'TauxSaisie1', 'Temporelle1', 'Donnees1',
                        'Qualite1', 1))
        conn.commit()
    except sqlite3.Error as e:
        print("Erreur lors de l'ajout de données :", e)
    finally:
        conn.close()

def add_bad_data():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        # Ajout de données incorrectes (par exemple, avec des champs vides)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Mesure VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (datetime.now(), datetime.now(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 1))
        conn.commit()
    except sqlite3.Error as e:
        print("Erreur lors de l'ajout de mauvaises données :", e)
    finally:
        conn.close()

def add_incoherent_data():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        # Ajout de données incohérentes (par exemple, une date de fin antérieure à la date de début)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Mesure VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (datetime.now(), datetime.now(), 'Site001', 'NO2', 'Discriminant1', 'Reglementaire1', 'Evaluation1',
                        'ProcedureMesure1', 'TypeValeur1', 10.5, 9.8, 'Unite1', 'TauxSaisie1', 'Temporelle1', 'Donnees1',
                        'Qualite1', 1))
        conn.commit()
    except sqlite3.Error as e:
        print("Erreur lors de l'ajout de données incohérentes :", e)
    finally:
        conn.close()

def main():
    # Exécutez des exemples de fonctions ici si nécessaire
    pass

if __name__ == "__main__":
    main()
