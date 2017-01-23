# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Recipe inputs
accidents_lieux = dataiku.Dataset("accidents_lieux")
accidents_lieux_df = accidents_lieux.get_dataframe()

prepared = prepare(accidents_lieux_df)

# Recipe outputs
lieux_prepared = dataiku.Dataset("lieux_prepared")
lieux_prepared.write_with_schema(prepared)

def prepare(dataset):
    """ Prépare le jeux de données caractérisant les lieux d'accident

    >>> csv = pd.readcsv("Num_Acc,catr,voie,v1,v2,circ,nbv,pr,pr1,vosp,prof,plan,lartpc,larrout,surf,infra,situ,env1
200500000001,3,00041,0,B,2,02,1,430,0,1,1,000,063,1,0,1,00")
    >>> prepare(csv)
    ...
    """
    labels = {
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
    }

    for key, values in labels.items():
        dataset[key] = dataset[key].map(values)

    return dataset
