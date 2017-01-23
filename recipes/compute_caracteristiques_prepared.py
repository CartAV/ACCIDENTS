# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# -*- coding: utf-8
import pandas as pd


def fillna(dataset):
    return dataset.fillna(axis=1, value={
        'col': '0',
        'com': '000',
        'atm': '1',
        })


def invalid_coordinates(lon, lat):
    return (abs(lat) < 10 or abs(lon) < 10 or
            (lat % 1000 == 0 and lon % 1000 == 0))


def process_coordinates(row):
    """
    >>> def c(lon, lat, g='M'): return({'long': lon, 'lat': lat, 'gps': g})
    ...
    >>> process_coordinates(c('a', '120000'))
    {'lat': None, 'long': None, 'gps': 'M'}

    >>> process_coordinates(c('0000000', '0000000'))
    {'lat': None, 'long': None, 'gps': 'M'}

    >>> process_coordinates(c('4951000', '242000'))
    {'lat': None, 'long': None, 'gps': 'M'}

    >>> process_coordinates(c('4951000', '242100'))
    {'lat': 2.421, 'long': 49.51, 'gps': 'M'}

    >>> process_coordinates(c('5549770', '2114500', 'R'))
    {'lat': -21.145, 'long': 55.4977, 'gps': 'R'}

    >>> process_coordinates(c('5549770', '-2114500', 'Y'))
    {'lat': -21.145, 'long': 55.4977, 'gps': 'Y'}

    >>> process_coordinates(c('6099990', '1463010', 'A'))
    {'lat': 14.6301, 'long': -60.9999, 'gps': 'A'}
    """
    try:
        lon, lat = int(row['long']), int(row['lat'])
        if invalid_coordinates(lon, lat):
            row['long'] = row['lat'] = None
        else:
            row['lat'] = lat / 100000.0
            row['long'] = lon / 100000.0
            # La Réunion
            if row['gps'] in ('R', 'Y'):
                row['lat'] = - abs(row['lat'])
            # Guadeloupe et Martinique
            if row['gps'] in ('G', 'A'):
                row['long'] = - abs(row['long'])
    except (TypeError, ValueError):
        row['lat'] = row['long'] = None
    return row


def fix_coordinates(dataset):
    return dataset.apply(process_coordinates, axis=1)

def parse_date(dataset):
    return dataset.apply(
        lambda row: pd.to_datetime(
            "20%02d%02d%02d%04d".format(
            row['an'], row['mois'], row['jour'], row['hrmn'])))


def prepare(dataset):
    labels = {
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

    dataset = fillna(dataset)

    for key, values in labels.items():
        dataset[key] = dataset[key].map(values)

    dataset = process_coordinates(dataset)
    dataset['date'] = parse_date(dataset)

    return dataset


# Recipe inputs
accidents_caracteristiques = dataiku.Dataset("accidents_caracteristiques")
accidents_caracteristiques_df = accidents_caracteristiques.get_dataframe(infer_with_pandas=False)

prepared = prepare(accidents_caracteristiques_df)
# Recipe outputs
caracteristiques_prepared = dataiku.Dataset("caracteristiques_prepared")
caracteristiques_prepared.write_with_schema(prepared)
