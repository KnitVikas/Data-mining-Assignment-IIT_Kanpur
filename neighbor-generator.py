import pandas as pd
import os
import numpy as np
import json

# os.chdir("/content/drive/My Drive/assignment_shubham")


def get_neighbour_time_csv(
    path_cases_time_file, path_edge_graph_file, path_neighbour_district_modified
):
    with open(path_neighbour_district_modified, "r") as json_file:
        neighbour_district = json.loads(json_file.read())
    id2dist = {}
    for k, v in neighbour_district.items():
        id2dist[k.split("/")[1]] = k.split("/")[0]

    edge_graph = pd.read_csv(path_edge_graph_file)
    cases_week = pd.read_csv(path_cases_time_file)
    # print(cases_week.head(),edge_graph.head())
    final_data = []
    for col in edge_graph.columns:
        for id in range(1, len(set(cases_week.timeid))+1):

            cases = []
            for neighbour in edge_graph[col]:
                if id in cases_week["timeid"] and int(neighbour) != 0:
                    case = cases_week[
                        (
                            cases_week["districtid"].str.lower()
                            == id2dist[str(neighbour)].lower()
                        )
                        & (cases_week["timeid"] == np.int64(id))
                    ].cases.to_list()

                    if case:
                        cases.append(case[0])
                        print("case found")
                    else:
                        print("no case found")
                else:
                    pass
            # if np.array(cases).std() !=np.nan and np.array(cases).mean()!=np.nan and int(neighbour)!=0:
            final_data.append(
                (
                    id2dist[str(col)].lower(),
                    id,
                    round(np.array(cases).mean(), 2),
                    round(np.array(cases).std(), 2),
                )
            )
    week_data = [i for i in final_data if i[2] != final_data[0][2]]
    week_data.sort(key=lambda key: key[0])

    d = pd.DataFrame(
        week_data, columns=["districtid", "timeid", "neighbormean", "neighborstdev"]
    )
    d = d.sort_values("districtid")

    d["districtid"] = d["districtid"].apply(lambda x: x.lower())
    time = os.path.basename(path_cases_time_file).split("-")[-1].split(".")[0]
    d.to_csv("neighbor-" + time + ".csv", index=False)


edge_graph_file = "edge-graph.csv"
cases_time_file = "cases-week.csv"
neighbour_district_modified = "neighbor-districts-modified.json"
# get_neighbour_time_csv(cases_time_file, edge_graph_file, neighbour_district_modified)
get_neighbour_time_csv(
    "cases-overall.csv", edge_graph_file, neighbour_district_modified
)
get_neighbour_time_csv("cases-month.csv", edge_graph_file, neighbour_district_modified)
