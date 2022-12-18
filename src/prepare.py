from init import *

rankings = rankings.loc[:, ['rank', 'country_full',
                            'country_abrv', 'total_points', 'confederation', 'rank_date']]
rankings['rank_date'] = pd.to_datetime(rankings['rank_date'])
rankings = rankings.set_index(['rank_date'])\
    .groupby(['country_full'], group_keys=False)\
    .resample('D').first()\
    .fillna(method='ffill')\
    .reset_index()
rankings.head()


rankings_by_team = rankings.groupby(
    [rankings.rank_date.dt.year, rankings.country_full]).mean(numeric_only=True)
rankings_by_team = rankings_by_team.reset_index()


#print("10 best average World Ranks")
rankings_by_team.groupby(['country_full']).mean().sort_values(by=['rank'])['rank'][:10]


teams = ['Netherlands', 'USA', 'Argentina', 'Australia', 'France', 'Poland', 'England', 'Senegal',
         'Japan', 'Croatia', 'Brazil', 'South Korea', 'Morocco', 'Spain', 'Portugal', 'Switzerland']

world_cup_participants = rankings_by_team[rankings_by_team['country_full'].isin(
    teams)]['country_full'].unique()

#print(world_cup_participants)


# import chart_studio.plotly as py
# from plotly.offline import init_notebook_mode, iplot
# import plotly.graph_objs as go
# trace = []
# for team in world_cup_participants:
#     trace.append(go.Scatter(
#             x = rankings_by_team[rankings_by_team['country_full'] == team]['rank_date'],
#             y = rankings_by_team[rankings_by_team['country_full'] == team]['rank'],
#             mode = "lines",
#             name = team))
# layout = dict(title = 'FIFA Rank of World Cup 2018 Participants From 1993-2018',
#              xaxis = dict(title= 'Rank Date', dtick=6,),
#              yaxis = dict(title= 'Rank', dtick=10, autorange='reversed'),
#              height = 800
#              )
# fig = dict(data = trace, layout = layout)
# iplot(fig)

matches['date'] = pd.to_datetime(matches['date'])
#print(matches)
# print(matches.info())
# print(matches.head())

matches['score_diff'] = abs(matches['home_score'] - matches['away_score'])
matches[matches['score_diff'] == matches['score_diff'].max()].head()


def get_result(df):
    if df['home_score'] > df['away_score']:
        return 1
    elif df['home_score'] == df['away_score']:
        return 0.5
    else:
        return 0


matches['result'] = matches.apply(get_result, axis=1)


teams_df = pd.unique(matches[['home_team', 'away_team']].values.ravel('K'))
teams_df = pd.DataFrame({'team': teams_df})
teams_df['elo'] = 1500
