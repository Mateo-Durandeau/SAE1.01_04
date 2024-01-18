import script_donnes_csv_data
import script_requete_download_http

# attention verifier nom de la base de données

######################################################################
#
#           # READ ME
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
    
def choix_v2(nombre_jour, year, month, day):
    day = day
    day_test = day
    for i in range(0, nombre_jour):
        script_requete_download_http.download_day(year, month, day_test)
        script_donnes_csv_data.all_table_add(1, year, month, day_test)
        day_test += 1

if __name__=='__main__':

    nombre_jour = 1

    case = 1

    year = 2024
    month = 1
    day = 1

    choix(case, year, month, day)
    #choix_v2(nombre_jour, year, month, day)
