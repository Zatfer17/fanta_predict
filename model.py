import pandas as pd
import numpy as np
from plotter import plot

def run_model(start=15, end=21, player='ILICIC'):

    dataframes_votes = []
    dataframes_roles = []

    for year in range(start, end):
        season = str(year) + '-' + str(year + 1)
        dataframes_votes.append(pd.read_csv('datasets/votes/votes_s' + season + '.csv', index_col=0))
        dataframes_roles.append(pd.read_csv('datasets/roles/roles_s' + season + '.csv', index_col=0))

    Y = []
    X = []
    for (year, dataframe) in zip(range(start, end), dataframes_votes):
        season = str(year) + '-' + str(year + 1)
        X = np.append(X, [i + '_' + season for i in dataframe.columns])
        Y = np.append(Y, dataframe.loc[player].values)

    plot(X, Y)