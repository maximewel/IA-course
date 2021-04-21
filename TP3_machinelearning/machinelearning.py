import pandas as pd
import matplotlib.pyplot as plt
from tsfresh.feature_extraction import extract_features, ComprehensiveFCParameters, MinimalFCParameters




timeseries = pd.read_csv("C:\\DEV\\IA\\TP3_machinelearning\\dataset_SOON_Electric_Engine_Simulator\\2021-03-26\\gray_75_balanced.csv", header=None, names=["a1", "a2", "a3"])

#insert the ID
timeseries.insert(0,"id",1)

print(f"timeserie : \n{timeseries}")

"""
settings = MinimalFCParameters()
extract_features(timeseries, default_fc_parameters=settings, column_id="id")

print(extracted_features)"""

#Hand-made extraction

#means
timeseries["rolling_mean1"] = timeseries["a1"].rolling(window=5).mean()
timeseries["rolling_mean2"] = timeseries["a2"].rolling(window=5).mean()
timeseries["rolling_mean3"] = timeseries["a3"].rolling(window=5).mean()

#std

print(timeseries)