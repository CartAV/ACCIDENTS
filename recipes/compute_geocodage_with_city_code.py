# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

class CityCodes():
    def __init__(self):
        try:
            import dataiku
            mydataset = dataiku.Dataset('laposte_hexasmal')
            poste = mydataset.get_dataframe(infer_with_pandas=False)
        except ImportError:
            poste = pd.read_csv('laposte_hexasmal.csv', sep=';', dtype={'Code_postal':str})
    
        self.city_codes_set = set(poste['Code_commune_INSEE'])
        # Marseille Lyon sont à part : leur code insee n'est pas dans les données ouvertes de la poste
        self.city_codes_set.add('13055')
        self.city_codes_set.add('69123')
        
        self.post_to_city_code = {}
        for row in poste.itertuples():
            self.post_to_city_code[row[3]] = row[1]
            
        self.old_insee = {
            '50602': '50129', # Tourlaville
            '50173': '50129', # Équeurdreville-Hainneville
            '50203': '50129', # Glacerie
            '50416': '50129', # Querqueville
            '59355': '59350', # Lomme
        }
     
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
    
    def city_code(self, departement, commune):
        """
        Transforme les identifiants des départements et des communes
        de la base d'accidents corporels en code INSEE si possible. Sinon, on tente de voir s'il
        correspond à un code postal dont on récupère le code INSEE. Sinon il est gardé tel quel.
        
        Code INSEE valable
        >>> c.city_code('750', '112')
        ('75112', 'Insee')
        
        Code INSEE non valable et code postal valable
        >>> c.city_code('750', '012')
        ('75112', 'Postal')
        
        Code non valable
        >>> c.city_code('750', '121')
        ('75121', 'Unknown')
        
        Le code Insee a changé (par exemple fusion)
        >>> c.city_code('500', '602')
        ('50129', 'Old insee code')
        """
        code = self.create_code(departement, commune)
        if self.is_in_insee(code):
            return (code, 'Insee')
        elif code in self.post_to_city_code:
            return (self.post_to_city_code[code], 'Postal')
        elif code in self.old_insee:
            return (self.old_insee[code], 'Old insee code')
        else:
            return (code, 'Unknown')
        
    def create_code(self, departement, commune):
        """Transforme les identifiants des départements et des communes
        de la base d'accidents corporels en code probablement INSEE
    
        >>> c.create_code('590', '309')
        '59309'

        Corse : le bon département doit être retourné    
        >>> c.create_code('201', '247')
        '2A247'
    
        Outre-Mer : le département est sur 3 caractères, la commune sur 2
        >>> c.create_code('972', '024')
        '97224'
        
        >>> c.create_code('130', '55')
        '13055'
        
        >>> c.create_code('10', '7')
        '01007'
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
        
        return departement + commune

c = CityCodes()

# Recipe inputs
geocodage_quali = dataiku.Dataset("geocodage_quali")
geocodage_quali_df = geocodage_quali.get_dataframe(infer_with_pandas=False)

geocodage_quali_df['city_code'] = geocodage_quali_df.apply(lambda x: c.city_code(x["dep"], x["com"])[0], axis = 1)
geocodage_quali_df['city_code_source'] = geocodage_quali_df.apply(lambda x: c.city_code(x["dep"], x["com"])[1], axis = 1)

# Recipe outputs
geocodage_with_city_code = dataiku.Dataset("geocodage_with_city_code")
geocodage_with_city_code.write_with_schema(geocodage_quali_df)


