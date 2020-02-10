import random
from timeit import default_timer as timer
import numpy as np
from Algorithm import algorithm_dict
import pandas as pd
import matplotlib.pyplot as plt

ad = algorithm_dict.create_algorithms()

match_file = pd.read_csv('evaluation-matches.csv')
all_matches = pd.read_csv('all_matches.csv')
all_teams = pd.read_csv('all_teams.csv')
all_outcomes = [[int(g1 > g2), int(g1 < g2), int(g1 == g2)] for [g1, g2] in
                match_file[['goal1', 'goal2']].values.tolist()]


def filter_matches(year):
    scope = all_matches[['date', 'play_day']].values.tolist()
    valid_matches = [int(dt[:4]) > year or int(dt[:4]) == year and day < 17 for dt, day in scope]
    return all_matches[valid_matches]


def filter_teams(year):
    return set([team for team, date in all_teams.values.tolist() if date >= year])


def flatten(li):
    return [item for sublist in li for item in sublist]


def to_interval(li):
    return [prediction[0] - prediction[1] for prediction in li]


def all_corr(v1, v2):
    x, y = flatten(v1), flatten(v2)
    x2, y2 = to_interval(v1), to_interval(v2)
    return [corr(x, y), corr(x2, y2)]


def corr(x, y):
    return round(np.corrcoef(x, y)[0, 1], 3)


def random_results(v1):
    res = [1]
    prediction = [0, 0, 0]
    for i in range(len(v1)):
        prediction[random.randint(0, 2)] = 1
        res.append(prediction)
        prediction = [0, 0, 0]
    return res[1:]


def run_prediction(year):
    algorithm_dict.train_all(ad, filter_matches(year), data_type='frame')
    teams = filter_teams(year)
    valid_matches = [set(match).issubset(teams) for match in match_file[['team1', 'team2']].values.tolist()]
    matches = match_file[valid_matches]

    def get_teams():
        return matches[['team1', 'team2']].values.tolist()

    def get_results():
        results = matches[['goal1', 'goal2']].values.tolist()
        return [[int(g1 > g2), int(g1 < g2), int(g1 == g2)] for [g1, g2] in results]

    def request_all(hst, gst):
        request_dict = dict(host=hst, guest=gst)
        prediction = []
        for al_name, al in ad.items():
            result = al.request(request_dict)
            result = [round(result[k], 3) for k in ['win', 'lose', 'draw']]
            prediction.append(result)
        return prediction

    def predict_results():
        return [['{} vs {}'.format(host, guest), *request_all(host, guest)] for host, guest in get_teams()]

    def df_predictions():
        results_list = [x + [y] for x, y in zip(predict_results(), get_results())]
        return pd.DataFrame(results_list, columns=['match', 'Rlt Freq', 'Goals/M', 'Goals/M 2', 'Poisson', 'Actual'])

    df_res = df_predictions()
    outcome = df_res['Actual']

    return [[algorithm, year] + all_corr(df_res[algorithm].values.tolist(), outcome)
            for algorithm in ['Rlt Freq', 'Goals/M', 'Goals/M 2', 'Poisson']]


def predict_all():
    years = range(2008, 2019)
    data = []
    for year in years:
        data.extend(run_prediction(year))
    df_all = pd.DataFrame(data, columns=['algorithm', 'Data from', 'Event', 'Interval'])
    return df_all


def print_prediction():
    years = range(2008, 2019)
    print('Correlations:')
    print('Knowing: ' + str(all_corr(all_outcomes, all_outcomes)[0]))
    print('Random:  ' + str(all_corr(random_results(all_outcomes), all_outcomes)[0]))
    print('         Event,  float')
    for year in years:
        print(year)
        for res in run_prediction(year):
            print(res[0] + ":" + " " * (9 - len(res[0])) + ',   '.join(map(lambda x: str(x), res[2:])))


# print_prediction() case plotting doesnt work

def plot_prediction():
    df_all_years = predict_all()
    for scope in ['Event', 'Interval']:
        title = scope + ' Comparison'
        scope = df_all_years[['algorithm', 'Data from', scope]].pivot(
            index='Data from', columns='algorithm', values=scope)
        scope.plot(title=title, ylim=(-0.05, 0.4))
    plt.show()


# Explanation:
# 'Plain' is the ability to predict a single outcome (win, lose, or draw)
# 'Interval' predicts only who is more likely to win
# The y-scale is the correlation between the prediction and the actual outcome
# Knowing means correlation of 1, random of 0, 'lying' of -1


def execution_time():
    print()
    algorithm_dict.train_all(ad, filter_matches(2011), data_type='frame')
    teams = filter_teams(2011)
    valid_matches = [set(match).issubset(teams) for match in match_file[['team1', 'team2']].values.tolist()]
    matches = match_file[valid_matches][['team1', 'team2']].values.tolist()
    matches *= 4
    match_list = [dict(host=t1, guest=t2) for [t1, t2] in matches[:500]]
    print('Requesting 500 matches...')
    for alg in ad.values():
        start = timer()
        for match in match_list:
            alg.request(match)
        end = timer()
        print(alg.name + ":   " + " " * (26 - len(alg.name)) + str(round(end - start, 4)) + ' seconds')


execution_time()
plot_prediction()

