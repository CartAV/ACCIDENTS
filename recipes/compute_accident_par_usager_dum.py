# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import distance

# Recipe inputs
ds_in = dataiku.Dataset("accidents_par_usager")
df = ds_in.get_dataframe()
print("chargement initial")    


nrows=len(df.index)
threshold=0.02*float(nrows)



liste=('catv','obs','obsm','choc','manv','catu','place','grav','sexe','age','actp','secu','env1','etatp','trajet')
for key in liste:
    print("dummies : "+key)    
    df=pd.concat([df,pd.get_dummies(df[key],prefix="DUM_"+key,prefix_sep=" ")],axis=1)

liste=('LIBELLE_NATURE','MARQUE','NATIONALITE_PLAQUE')
for key in liste:
    print("signicative dummies : "+key)    
    values = df[key]
    counts = pd.value_counts(values)
    #filtre les valeurs présentées à moins de (threshold) %
    mask = values.isin(counts[counts > threshold].index)
    df=pd.concat([df,pd.get_dummies(values[mask],prefix="DUM_"+key,prefix_sep=" ")],axis=1)

print("écriture finale")    

# Recipe outputs
ds_out = dataiku.Dataset("accident_par_usager_dum")
ds_out.write_with_schema(df)
