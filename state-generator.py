import json
import numpy as np
import requests
import pandas as pd
import os


def get_preprocess_data():
  contents = requests.get("https://api.covid19india.org/v4/data-all.json").json()
  # with open('all_data.json', 'w') as json_file:
  #     json.dump(response, json_file)

  # with open("all_data.json", 'r') as j:
      # contents = json.loads(j.read())
    # contents = json.loads(j.read())
  districts = []
  T = 0
  D = 0
  C = 0
  case_count=0
  monthly_cases = []
  for date in list(contents.keys())[48:]:
    for state in list(contents[date].keys()):
      if "districts" in list(contents[date][state].keys()):
          for district in list(contents[date][state]["districts"].keys()):
    
              if "total" in list(contents[date][state]["districts"][district].keys()):

                if "confirmed" in list(contents[date][state]["districts"][district]["total"].keys()) :             
                  cases = contents[date][state]["districts"][district]["total"]["confirmed"] 
                  # print(f"{case_count} cases found")
                  districts.append((date, state,district,cases))
                  case_count+=case_count
                else:
                  print("confirmed cases not found")
                  
                  C+=1

              else:
                print("total not present in list")
                T+=1
      else:
        print("district is not present")
        D+=1  
  return districts

def get_state_time_csv(path_cases_time_file):
  all_dataset = get_preprocess_data()
  week_cases = pd.read_csv(path_cases_time_file)
  final_=[]
  for state in list(set([i[1] for i in all_dataset])):

    for id in range(1,len(set(week_cases["timeid"]))+1):
      case=[]
      for district in set([i[2] for i in all_dataset if i[1]==state]):
        if id in week_cases["timeid"]:
          week_case = week_cases[(week_cases["districtid"].str.lower() == district.lower()) & (week_cases["timeid"]==id)].cases.to_list()  
          if week_case:
            case.append((district,week_case[0],id))
            # print(district,week_case[0],id)
      
      
      
      for j in range(len(case)):
        m = np.array([i[1] for i in case if i!=case[j]]).mean()
        s = np.array([i[1] for i in case if i!=case[j]]).std() 
        d = case[j][0]
        final_.append((d,id,round(m,2),round(s,2))) 
  final_.sort(key = lambda key: key[0])
  d = pd.DataFrame(final_, columns =["districtid", "timeid", "statemean","statestdev"])
  d["districtid"] =d["districtid"].apply(lambda x : x.lower()) 
  time = os.path.basename(path_cases_time_file).split("-")[-1].split(".")[0]
  d.to_csv("state-"+time+".csv",index=False)
  
get_state_time_csv("cases-week.csv")
get_state_time_csv("cases-month.csv")
get_state_time_csv("cases-overall.csv")

