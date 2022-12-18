from prepare import *
from elo import *
world_cup = pd.read_csv('../data/qualified.csv')
world_cup_rankings = rankings.loc[(rankings['rank_date'] == rankings['rank_date'].max()) &
                                  rankings['country_full'].isin(teams)]
world_cup_rankings = world_cup_rankings.set_index(['country_full'])
print(world_cup_rankings)
world_cup_elo = teams_df.loc[teams_df.index.isin(
    teams)].sort_values(by=['team'])
print(world_cup_elo)
world_cup_rankings['elo_ratings'] = world_cup_elo.loc[:, ['elo']]

# print(teams)

matches = matches.merge(rankings,
                        left_on=['date', 'home_team'],
                        right_on=['rank_date', 'country_full'])
matches = matches.merge(rankings,
                        left_on=['date', 'away_team'],
                        right_on=['rank_date', 'country_full'],
                        suffixes=('_home', '_away'))


matches['rank_difference'] = matches['rank_home'] - matches['rank_away']
matches['average_rank'] = (matches['rank_home'] + matches['rank_away'])/2
matches['point_difference'] = matches['total_points_home'] - \
    matches['total_points_away']
matches['score_difference'] = matches['home_score'] - matches['away_score']
matches['is_won'] = matches['score_difference'] > 0  # take draw as lost
matches['is_stake'] = matches['tournament'] != 'Friendly'
matches['elo_difference'] = matches['home_elo'] - matches['away_elo']

#max_rest = 30

matches['wc_participant'] = matches['home_team'] * \
    matches['home_team'].isin(world_cup.index.tolist())
matches['wc_participant'] = matches['wc_participant'].replace({'': 'Other'})
matches = matches.join(pd.get_dummies(matches['wc_participant']))
