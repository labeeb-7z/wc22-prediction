import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


rankings = pd.read_csv('../data/fifa_ranking.csv')


matches = pd.read_csv('../data/resultsIM.csv')
wc = pd.read_csv('../data/wc2022.csv')
rankings.replace("Korea Republic","South Korea",inplace=True)
wc.replace("Korea Republic","South Korea",inplace=True)

matches.replace("United States","USA",inplace=True)

print('South Korea' in wc['home_team'].values)


# print(matches)
# print(rankings)
# print(rankings.info())
# print(matches.info())
