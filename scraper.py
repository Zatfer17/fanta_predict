import requests
import ast
from tqdm import tqdm
import numpy as np
import pandas as pd

url = 'https://www.fantacalcio.it/api/live/{team}?g={game}&i={year}'
bonus_types = {
    '': ['nessuno', 0],
    '1': ['ammonizione', -0.5],
    '2': ['espulsione', -1],
    '3': ['gol', 3],
    '4': ['gol subito', -1],
    '5': ['assist', 1],
    '6': ['assist fermo', 1],
    '7': ['rigore parato', 3],
    '8': ['rigore sbagliato', -3],
    '9': ['rigore segnato', 3],
    '10': ['autorete', -2],
    '11': ['gol vittoria', 0],
    '12': ['gol pareggio', 0],
    '14': ['sostituito', 0],
    '15': ['subentrato', 0],
    '16': ['gol annullato var', 0],
    '17': ['assist annullato var', 0],
    '20': ['low quality assist', 1],
    '21': ['medium quality assist', 1],
    '22': ['high quality assist', 1],
    '23': ['assist rimessa dal fondo', 1],
    '24': ['assist angolo', 1],
    '25': ['assist punizione', 1]
}

def scrape(start=15, end=21, games=38, last_year=21, last_game=26, teams=50):

    data = {}
    roles = {}
    for s in range(start, end):
        data[str(s) + '-' + str(s + 1)] = {}
        roles[str(s) + '-' + str(s + 1)] = {}
    columns = ['g' + str(g) for g in range(games)]

    for year in tqdm(range(start, end)):
        season = str(year) + '-' + str(year + 1)
        for game in range(games if year < last_year else last_game):
            for team in range(teams):
                r = requests.get(url.replace('{team}', str(team+1)).replace('{game}', str(game+1)).replace('{year}', str(year-5)))
                content = r.content.decode('UTF-8')
                if content != '[]':
                    content = content.replace('[{', '').replace('}]', '')
                    players = content.split('},{')
                    for player in players:
                        temp = ast.literal_eval('{' + player + '}')

                        name = temp['nome']
                        role = temp['ruolo']
                        if temp['voto'] == 55.0:
                            vote = 0.0
                            bonus = 0.0
                        else:
                            vote = temp['voto']
                            events = temp['evento'].split(',')

                            bonus = 0

                            for event in events:
                                bonus += bonus_types[event][1]
                            if role == 'P' and '4' not in events:
                                bonus += 1

                        try:
                            data[season][name][game - 1] = vote + bonus
                        except KeyError:
                            data[season][name] = np.zeros(len(columns))
                            data[season][name][game - 1] = vote + bonus

                        if name not in roles[season]:
                            roles[season][name] = role

        season_votes = pd.DataFrame.from_dict(data[season], orient='index', columns=columns)
        season_roles = pd.DataFrame.from_dict(roles[season], orient='index', columns=['role'])
        season_votes.to_csv('datasets/votes/votes_s' + season + '.csv')
        season_roles.to_csv('datasets/roles/roles_s' + season + '.csv')

