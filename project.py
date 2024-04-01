import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

# load the raw data
df=pd.read_csv('data/Air_Quality.csv')
print(df.head())
