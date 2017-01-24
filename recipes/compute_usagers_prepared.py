# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu


def prepare(dataset):
    """ Prépare le jeux de données caractérisant les usagers impliqués dans
    les accidents
    """

    labels = {
        # Gravité accident
        'grav': {
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
        'actp': {
            '0': '',
            '1': 'piéton sens véhicule',
            '2': 'piéton sens inverse véhicule',
            '3': 'piéton traversant',
            '4': 'piéton masqué',
            '5': 'piéton jouant',
            '6': 'piéton avec animal',
        },
        'locp': {
            '0': '',
            '1': 'plus de 50m un passage piéton',
            '2': 'moins de 50m passage piéton',
            '3': 'sans signalisation lumineuse',
            '4': 'avec signalisation lumineuse'
        },
        'etatp': {
            '0': '',
            '1': 'piéton seul',
            '2': 'piéton accompagné',
            '3': 'piéton en groupe'
        }
    }

    for key, values in labels.items():
        dataset[key] = dataset[key].map(values)

    return dataset



# Recipe inputs
accidents_usagers = dataiku.Dataset("accidents_usagers")
accidents_usagers_df = accidents_usagers.get_dataframe(infer_with_pandas=False)

prepared = prepare(accidents_usagers_df)

# Recipe outputs
usagers_prepared = dataiku.Dataset("usagers_prepared")
usagers_prepared.write_with_schema(prepared)
