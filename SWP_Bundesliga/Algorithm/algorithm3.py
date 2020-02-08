from Algorithm import AlgorithmClass as aC
import pandas as pd
import numpy as np
from scipy.stats import poisson
import statsmodels.api as sm
import statsmodels.formula.api as smf


def library_creator(matches, **kwargs):
    df_matches = pd.DataFrame(matches)
    df_matches.columns = ['date', 'HomeTeam', 'AwayTeam', 'goals_home', 'goals_away', 'day']

    # Toss the date information
    df_matches_goals = df_matches[['HomeTeam', 'AwayTeam', 'goals_home', 'goals_away']]

    # This is basically the code from the internet blog
    goal_model_data = pd.concat([df_matches_goals[['HomeTeam', 'AwayTeam', 'goals_home']].assign(home=1)
                                .rename(columns={'HomeTeam': 'team', 'AwayTeam': 'opponent', 'goals_home': 'goals'}),
                                 df_matches_goals[['AwayTeam', 'HomeTeam', 'goals_away']].assign(home=0)
                                .rename(columns={'AwayTeam': 'team', 'HomeTeam': 'opponent', 'goals_away': 'goals'})])
    poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data,
                            family=sm.families.Poisson()).fit()

    return poisson_model


def library_request(library, match_dict, **kwargs):
    def get_avg_goals(team: str, opponent: str, home: int):
        return library.predict(pd.DataFrame(data={'team': team, 'opponent': opponent, 'home': home},
                                            index=[1])).values[0]

    home_team = match_dict['host']
    away_team = match_dict['guest']
    max_goals = 12

    home_goals_avg = get_avg_goals(home_team, away_team, 1)
    away_goals_avg = get_avg_goals(away_team, home_team, 0)

    prediction = [[poisson.pmf(i, team_avg) for i in range(0, max_goals+1)]
                  for team_avg in [home_goals_avg, away_goals_avg]]

    results_array = (np.outer(np.array(prediction[0]), np.array(prediction[1])))

    # probabilities for win, loose, draw
    predicted_outcomes = [np.sum(np.tril(results_array, -1)),
                          np.sum(np.triu(results_array, 1)),
                          np.sum(np.diag(results_array))]
    predicted_outcomes = [round(x, 4) for x in predicted_outcomes]

    return predicted_outcomes


def create():
    poisson_algorithm = aC.Algorithm('PoissonAlgorithm', library_creator, library_request, 'csv')
    return poisson_algorithm
