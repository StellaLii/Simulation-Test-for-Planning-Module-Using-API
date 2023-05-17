#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
from pandas import DataFrame
import pandasql as ps
import plotly.graph_objects as go
import plotly.express as px

import requests


headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }

data = '{"batch_name": "planning-cicd-single-frame-test-2-2-0-v8mz5"}'
# planning-cicd-single-frame-test-2-1-1-6xlj7 最新

response = requests.post('http://analysis-service.simulation-platform-prod.simulation.deeproute.ai/api/v2/get_scenario_results', headers=headers, data=data)
#new_response = response_data["scenarioResults"]

response_data = response.json()
# print(response_data)
# new_response = response_data["scenarioResults"][0]['metricResults'][0]['annotations']['scenario_result']
# new_response1 = response_data["scenarioResults"][0]['scenarioMetadata']['scenarioId']

# # df = pd.DataFrame(columns=['scenarioId', 'scenarioResults', 'jiraId', 'issueTypes', 'sceneTypes', 'stable', 'gradingReady'])
# # print(df)

# scenarioResults = []
# for i in response_data["scenarioResults"]:
#     if i['metricResults'][0]['metricName'] == 'job_info':
#         scenarioResults.append(i['metricResults'][0]['annotations']['scenario_result'])
# scenarioId = []
# for i in response_data["scenarioResults"]:
#     scenarioId.append(i['scenarioMetadata']['scenarioId'])
# # jiraId = []
# # for i in response_data["scenarioResults"]:
# #     jiraId.append(i['scenarioMetadata']['jiraId'])
    
# issueTypes = []
# for i in response_data["scenarioResults"]:
#     issueTypes.append(i['scenarioMetadata']['issueTypes'])

# sceneTypes = []
# for i in response_data["scenarioResults"]:
#     sceneTypes.append(i['scenarioMetadata']['sceneTypes'])
    
# stable = []
# for i in response_data["scenarioResults"]:
#     stable.append(i['scenarioMetadata']['stable'])
    
# gradingReady = []
# for i in response_data["scenarioResults"]:
#     gradingReady.append(i['scenarioMetadata']['gradingReady'])
#     print(gradingReady)

# df = pd.DataFrame([scenarioId, scenarioResults, issueTypes, sceneTypes]).T
# df.columns = ["scenarioId", "scenarioResults", "issueTypes", "sceneTypes"]
# # print(df.head())
# df['scenarioId']= df['scenarioId'].astype('str')
# df['scenarioResults']= df['scenarioResults'].astype('str')
# df['issueTypes']= df['issueTypes'].astype('str')
# df['sceneTypes']= df['sceneTypes'].astype('str')
# # print(df.dtypes)


# group = df.groupby('scenarioResults')

# sql = """
# SELECT COUNT(scenarioResults) AS scenarioResults
# FROM df
# GROUP BY scenarioResults
# """

# sql_result = ps.sqldf(sql, locals())
# print(sql_result)

# sql_result = sql_result.reset_index()
# print(sql_result)
# fig = px.pie(values=sql_result["index"], names=sql_result["scenarioResults"])
# fig.update_traces(textposition='inside', textinfo='percent+label')
# # Edit the layout
# fig.update_layout(
#     # title={
#     # 'text' : '本日新增OB分布图',
#     # 'x':0.5,
#     # 'xanchor': 'center'}
#     # width = 1000,
#     height= 750
# )
# fig.show()

# new_response1 = response_data["scenarioResults"][0]['scenarioMetadata']['scenarioId'] ['jiraId'] ['issueTypes'] ['sceneTypes'] ['stable'] ['gradingReady']
# # data_frame=pd.DataFrame(new_response)


# file_name = 'MarksData.xlsx'
  
# # saving the excel
# data_frame.to_excel(file_name)


with open('/home/DEEPROUTE/jiananli/Desktop/text.txt', 'w') as file:
     file.write(json.dumps(response_data))