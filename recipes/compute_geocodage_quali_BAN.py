# -*- coding: utf-8 -*-
import dataiku as d
import os.path
import codecs, io, StringIO, requests
import pandas as pd, numpy as np
import concurrent.futures
from sklearn.utils import shuffle
from dataiku import pandasutils as pdu
from collections import OrderedDict

# Recipe inputs
f = d.Dataset("accidents_par_usager")
i=0
liste=[]
futures=[]
split=500
verbosechunksize=2000
maxtries=4
nthreads=3
j=0

def adresse_submit(df):
    global i
    s = StringIO.StringIO()
    i+=split
    if ((i%verbosechunksize)==0):
        print("geocoding chunk %r to %r" %(i-verbosechunksize,i))
    t=1
    while (t<=maxtries):
        df_adr=df[["Num_Acc","adr","city_code"]]
        df_adr.to_csv(s,sep=",", quotechar='"',encoding="utf8",index=False)
        requests_session = requests.Session()
        kwargs = {
            'data': OrderedDict([                     
                    ('columns', 'adr'), 
                    ('citycode', 'city_code')
              ]),
            'method': 'post',
            'files': OrderedDict([
                ('data', s.getvalue())
            ]),
            'stream': True,
            'timeout':500,
            'url': 'http://fa-srv-1/search/csv/'
        }
    
        response = requests_session.request(**kwargs)
        if (response.status_code == 200):
            res=pd.read_csv(StringIO.StringIO(response.content.decode('utf-8')),sep=",",quotechar='"')
            res=pd.merge(df,res,how='left',on=['Num_Acc','v1','adr','code_insee'])
            t=maxtries+1
        elif (response.status_code == 400):
            print("chunk %r to %r generated an exception, try #%r" %(i-split,i,t))
            res=df
            res['result_score']=-1
            df_adr=shuffle(df_adr)
            t=maxtries+1
        else:
            print("chunk %r to %r generated an exception, try #%r" %(i-split,i,t))
            res=df
            res['result_score']=-0.5
            t+=1
        
        
    return 




#version monothread
#for events_subset in f.iter_dataframes(chunksize=split):
#    i+=split
#    print("Enrichissement addok/BAN: {}...".format(i))
#    liste.append(adresse_submit(events_subset))
#    # Insert here applicative logic on each partial dataframe.
#    pass    

#multithread

with concurrent.futures.ThreadPoolExecutor(max_workers=nthreads) as executor:
    enrich={executor.submit(adresse_submit,subset) for subset in f.iter_dataframes(chunksize=split,infer_with_pandas=False)}
    for s in concurrent.futures.as_completed(enrich):  
        j+=split
        try:
            liste.append(s.result())
        except Exception as exc:
            print("chunk %r to %r generated an exception: %r\n%r" %(j-split,j,exc,s))
        else:
            if ((j%verbosechunksize)==0):
                print("geocoded chunk %r to %r" %(j-verbosechunksize,j))


events=pd.concat(liste,ignore_index=True)

# Recipe outputs
out = d.Dataset("accidents_geo")
out.write_with_schema(events)
