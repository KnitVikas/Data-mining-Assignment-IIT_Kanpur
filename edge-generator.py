import os
import json
import pandas as pd


def get_edge_graph(path_neighbour_districts_modified_json):
    neighbour_dict = {}
    with open(path_neighbour_districts_modified_json, "r") as json_file:
        modified_jsn = json.loads(json_file.read())
    for k, v in modified_jsn.items():
        value_list = []
        for val in modified_jsn[k]:
            d = val.split("/")[1]
            value_list.append(d)
        if len(value_list) != 10:
            value_list.extend([0] * (10 - len(value_list)))
            neighbour_dict[k.split("/")[1]] = value_list
    df = pd.DataFrame(neighbour_dict)
    df.to_csv("edge-graph.csv", index=False)


get_edge_graph("neighbor-districts-modified.json")
