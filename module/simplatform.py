#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
import csv
import pandas as pd
from pandas import DataFrame
import pandasql as ps
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import requests
from sqlalchemy import true
import numpy as np

class SimPlatformAPI(object):
    '''
    https://rqk9rsooi4.feishu.cn/wiki/wikcnYBG0G58wTAC9mW8keeIIGb#HiC4xU
    https://rqk9rsooi4.feishu.cn/wiki/wikcnO2o7gwVbedwfeWGcfrzwof#
    '''
    def __init__(self):
        pass

    def authority(self):
        pass
    
    def get_scenario_result(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            }
        
        A = '\"planning-cicd-single-frame-test-2-2-0-krxwq\"'
        data1 = '{"batch_name": '+A+'}' 
        

        response1 = requests.post('http://analysis-service.simulation-platform-prod.simulation.deeproute.ai/api/v2/get_scenario_results', headers=headers, data=data1)

        response_data1 = response1.json()
        # new_response = response_data["scenarioResults"][0]['metricResults'][0]['annotations']['scenario_result']
        # new_response1 = response_data["scenarioResults"][                0]['scenarioMetadata']['scenarioId']
        
        scenarioResults = []
        for i in response_data1["scenarioResults"]:
            for j in i ['metricResults']:
                if j['metricName'] == 'job_info':                                     
                    scenarioResults.append(j['annotations']['scenario_result'])
                    
        log_url = []
        for i in response_data1["scenarioResults"]:
            for j in i ['metricResults']:
                if j['metricName'] == 'job_info':
                    log_url.append(j['annotations']['log_url'])
                         
        scenarioId = []
        for i in response_data1["scenarioResults"]:
            scenarioId.append(i['scenarioMetadata']['scenarioId'])
            
        jiraId = []
        for i in response_data1["scenarioResults"]:
            try:
                jiraId.append(i['scenarioMetadata']['jiraId'])
            except:
                jiraId.append("None")
            
        issueTypes = []
        for i in response_data1["scenarioResults"]:
            try:
                issueTypes.append(i['scenarioMetadata']['issueTypes'])
            except:
                issueTypes.append("none")

        sceneTypes = []
        for i in response_data1["scenarioResults"]:
            try:
                sceneTypes.append(i['scenarioMetadata']['sceneTypes'])
            except:
                sceneTypes.append("none")
            
        stable = []
        for i in response_data1["scenarioResults"]:
            try:
                stable.append(i['scenarioMetadata']['stable'])
            except:
                stable.append("False")
            
        # gradingReady = []
        # for i in response_data["scenarioResults"]:
        #     gradingReady.append(i['scenarioMetadata']['gradingReady'])
        #     print(gradingReady)

        # dataframe = pd.DataFrame([scenarioId, jiraId, scenarioResults, stable, issueTypes, sceneTypes, log_url]).T
        # dataframe.columns = ["scenarioId", "jiraId","scenarioResults", "stable", "issueTypes", "sceneTypes", "log_url"]
        dataframe1 = pd.DataFrame([scenarioId, jiraId, scenarioResults, stable, log_url]).T
        dataframe1.columns = ["scenarioId", "jiraId","scenarioResults", "stable", "log_url"]

        dataframe1['scenarioId']= dataframe1['scenarioId'].astype('str')
        dataframe1['jiraId']= dataframe1['jiraId'].astype('str')
        dataframe1['scenarioResults']= dataframe1['scenarioResults'].astype('str')
        dataframe1['log_url']= dataframe1['log_url'].astype('str')
        dataframe1['stable']= dataframe1['stable'].astype('str')
        # dataframe['issueTypes']= dataframe['issueTypes'].astype('str')
        # dataframe['sceneTypes']= dataframe['sceneTypes'].astype('str')
        # dataframe.to_excel("output.xlsx")
        
        B = '\"planning-cicd-single-frame-test-2-2-0-tbr6v\"'
        data2 = '{"batch_name": '+B+'}' 

        response2 = requests.post('http://analysis-service.simulation-platform-prod.simulation.deeproute.ai/api/v2/get_scenario_results', headers=headers, data=data2)

        response_data2 = response2.json()
        # new_response = response_data["scenarioResults"][0]['metricResults'][0]['annotations']['scenario_result']
        # new_response1 = response_data["scenarioResults"][0]['scenarioMetadata']['scenarioId']
        
        scenarioResults = []
        for i in response_data2["scenarioResults"]:
            for j in i ['metricResults']:
                if j['metricName'] == 'job_info':
                    scenarioResults.append(j['annotations']['scenario_result'])
                    
        log_url = []
        for i in response_data2["scenarioResults"]:
            for j in i ['metricResults']:
                if j['metricName'] == 'job_info':
                    log_url.append(j['annotations']['log_url'])

        scenarioId = []
        for i in response_data2["scenarioResults"]:
            scenarioId.append(i['scenarioMetadata']['scenarioId'])
            
        jiraId = []
        for i in response_data2["scenarioResults"]:
            try:
                jiraId.append(i['scenarioMetadata']['jiraId'])
            except:
                jiraId.append("None")
            
        issueTypes = []
        for i in response_data2["scenarioResults"]:
            try:
                issueTypes.append(i['scenarioMetadata']['issueTypes'])
            except:
                issueTypes.append("none")

        sceneTypes = []
        for i in response_data2["scenarioResults"]:
            try:
                sceneTypes.append(i['scenarioMetadata']['sceneTypes'])
            except:
                sceneTypes.append("none")
            
        stable = []
        for i in response_data2["scenarioResults"]:
            try:
                stable.append(i['scenarioMetadata']['stable'])
            except:
                stable.append("False")
            
        dataframe2 = pd.DataFrame([scenarioId, jiraId, scenarioResults, stable, log_url]).T
        dataframe2.columns = ["scenarioId", "jiraId","scenarioResults", "stable", "log_url"]

        dataframe2['scenarioId']= dataframe2['scenarioId'].astype('str')
        dataframe2['jiraId']= dataframe2['jiraId'].astype('str')
        dataframe2['scenarioResults']= dataframe2['scenarioResults'].astype('str')
        dataframe2['log_url']= dataframe2['log_url'].astype('str')
        dataframe2['stable']= dataframe2['stable'].astype('str')
        
        dataframe = pd.concat([dataframe1,dataframe2],axis=0)
        # dataframe.to_excel("DataFile/0636.xlsx")
        return dataframe
    
    def get_failure_scenario_result(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            }

        A = '\"planning-cicd-single-frame-test-2-2-0-v8mz5\"'
        data1 = '{"batch_name": '+A+'}' 


        response1 = requests.post('http://analysis-service.simulation-platform-prod.simulation.deeproute.ai/api/v2/get_scenario_results', headers=headers, data=data1)

        response_data1 = response1.json()
        a = response_data1
        
        id_list1 = []
        jr_list1 = []
        mt_dict1 = dict()
        for item in a['scenarioResults']:
            flag = False
            for j in item["metricResults"]:
                if j["metricName"] == "job_info":
                    flag = j["annotations"]["scenario_result"]
            if flag == False:
                id = item["scenarioMetadata"]["scenarioId"]
                id_list1.append(item["scenarioMetadata"]["scenarioId"])
                try:
                    jr_list1.append(item["scenarioMetadata"]["jiraId"])
                except:
                    jr_list1.append(None)
                mt_dict1[item["scenarioMetadata"]["scenarioId"]] = []
                for j in item["metricResults"]:
                    try:
                        if j["annotations"]["hard_grading_result"] == False:
                            mt_dict1[id].append(j["metricName"])
                    except:
                        pass
        # print(json.dumps(mt_dict))
                    
        dataframe1 = pd.DataFrame([mt_dict1.keys(), mt_dict1.values()]).T
        dataframe1.columns = ['scenarioId', 'failedMetrics']
                
        dataframe1['jiraId'] = jr_list1


        B = '\"planning-cicd-single-frame-test-2-2-0-2r64x\"'
        data2 = '{"batch_name": '+B+'}' 
        
        response2 = requests.post('http://analysis-service.simulation-platform-prod.simulation.deeproute.ai/api/v2/get_scenario_results', headers=headers, data=data1)

        response_data2 = response2.json()
        b = response_data2
        
        id_list2 = []
        jr_list2 = []
        mt_dict2 = dict()
        for item in b['scenarioResults']:
            flag = False
            for j in item["metricResults"]:
                if j["metricName"] == "job_info":
                    flag = j["annotations"]["scenario_result"]
            if flag == False:
                id = item["scenarioMetadata"]["scenarioId"]
                id_list2.append(item["scenarioMetadata"]["scenarioId"])
                try:
                    jr_list2.append(item["scenarioMetadata"]["jiraId"])
                except:
                    jr_list2.append(None)
                mt_dict2[item["scenarioMetadata"]["scenarioId"]] = []
                for j in item["metricResults"]:
                    try:
                        if j["annotations"]["hard_grading_result"] == False:
                            mt_dict2[id].append(j["metricName"])
                    except:
                        pass
        # print(json.dumps(mt_dict))
                    
        dataframe2 = pd.DataFrame([mt_dict2.keys(), mt_dict2.values()]).T
        dataframe2.columns = ['scenarioId', 'failedMetrics']
                
        dataframe2['jiraId'] = jr_list2
        
        dataframe = pd.concat([dataframe1,dataframe2],axis=0)
        dataframe.to_excel("DataFile/failedMetrics.xlsx")
        return dataframe
    
    def get_failed_metrics_sum(self):
        dataframe = pd.read_excel("DataFile/failedMetrics.xlsx")
        # df = dataframe.explode(["scenarioId","failedMetrics"])
        dataframe["failedMetrics"] = dataframe["failedMetrics"].astype(str).str.replace("'", "", regex=True)
        dataframe["failedMetrics"] = dataframe["failedMetrics"].astype(str).str.replace("[", "", regex=True)
        dataframe["failedMetrics"] = dataframe["failedMetrics"].astype(str).str.replace("]", "", regex=True)
        dataframe["failedMetrics"] = dataframe["failedMetrics"].str.split(",")        
        df = dataframe.explode("failedMetrics")
        df = df["failedMetrics"].value_counts(dropna=False)
        df = df.to_frame()
        df = df.reset_index()
        df = df.rename(columns={'failedMetrics':'Count'})
        df = df.rename(columns={'index':'failedMetrics'})
        df["failedMetrics"].replace('', np.nan, inplace=True)
        df.dropna(subset=["failedMetrics"], inplace=True)
        # print(df)
        return df
            

    # def list_features(self):
    #     response = requests.get('http://scenario-service.simulation-platform-prod.simulation.deeproute.ai/api/v2/list_features', json={})
    #     response_data = response.text
    #     return response_data
    
    # def get_feature_id(self):
    #     response = requests.get('http://scenario-service.simulation-platform-prod.simulation.deeproute.ai/api/v2/get_scenario_id_by_feature_id', json = {"feature_id": 1})
    #     response_data = response.json()
        
    #     df = pd.read_csv('get_feature_id.csv')   
    #     return df
    
if __name__ == '__main__':
    spa = SimPlatformAPI()
    s = spa.get_scenario_result()
    k = spa.get_failure_scenario_result()
    t = spa.get_failed_metrics_sum()
    # s = spa.list_features()
    # t = spa.get_feature_id()
    # print(r)
    # print(s)
    # print(t)