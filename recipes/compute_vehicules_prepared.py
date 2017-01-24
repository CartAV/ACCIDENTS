# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

def prepare(dataset):
    """ Prépare le jeux de données caractérisant les véhicules impliqués dans
    les accidents
    """

    labels = {
        'senc': {
            '0': '',
            '1': 'PK-PR-num rue croissant',
            '2': 'PK-PR-num rue décroissant',
        },
        # catégorie véhicules
        'catv': {
            '01': 'bicyclette',
            '02': 'cyclomoteur -50cm3',
            '03': 'voiturette',
            '04': 'scooter immatriculé (ref obsolète)',
            '05': 'motocyclette (ref obsolète)',
            '06': 'side-car (ref obsolète)',
            '07': 'voiture',
            '08': 'voiture+caravane (ref obsolète)',
            '09': 'voiture+remorque (ref obsolète)',
            '10': 'utilitaire',
            '11': 'utilitaire+caravane (ref obsolète)',
            '12': 'utilitaire+remorque (ref obsolète)',
            '13': 'poids lourd',
            '14': 'poids lourd',
            '15': 'poids lourd',
            '16': 'tracteur',
            '17': 'tracteur+semi-remorque',
            '18': 'transport en commun (ref obsolète)',
            '19': 'tramway (ref obsolète)',
            '20': 'engin spécial',
            '21': 'tracteur',
            '30': 'scooter -50cm3',
            '31': 'motocyclette +50cm3-125cm3',
            '33': 'motocyclette +125cm3',
            '34': 'scooter +125cm3',
            '35': 'quad -50cm3',
            '36': 'quad +50cm3',
            '37': 'bus',
            '39': 'train',
            '40': 'tramway',
            '99': 'autre véhicule'
        },
        'obsm': {
            '1': 'choc piéton',
            '2': 'choc véhicule',
            '4': 'choc sur rail',
            '6': 'choc animal domestique',
            '9': 'choc autre obstacle mobile'
        },
        'obs': {
            '1': 'Véhicule en stationnement',
            '2': 'Arbre',
            '3': 'Glissière métallique',
            '4': 'Glissière béton',
            '5': 'Autre glissière',
            '6': 'Bâtiment, mur, pile de pont',
            '7': "Support de signalisation verticale ou poste d'appel d'urgence",
            '8': 'Poteau',
            '9': 'Mobilier urbain',
            '10': 'Parapet',
            '11': 'Ilot, refuge, borne haute',
            '12': 'Bordure de trottoir',
            '13': 'Fossé, talus, paroi rocheuse',
            '14': 'Autre obstacle fixe sur chaussée',
            '15': 'Autre obstacle fixe sur trottoir ou accotement',
            '16': 'Sortie de chaussée sans obtacle'
        },
        'choc': {
            '1': 'avant',
            '2': 'avant droit',
            '3': 'avant gauche',
            '4': 'arrière',
            '5': 'arrière droit',
            '6': 'arrière gauche',
            '7': 'côté droit',
            '8': 'côté gauche',
            '9': 'multiples'
        },
        'manv': {
            '1': 'sans changement de direction',
            '2': 'même sens, même file',
            '3': 'entre 2 files',
            '4': 'en marche arrière',
            '5': 'à contresens',
            '6': 'en franchissant le terre-plein central',
            '7': 'dans le couloir bus, dans le même sens',
            '8': 'dans le couloir bus, dans le sens inverse',
            '9': "en s'insérant",
            '10': 'en faisant demi-tour sur la chaussée',
            '11': 'changeant de file à gauche',
            '12': 'changeant de file à droite',
            '13': 'déporté à gauche',
            '14': 'déporté à droite',
            '15': 'tournant à gauche',
            '16': 'tournant à droite',
            '17': 'tournant à gauche',
            '18': 'tournant à droite',
            '19': 'traversant la chaussée',
            '20': 'manoeuvre de stationnement',
            '21': "manoeuvre d'évitement",
            '22': 'ouverture de porte',
            '23': 'arrêté non stationné',
            '24': 'stationné'
        }
    }

    for key, values in labels.items():
        dataset[key] = dataset[key].map(values)

    return dataset



# Recipe inputs
accidents_vehicules = dataiku.Dataset("accidents_vehicules")
accidents_vehicules_df = accidents_vehicules.get_dataframe(infer_with_pandas=False)

prepared = prepare(accidents_vehicules_df)

# Recipe outputs
vehicules_prepared = dataiku.Dataset("vehicules_prepared")
vehicules_prepared.write_with_schema(prepared)
