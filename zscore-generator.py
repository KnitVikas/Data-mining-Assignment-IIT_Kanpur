import csv
import pandas as pd
import numpy as np


def get_zscore(case_time_file, neighbor_time_file, state_time_file):
    time = os.path.basename(case_time_file).split("-")[-1].split(".")[0]
    file_name = "zscore-" + time + ".csv"

    with open(file_name, "w", newline="") as csvfile:
        fieldnames = ["district-id", "time-id", "neighborhood-zscore", "state-zscore"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        df = pd.read_csv(case_time_file).dropna()
        ans = pd.read_csv(neighbor_time_file).dropna()
        temp = pd.read_csv(state_time_file).dropna()
        merged = pd.merge(df, ans, how="inner", on=["districtid", "timeid"])
        merged = pd.merge(merged, temp, how="inner", on=["districtid", "timeid"])
        merged = merged.dropna()

        for i in range(0, len(merged)):

            district_id = merged["districtid"][i]
            time_id = merged["timeid"][i]
            cases = merged["cases"][i]

            neighbour_mean = merged["neighbormean"][i]
            neighbour_std = merged["neighborstdev"][i]

            state_mean = merged["statemean"][i]
            state_std = merged["statestdev"][i]

            z_score_neighbour = 0
            if neighbour_std != 0:
                z_score_neighbour = round(((cases - neighbour_mean) / neighbour_std), 2)
            z_score_state = 0
            if state_std != 0:
                z_score_state = round(((cases - state_mean) / state_std), 2)
            writer.writerow(
                {
                    "district-id": district_id,
                    "time-id": time_id,
                    "neighborhood-zscore": z_score_neighbour,
                    "state-zscore": z_score_state,
                }
            )


get_zscore("cases-month.csv", "neighbor-month.csv", "state-month.csv")
get_zscore("cases-week.csv", "neighbor-week.csv", "state-week.csv")
get_zscore("cases-overall.csv", "neighbor-overall.csv", "state-overall.csv")
