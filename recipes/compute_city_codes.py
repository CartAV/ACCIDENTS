# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu


class CityCodes():
    def __init__(self):
        try:
            import dataiku
            mydataset = dataiku.Dataset("DATAPREPOPENDATAGEO.2016_codes_postaux_prep")
            poste = mydataset.get_dataframe(infer_with_pandas=False)
        except ImportError:
            poste = pd.read_csv(
                'laposte_hexasmal.csv',
                sep=';',
                dtype={'Code_postal': str})

        self.city_codes_set = set(poste['Code_commune_INSEE'])
        # Marseille Lyon sont à part : leur code insee n'est pas dans les
        # données ouvertes de la poste
        self.city_codes_set.add('13055')
        self.city_codes_set.add('69123')

        self.post_to_city_code = {}
        for row in poste.itertuples():
            self.post_to_city_code[row[3]] = row[1]


    def is_in_insee(self, code):
        """
        >>> c.is_in_insee('40082')
        True

        >>> c.is_in_insee('75012')
        False

        >>> c.is_in_insee('13055')
        True
        """
        return code in self.city_codes_set

    def city_code(self, departement, commune, date=''):
        """
        Transforme les identifiants des départements et des communes de la
        base d'accidents corporels en code INSEE si possible. Sinon, on tente
        de voir s'il correspond à un code postal dont on récupère le code
        INSEE. Sinon il est gardé tel quel.

        Code INSEE valable
        >>> c.city_code('750', '112')
        ('75112', 'Insee', '75')

        Code INSEE non valable et code postal valable
        >>> c.city_code('750', '012')
        ('75112', 'Postal', '75')

        Code non valable
        >>> c.city_code('750', '121')
        ('75121', 'Unknown', '75')

        Le code Insee a changé (par exemple fusion)
        >>> c.city_code('500', '602', '2005-01-01')
        ('50129', 'Old insee code', '50')
        """
        (code, dep) = self.create_code(departement, commune)

        if self.is_in_insee(code):
            return [code, 'Insee', dep]
        elif code in self.post_to_city_code:
            return [self.post_to_city_code[code], 'Postal', dep]
        else:
            return [code, 'Unknown', dep]

    def create_code(self, departement, commune):
        """Transforme les identifiants des départements et des communes de la
        base d'accidents corporels en code probablement INSEE. Renvoit
        également le numéro du département.

        >>> c.create_code('590', '309')
        ('59309', '59')

        Corse : le bon département doit être retourné
        >>> c.create_code('201', '247')
        ('2A247', '2A')

        Outre-Mer : le département est sur 3 caractères, la commune sur 2
        >>> c.create_code('972', '024')
        ('97224', '972')

        >>> c.create_code('130', '55')
        ('13055', '13')

        >>> c.create_code('10', '7')
        ('01007', '01')
        """

        departement = departement.zfill(3)
        commune = commune.zfill(3)

        if departement == '201':
            departement = '2A'
        elif departement == '202':
            departement = '2B'
        elif departement[0:2] in ['97', '98']:
            commune = commune[1:3]
        else:
            departement = departement[0:2]

        return (departement + commune, departement)


c = CityCodes()

# Recipe inputs
geocodage_quali = dataiku.Dataset("caracteristiques_prepared")
geocodage_quali_df = geocodage_quali.get_dataframe(infer_with_pandas=False)


geocodage_quali_df[['city_code', 'city_code_source', 'dep']] = geocodage_quali_df[['dep', 'com', 'date']].apply(lambda x: c.city_code(x["dep"], x["com"], str(x["date"])), axis = 1)
#geocodage_quali_df[] = geocodage_quali_df.apply(lambda x: c.city_code(x["dep"], x["com"], str(x["date"]))[1], axis = 1)
#geocodage_quali_df['dep'] = geocodage_quali_df.apply(lambda x: c.city_code(x["dep"], x["com"])[2], axis = 1)

# Recipe outputs
geocodage_with_city_code = dataiku.Dataset("caracteristiques_prepared2")
geocodage_with_city_code.write_with_schema(geocodage_quali_df)


