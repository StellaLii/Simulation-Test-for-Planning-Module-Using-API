#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
from pandas import DataFrame
import pandasql as ps
import plotly.graph_objects as go
import plotly.express as px
from module.simplatform import SimPlatformAPI
from module.jira_api import *

class analysis(object):
    def __init__(self):
        self.spa = SimPlatformAPI()
        self.ja = JiraAPI()

    def part_1(self):
        """
        
        """
        #加载data
        # 新版本
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")
        # dataframe1 = self.spa.get_scenario_result_v1()
        dataframe1 = dataframe1[['scenarioId','scenarioResults']]
        dataframe1.rename(columns={"scenarioResults": "0.63.3"}, inplace=True)
        # dataframe2 = self.spa.get_scenario_result_v2()
        dataframe2 = dataframe2[['scenarioId', 'jiraId', 'scenarioResults']]
        dataframe2.rename(columns={"scenarioResults": "0.63.6"}, inplace=True)
        # dataframe3 = self.spa.get_scenario_result_v3()
        # dataframe3 = dataframe3[['scenarioId', 'scenarioResults']]
        # dataframe3.rename(columns={"scenarioResults": "0.62.1"}, inplace=True)
        
        intersected_df = pd.merge(dataframe1, dataframe2, on = ['scenarioId'], how = 'inner')     
        # intersected_df = pd.merge(intersected_df1, dataframe3, on = ['scenarioId'], how = 'inner') 
        intersected_df.to_excel("intersected_df.xlsx")
        return intersected_df
    
    
if __name__ == '__main__':
    ana = analysis()
    ana.part_1()  
    # print(ana.part_1())