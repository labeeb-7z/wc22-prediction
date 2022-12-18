from train import *

gb_model = GradientBoostingClassifier()
gb_model.fit(X_train, y_train)
qda_model = QuadraticDiscriminantAnalysis()
qda_model.fit(X_train, y_train)
xgb_model = XGBClassifier()
xgb_model.fit(X_train, y_train)


pairing = [0, 3, 4, 7, 8, 11, 12, 15, 1, 2, 5, 6, 9, 10, 13, 14]

world_cup = world_cup.sort_values(
    by=['Group', ], ascending=False).reset_index()
next_round_wc = world_cup.groupby('Group').nth([0, 1])  # select the top 2
next_round_wc = next_round_wc.reset_index()
print("Qualified Teams\n")
print(next_round_wc.loc[:, ['Group', 'Team', ]])
print("\n")
next_round_wc = next_round_wc.loc[pairing]
next_round_wc = next_round_wc.set_index('Team')

finals = ['Round_of_16', 'Quarterfinal', 'Semifinal', 'Final']

labels = list()
odds = list()


for f in finals:
    print(f)
    iterations = int(len(next_round_wc) / 2)
    winners = []

    for i in range(iterations):
        home = next_round_wc.index[i*2]
        away = next_round_wc.index[i*2+1]
        print(f"{home} vs. {away}: ", end='')
        row = pd.DataFrame(
            np.array([[np.nan, np.nan, np.nan, np.nan, True]]), columns=X_test.columns)
        home_rank = world_cup_rankings.loc[home, 'rank']
        home_points = world_cup_rankings.loc[home, 'total_points']
        home_elo = world_cup_rankings.loc[home, 'elo_ratings']
        opp_rank = world_cup_rankings.loc[away, 'rank']
        opp_points = world_cup_rankings.loc[away, 'total_points']
        opp_elo = world_cup_rankings.loc[away, 'elo_ratings']
        row['average_rank'] = (home_rank + opp_rank) / 2
        row['rank_difference'] = home_rank - opp_rank
        row['point_difference'] = home_points - opp_points
        row['elo_difference'] = home_elo - opp_elo

        elo_prob = expected(home_elo, opp_elo)
        home_win_prob = qda_model.predict_proba(
            row)[:, 1][0] * 0.5 + xgb_model.predict_proba(row)[:, 1][0] * 0.5
        if home_win_prob <= 0.5:
            print(f"{away} wins with probability {1-home_win_prob:.2f}")
            winners.append(away)
        else:
            print(f"{home} wins with probability {home_win_prob:.2f}")
            winners.append(home)

        labels.append(
            f"{world_cup_rankings.loc[home,'country_abrv']}({1/home_win_prob:.2f}) vs. {world_cup_rankings.loc[away,'country_abrv']}({1/(1-home_win_prob):.2f})")
        odds.append([home_win_prob, 1-home_win_prob])

    next_round_wc = next_round_wc.loc[winners]
    print("\n")
