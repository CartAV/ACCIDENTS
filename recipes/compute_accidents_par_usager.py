# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Recipe inputs
ds_in = dataiku.Dataset("accidents_par_usager_brut")
events = ds_in.get_dataframe(infer_with_pandas=False)

dico={
    'usagers': {
        'grav': {#gravité accident
            '2': 'tué',
            '3': 'hospitalisé',
            '4': 'blessé léger',
            '1': 'indemne',
        },
        'catu': {
            '1': 'conducteur',
            '2': 'passager',
            '3': 'piéton',
            '4': 'trottinette'
        },
        'sexe': {
            '1': 'homme',
            '2': 'femme'
        },
        'trajet': {
            '1': 'domicile travail',
            '2': 'domicile école',            
            '3': 'courses',
            '4': 'professionnel',
            '5': 'loisirs',
            '9': 'autres'
        },
        'secu': {
            '11': 'avec ceinture', '12': 'sans ceinture',
            '21': 'avec casque', '22': 'sans casque',
            '31': 'avec siège enfant', '32': 'sans siège enfant',
            '41': 'avec réflecteur', '42': 'sans réflecteur'
        },
        'locp': {
            0: '',
            1: 'plus de 50m un passage piéton',
            2: 'moins de 50m passage piéton',
            3: 'sans signalisation lumineuse',
            4: 'avec signalisation lumineuse'
        },
        'actp': {
            '0': '',
            '1': 'piéton sens véhicule',
            '2': 'piéton sens inverse véhicule',            
            '3': 'piéton traversant',
            '4': 'piéton masqué',
            '5': 'piéton jouant',
            '6': 'piéton avec animal',
        },
        'etatp': {
            '0': '',
            '1': 'piéton seul',
            '2': 'piéton accompagné',
            '3': 'piéton en groupe'
        }
    },
    'vehicules': {
        'senc': {
            '0': '',
            '1': 'PK-PR-num rue croissant',
            '2': 'PK-PR-num rue décroissant',
            },
        'catv': {#catégorie véhicules
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
            '12': 'utilitaire+remorque (ref obsolète)',            '13': 'poids lourd',
            '14': 'poids lourd',
            '15': 'poids lourd',
            '16': 'tracteur',
            '17': 'tracteur+semi-remorque',            
            '18': 'transport en commun (ref obsolète)',            
            '18': 'tramway (ref obsolète)',            
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
        'obs':{
            '1': 'Véhicule en stationnement',
            '2': 'Arbre',
            '3': 'Glissière métallique',
            '4': 'Glissière béton' ,
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
        'manv':{
            '1': 'sans changement de direction',
            '2': 'même sens, même file', 
            '3': 'entre 2 files', 
            '4': 'en marche arrière', 
            '5': 'à contresens', 
            '6': 'en franchissant le terre-plein central' ,
            '7': 'dans le couloir bus, dans le même sens' ,
            '8': 'dans le couloir bus, dans le sens inverse', 
            '9': "en s'insérant" ,
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
    },
    'lieux': {
        'catr': {
            '1': 'autoroute',
            '2': 'route nationale',
            '3': 'route départementale',
            '4': 'voie communale',
            '5': 'hors réseau public',
            '6': 'parking',
            '9': 'autre route'
        },
        'circ': {
            '1': 'sens unique',
            '2': 'bidirectionnel',
            '3': 'chaussées séparées',
            '4': 'affectation variable'
        },
        'vosp': {
            '1': 'piste cyclable',
            '2': 'banque cyclable',
            '3': 'voie réservée'
            },
        'prof': {
            '1': 'plat',
            '2': 'pente',
            '3': 'sommet de côte',
            '4': 'bas de côte'
            },
        'plan': {
            '1': 'rectiligne',
            '2': 'courbe à gauche',
            '3': 'courbe à droite',
            '4': 'en S'
        },
        'surf': {
            '1': 'surface normale',
            '2': 'surface mouillée',
            '3': 'flaques',
            '4': 'surface innondée',
            '5': 'surface enneigée',
            '6': 'boue',
            '7': 'surface verglacée',
            '8': 'corps gras-huile',
            '9': 'autre surface'
        },
        'infra': {
            '1': 'souterrain ou tunnel',
            '2': 'pont',
            '3': 'échangeur',
            '4': 'rails',
            '5': 'carrefour aménagé',
            '6': 'zone piétonne',
            '7': 'zone de péage'
        },
        'situ': {
            '1': 'chaussée',
            '2': "bande d'arrêt d'urgence",
            '3': 'accotement', 
            '4': 'trottoir', 
            '5': 'piste cyclable'
        },
        'env1': {
            '03': 'école proche'
        }
    },
    'caractéristiques': {
        'lum': {
            '1': 'plein jour',
            '2': 'crépuscule ou aube',
            '3': 'nuit sans éclairage public',
            '4': 'nuit avec éclairage public non allumé',
            '5': 'nuit avec éclairage public allumé'
        },
        'agg': {
            '1': 'hors agglomération',
            '2': 'en agglomération'
        },
        'int': {
            '1': 'hors intersection',
            '2': 'intersection en X',
            '3': 'intersection en T',
            '4': 'intersection en Y',
            '5': 'intersection +4 branches',
            '6': 'giratoire',
            '7': 'place',
            '8': 'passage à niveau',
            '9': 'autre intersection'
        },
        'atm': {
            '1': 'météo normale',
            '2': 'pluie légère',
            '3': 'pluie forte',
            '4': 'neige - grêle', 
            '5': 'brouillard - fumée',
            '6': 'vent fort - tempête',
            '7': 'temps éblouissant',
            '8': 'temps couvert', 
            '9': 'autre météo',
        },
        'col': {
            '1': '2 véhicules frontal',
            '2': "2 véhicules par l'arrière",
            '3': '2 véhicules côté',
            '4': '3+ véhicules en chaîne',
            '5': '3+ véhicules autre',
            '6': 'autre collision',
            '7': 'Sans collision'
        }
    }
}

for table in list(dico.keys()):
    print ">traduction {}".format(table)
    for key in list(dico[table].keys()):
        print ">>>> {}".format(key)
        events[key]=events[key].map(dico[table][key])



# Recipe outputs
ds_out = dataiku.Dataset("accidents_par_usager_valeurs")
ds_out.write_with_schema(events)
