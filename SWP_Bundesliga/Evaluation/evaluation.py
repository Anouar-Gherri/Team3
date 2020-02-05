from Algorithm import algorithm_dict
import pandas as pd

match_file = pd.read_csv('evaluation-matches.csv')

match_list = match_file[['team1', 'team2']].values.tolist()

ad = algorithm_dict.create_algorithms()
algorithm_dict.train_all(ad, 'evaluation-data.csv')

res = ['win', 'lose', 'draw']


def request_all(hst, gst):
    request_dict = dict(host=hst, guest=gst)
    prediction = []
    for al_name, al in ad.items():
        result = al.request(request_dict)
        result = [round(result[k], 3) for k in ['win', 'lose', 'draw']]
        prediction.append(result)
    return prediction


results_list = [['{} vs {}'.format(host, guest), *request_all(host, guest)] for host, guest in match_list if
                host != '1. FC Union Berlin' and guest != '1. FC Union Berlin']

df_res = pd.DataFrame(results_list, columns=['match', 'RF', 'GPM', 'GPM2', 'Poisson'])

print(df_res.head())
df_res.to_csv('results.csv', index=False)
