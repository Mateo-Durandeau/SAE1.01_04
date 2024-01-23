from flask import request
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Assure la compatibilité de Matplotlib avec Flask
matplotlib.use('Agg')

# les mois de l'année
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre",'octobre',"novembre","décembre"]


def get_form():
    # on récupère les valeurs sélectionnées dans le formulaire
    mois = request.form.get("mois")
    jour = request.form.get('jour')
    polluant = request.form.get('polluant')
    seuil = request.form.get("seuil")

    # on modifie les valeurs qui causeraientt des erreurs
    mois = f"0{mois}" if mois in [str(i) for i in range(1,10)] else "01" if mois == None else mois
    jour = f"0{jour}" if jour in [str(i) for i in range(1,10)] else "01" if jour == None else jour
    polluant = "NO" if polluant == None else polluant
    seuil = "0" if seuil == None else seuil

    return mois,jour,polluant,seuil



def tracer_graphique(legende_x,legende_y,titre):
    # légende et titre
    plt.xlabel(legende_x)
    plt.ylabel(legende_y)
    plt.title(titre)

    # Convertion de l'histogramme en image
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convertion de l'image en format base64 pour l'inclure dans le template
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{image_base64}'


def tracer_courbe(donnees,polluant,jour,mois):
    # on filtre les mesures par rapport au polluant sélectionné
    donnees = donnees.query(f"nomPolluant == '{polluant}'")

    # on ne garde que le jour ou bien l'heure de la date
    if jour == "%":
        donnees["debut"] = donnees["debut"].str.split().str[0].str.split("-").str[2]
    else:
        donnees["debut"] = donnees["debut"].str.split().str[1].str.split(":").str[0]

    # on regroupe les mesure par date et on calcule les valeurs moyennes
    donnees = donnees.groupby("debut")["valeur"].mean().reset_index()

    # légende et titre
    legende_x = "temps"
    legende_y = 'concentration (µg-m3)'
    titre = f"évolution de la concentration de {polluant} {f'en {MOIS[mois]}' if jour == '%' else f'le {jour} {MOIS[mois]}'}"
    
    # on gérère la courbe 
    plt.figure(figsize=(10,4))
    plt.plot(donnees["debut"],donnees["valeur"], label=polluant)
    plt.legend()

    # on génère le reste du graphique
    return tracer_graphique(legende_x,legende_y,titre)

def tracer_histogramme(donnees,jour,mois):
    # on regroupe les mesures par polluant et on calcule les valeurs moyennes
    donnees = donnees.groupby("nomPolluant")["valeur"].mean().reset_index()

    # légende et titre
    legende_x = "Polluant"
    legende_y = "Concentration (µg-m3)"
    titre = f"Concentration moyenne des différents polluants {f'en {MOIS[mois]}' if jour == '%' else f'le {jour} {MOIS[mois]}'}"
    
    # on génère les bâtons
    plt.bar(donnees["nomPolluant"],donnees["valeur"])
    
    # on génère le reste du graphique
    return tracer_graphique(legende_x,legende_y,titre)