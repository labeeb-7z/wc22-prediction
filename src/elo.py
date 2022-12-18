from prepare import *
def expected(A, B):
    return 1 / (1 + 10 ** ((B - A) / 400))


def elo(old, exp, score, k=30):

    return old + k * (score - exp)


teams_df.set_index('team', inplace=True)
elo_ratings_home, elo_ratings_away = [], []
for index, row in matches.iterrows():
    elo_home = teams_df['elo'].loc[row['home_team']]
    elo_away = teams_df['elo'].loc[row['away_team']]

    new_elo_home = elo(elo_home, expected(elo_home, elo_away), row['result'])
    new_elo_away = elo(elo_away, expected(
        elo_away, elo_home), (row['result']-1)*-1)

    teams_df['elo'].loc[row['home_team']] = new_elo_home
    teams_df['elo'].loc[row['away_team']] = new_elo_away

    elo_ratings_home.append(new_elo_home)
    elo_ratings_away.append(new_elo_away)

matches['home_elo'] = elo_ratings_home
matches['away_elo'] = elo_ratings_away


# print("Top 10 Teams Based on Elo Rating")
# print(teams_df.sort_values(by=['elo'], ascending=False)[:10])
