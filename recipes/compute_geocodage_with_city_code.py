# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

class CityCodes():
    def __init__(self):
        try:
            import dataiku
            mydataset = dataiku.Dataset("laposte_hexasmal")
            poste = mydataset.get_dataframe()
        except ImportError:
            poste = pd.read_csv('laposte_hexasmal.csv', sep=';', dtype={'Code_postal':str})
    
        self.city_codes_set = set(poste['Code_commune_INSEE'])
        self.post_to_city_code = {}
        for row in poste.itertuples():
            self.post_to_city_code[row[3]] = row[1]
     
    def is_in_insee(self, code):
        """
        >>> c.is_in_insee('40082')
        True
        
        >>> c.is_in_insee('75012')
        False
        """
        return code in self.city_codes_set
    
    def get_city_code(self, postcode):
        """
        >>> c.get_city_code('75012')
        '75112'
        
        >>> c.get_city_code('75112') is None
        True
        """
        return self.post_to_city_code.get(postcode, None)
    
    def city_code(self, departement, commune):
        """
        Transforme les identifiants des départements et des communes
        de la base d'accidents corporels en code INSEE si possible. Sinon, on tente de voir s'il
        correspond à un code postal dont on récupère le code INSEE. Sinon il est gardé tel quel.
        
        Code INSEE valable
        >>> c.city_code('750', '112')
        '75112'
        
        Code INSEE non valable et code postal valable
        >>> c.city_code('750', '012')
        '75112'
        
        Code non valable
        >>> c.city_code('750', '121')
        '75121'
        """
        code = self.create_code(departement, commune)
        if self.is_in_insee(code):
            return code
        else:
            return self.get_city_code(code) or code
        
    def create_code(self, departement, commune):
        """Transforme les identifiants des départements et des communes
        de la base d'accidents corporels en code probablement INSEE
    
        >>> c.create_code('590', '309')
        '59309'

        Corse : le bon département doit être retourné    
        >>> c.create_code('201', '247')
        '2A247'
    
        Outre-Mer : le premier chiffre de la commune correspond au dernier du département
        >>> c.create_code('972', '224')
        '97224'
        """

        if departement == '201':
            short_dep = '2A'
        elif departement == '202':
            short_dep = '2B'
        else:
            short_dep = departement[0:2]
        
        return short_dep + commune

c = CityCodes()

# Recipe inputs
geocodage_quali = dataiku.Dataset("geocodage_quali")
geocodage_quali_df = geocodage_quali.get_dataframe()

geocodage_quali_df.apply(lambda x: c.city_code(x["dep"], x["com"]), axis = 1)

# Recipe outputs
geocodage_with_city_code = dataiku.Dataset("geocodage_with_city_code")
geocodage_with_city_code.write_with_schema(geocodage_quali_df)


