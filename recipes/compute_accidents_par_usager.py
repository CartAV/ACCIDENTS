# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Recipe inputs
ds_in = dataiku.Dataset("accidents_par_usager_brut")
events = ds_in.get_dataframe()




# Recipe outputs
ds_out = dataiku.Dataset("accidents_par_usager")
ds_out.write_with_schema(events)
