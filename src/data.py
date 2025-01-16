import pandas as pd
import numpy as np
import os


# x: float = 1
# for item, value in teams_names.items():
#     teams_names[item] = round(x, 2)
#     x -= 0.0454
# for item, value in teams_names.items():
#     print(item, value)

# def sum_points():
#     """
#
#     :return:
#     """
#     best_teams = data["Team_1"].drop_duplicates()
#     best_teams = best_teams.to_frame()
#     best_teams["sum"] = data.groupby("Team_1")["T1_Sum"].transform('sum')
#     best_teams = best_teams.sort_values("sum", ascending=False)
#     print(best_teams)



def prepare_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sciezka_do_pliku = os.path.join(current_dir, "..", "files", "Mens-Volleyball-PlusLiga-2008-2023.csv")

    pd.set_option("display.max_columns", None)

    data = pd.read_csv(sciezka_do_pliku)

    teams_names = {
        'PGE Skra Bełchatów': 0.,
        'ZAKSA Kędzierzyn-Koźle': 0.,
        'Asseco Resovia': 0.,
        'Jastrzębski Węgiel': 0.,
        'Projekt Warszawa': 0.,
        'AZS Olsztyn': 0.,
        'Trefl Gdańsk': 0.,
        'Chemik Bydgoszcz': 0.,
        'Czarni Radom': 0.,
        'AZS Częstochowa': 0.,
        'Społem Kielce': 0.,
        'Cuprum Lubin': 0.,
        'GKS Katowice': 0.,
        'MKS Będzin': 0.,
        'BBTS Bielsko-Biała': 0.,
        'Warta Zawiercie': 0.,
        'Stal Nysa': 0.,
        'Ślepsk Malow Suwałki': 0.,
        'Stocznia Szczecin': 0.,
        'LUK  Lublin': 0.,
        'Pamapol Wielton Wieluń': 0.,
        'Jadar Radom': 0.,
        'Barkom Każany Lwów': 0.,
    }

    x: float = 0.99
    for item, value in teams_names.items():
        teams_names[item] = x
        x -= 0.0449

    data_copy = data.copy()

    winner = data_copy["Winner"]
    data_copy = data_copy.drop(columns=["Date", "Winner"])
    for item, value in teams_names.items():
        data_copy["Team_1"] = np.where(data_copy["Team_1"] == item, value, data_copy["Team_1"])
        data_copy["Team_2"] = np.where(data_copy["Team_2"] == item, value, data_copy["Team_2"])

    percent_column = ["T1_Srv_Err", "T1_Srv_Eff", "T1_Rec_Pos", "T1_Rec_Perf", "T1_Att_Sum", "T1_Att_Kill_Perc", "T1_Att_Eff", "T1_Blk_As",
                      "T2_Srv_Eff", "T2_Srv_Err", "T2_Rec_Pos", "T2_Rec_Perf", "T2_Att_Sum" ,"T2_Att_Kill_Perc", "T2_Att_Eff", "T2_Blk_As"]

    #print(data_copy.info())
    for column in percent_column:
        data_copy[column] = data_copy[column].astype(str).str.replace(",", ".").str.replace("%", "").astype(float)
    #print(data_copy.info())
    for (column, columnData) in data_copy.items():
        if column != "Team_1" or column != "Team_2":
            data_copy[column] = data_copy[column].apply(lambda x: float(x)/10 if float(x) < 9.99
            else float(x)/ 100 if float(x) < 99.99 else float(x)/1000)
    return data_copy, winner

prepare_data()