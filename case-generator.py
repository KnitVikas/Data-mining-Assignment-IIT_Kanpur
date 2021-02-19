import json
import os
import requests
import pandas as pd


def get_preprocess_data():
    contents = requests.get("https://api.covid19india.org/v4/data-all.json").json()
    districts = []
    T = 0
    D = 0
    C = 0
    case_count = 0
    monthly_cases = []
    for date in list(contents.keys())[48:]:
        for state in list(contents[date].keys()):
            if "districts" in list(contents[date][state].keys()):
                for district in list(contents[date][state]["districts"].keys()):

                    if "total" in list(
                        contents[date][state]["districts"][district].keys()
                    ):

                        if "confirmed" in list(
                            contents[date][state]["districts"][district]["total"].keys()
                        ):
                            cases = contents[date][state]["districts"][district][
                                "total"
                            ]["confirmed"]
                            # print(f"{case_count} cases found")
                            if district != "Unknown":
                                districts.append((date, state, district, cases))
                                case_count += case_count
                        else:
                            print("confirmed cases not found")

                            C += 1

                    else:
                        print("total not present in list")
                        T += 1
            else:
                print("district is not present")
                D += 1
    return districts


def get_all_Ids():
    districts = get_preprocess_data()
    all_in_one = []
    id0 = []
    id1 = []
    id2 = []
    id3 = []
    id4 = []
    id5 = []
    for d, s, dist, c in districts:
        if d.split("-")[1] == "03" and 14 < int(d.split("-")[2]) <= 31:
            id0.append((d, s, dist, c))
        if d.split("-")[1] == "04" and 1 <= int(d.split("-")[2]) <= 15:
            id0.append((d, s, dist, c))
        if d.split("-")[1] == "04" and 15 < int(d.split("-")[2]) <= 31:
            id1.append((d, s, dist, c))
        if d.split("-")[1] == "05" and 1 <= int(d.split("-")[2]) <= 15:
            id1.append((d, s, dist, c))
        if d.split("-")[1] == "05" and 15 < int(d.split("-")[2]) <= 31:
            id2.append((d, s, dist, c))
        if d.split("-")[1] == "06" and 1 <= int(d.split("-")[2]) <= 15:
            id2.append((d, s, dist, c))
        if d.split("-")[1] == "06" and 15 < int(d.split("-")[2]) <= 31:
            id3.append((d, s, dist, c))
        if d.split("-")[1] == "07" and 1 <= int(d.split("-")[2]) <= 15:
            id3.append((d, s, dist, c))
        if d.split("-")[1] == "07" and 15 < int(d.split("-")[2]) <= 31:
            id4.append((d, s, dist, c))
        if d.split("-")[1] == "08" and 1 <= int(d.split("-")[2]) <= 15:
            id4.append((d, s, dist, c))
        if d.split("-")[1] == "08" and 15 < int(d.split("-")[2]) <= 31:
            id5.append((d, s, dist, c))
        if d.split("-")[1] == "09" and 1 <= int(d.split("-")[2]) <= 5:
            id5.append((d, s, dist, c))
        if dist != "Unknown":
            all_in_one.append((d, s, dist, c))

    total_ids = []
    count = 0
    for id in [id0, id1, id2, id3, id4, id5]:
        d = {district: 0 for date, state, district, cases in id}
        # if id:
        for date, state, district, cases in id:
            d[district] += cases
        Output = list(map(tuple, d.items()))
        id_sort = []
        for i, j in Output:
            id_sort.append((i, j, count))
        id_sort.sort(key=lambda x: x[0])
        total_ids.append(id_sort)
        count = count + 1
    return total_ids, all_in_one


def get_overall_cases_dataframe():
    _, complete_data = get_all_Ids()
    all = []
    for i in _:
        all.extend(i)
    d = {district: 0 for district, cases, id in all}
    for district, cases, id in all:
        d[district] += cases
    dataframe = pd.DataFrame(
        list(
            zip(
                list(d.keys()),
                list(d.values()),
                [1 for i in range(len(list(d.values())))],
            )
        ),
        columns=["districtid", "cases", "timeid"],
    )
    dataframe = dataframe.sort_values("districtid")
    dataframe["districtid"] = dataframe["districtid"].apply(lambda x: x.lower())
    dataframe.to_csv("cases-overall.csv", index=False)


def get_weekly_cases_dataframe():
    _, complete_data = get_all_Ids()
    df = pd.DataFrame(complete_data, columns=["Date", "State", "Districts", "Cases"])
    df["Date"] = pd.to_datetime(df["Date"])
    weeks = [g for n, g in df.groupby(pd.Grouper(key="Date", freq="W"))]

    i = 0
    cases = (
        weeks[i].groupby("Districts").Cases.apply(lambda g: sum(g))
    )  # same as .groupby.apply(lambda g: g.nlargest(2))
    cases = list(cases)
    districts = list(set(weeks[i]["Districts"]))
    id = [i for j in range(len(districts))]
    dataframe = pd.DataFrame(
        list(zip(districts, cases, id)), columns=["districtid", "cases", "timeid"]
    )
    dataframe = dataframe.sort_values("districtid")

    for i in range(1, len(weeks)):
        cases = (
            weeks[i].groupby("Districts").Cases.apply(lambda g: sum(g))
        )  # same as .groupby.apply(lambda g: g.nlargest(2))
        cases = list(cases)
        districts = list(set(weeks[i]["Districts"]))
        id = [i for j in range(len(districts) + 1)]
        dataframe_ = pd.DataFrame(
            list(zip(districts, cases, id)), columns=["districtid", "cases", "timeid"]
        )
        dataframe_ = dataframe_.sort_values("districtid")
        dataframe = pd.concat([dataframe, dataframe_], axis=0)
    dataframe["districtid"] = dataframe["districtid"].apply(lambda x: x.lower())
    dataframe = dataframe.dropna()
    dataframe.to_csv("cases-week.csv", index=False)


def get_monthly_cases_dataFrame():
    df = pd.DataFrame(columns=["districtid", "cases", "timeid"])
    monthly_data, complete_data = get_all_Ids()
    i0, i1, i2, i3, i4, i5 = monthly_data

    for id in [i0, i1, i2, i3, i4, i5]:
        df1 = pd.DataFrame(id, columns=["districtid", "cases", "timeid"])
        df = pd.concat([df, df1], axis=0)
    df = df.sort_values("districtid")
    df["districtid"] = df["districtid"].apply(lambda x: x.lower())
    df.to_csv("cases-month.csv", index=False)
    # print(df.timeid.nunique())


get_monthly_cases_dataFrame()
get_weekly_cases_dataframe()
get_overall_cases_dataframe()