
import pandas as pd
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sciezka_do_pliku = os.path.join(current_dir, "..", "files", "Mens-Volleyball-PlusLiga-2008-2023.csv")

pd.set_option("display.max_columns", None)

data = pd.read_csv(sciezka_do_pliku)

print(data[:10])

print(data["Team_1"].unique())
print(len(data["Team_1"].unique()))

teams_names = {
    'PGE Skra Bełchatów' : 0.,
    'ZAKSA Kędzierzyn-Koźle' : 0.,
    'Asseco Resovia' : 0.,
    'Jastrzębski Węgiel' : 0.,
    'Projekt Warszawa' : 0.,
    'AZS Olsztyn' : 0.,
    'Trefl Gdańsk' : 0.,
    'Chemik Bydgoszcz' : 0.,
    'Czarni Radom' : 0.,
    'AZS Częstochowa' : 0.,
    'Społem Kielce' : 0.,
    'Cuprum Lubin' : 0.,
    'GKS Katowice' : 0.,
    'MKS Będzin' : 0.,
    'BBTS Bielsko-Biała' : 0.,
    'Warta Zawiercie' : 0.,
    'Stal Nysa'  : 0.,
    'Ślepsk Malow Suwałki'  : 0.,
    'Stocznia Szczecin' : 0.,
    'LUK  Lublin' : 0.,
    'Pamapol Wielton Wieluń'  : 0.,
    'Jadar Radom'  : 0.,
    'Barkom Każany Lwów' : 0.,
}

# x: float = 1
# for item, value in teams_names.items():
#     teams_names[item] = round(x, 2)
#     x -= 0.0454
# for item, value in teams_names.items():
#     print(item, value)

def sum_points():
    """

    :return:
    """
    best_teams = data["Team_1"].drop_duplicates()
    best_teams = best_teams.to_frame()
    best_teams["sum"] = data.groupby("Team_1")["T1_Sum"].transform('sum')
    best_teams = best_teams.sort_values("sum", ascending=False)
    print(best_teams)

    x: float = 1
    for item, value in teams_names.items():
        teams_names[item] = x
        x -= 0.0454
    for item, value in teams_names.items():
        print(item, value)

def prepare_data():
    data_copy = data.copy()

    data_copy = data_copy.drop(columns=["Date"])

    for item, value in teams_names.items():
        data_copy["Team_1"] = np.where(data_copy["Team_1"] == item, value, data_copy["Team_1"])
        data_copy["Team_2"] = np.where(data_copy["Team_2"] == item, value, data_copy["Team_2"])
    print(data_copy[:10])

    return data_copy

sum_points()
prepare_data()