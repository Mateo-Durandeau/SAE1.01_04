import script_donnes_csv_data
import script_requete_download_http

# attention verifier nom de la base de données

######################################################################
#
#           # READ ME
#
#       Ce script automatise le téléchargement, la gestion de doublon et l'ajout dans les bases de données avec la supprésion du fichier dans les dossiers
#
#       Case 1 = 1 jours 
#       Case 2 = 7 jours 
#       Case 3 = 1 mois
#
######################################################################


def choix(case, year, month, day):
    if case == 1:
        script_requete_download_http.download_day(year, month, day)
        script_donnes_csv_data.all_table_add(1, year, month, day)
    elif case == 2: 
        script_requete_download_http.month_download(year, month)
        script_donnes_csv_data.all_table_add(2, year, month, day)
    elif case == 3: 
        script_requete_download_http.download_week(year, month, day)
        script_donnes_csv_data.all_table_add(3, year, month, day)
    
    script_donnes_csv_data.affiche_mesure_bdd()

if __name__=='__main__':
    case = 2
    year = 2021
    month = 4
    day = 1
    choix(case, year, month, day)
