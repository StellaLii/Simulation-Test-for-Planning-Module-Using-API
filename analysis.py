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
        
    def part_1a(self):
        """
        整体对比，新版本和之前版本的pass率
        """
        #加载data
        # dataframe1 = self.spa.get_scenario_result_v1()
        # dataframe2 = self.spa.get_scenario_result_v2()
        # dataframe3 = self.spa.get_scenario_result_v3()
        
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")

        df1 = dataframe1.groupby(['scenarioResults']).count()
        df1= df1.reset_index()
        df1['Percent(%)'] = ((df1['scenarioId'] / df1['scenarioId'].sum()) * 100).round(2)
        df1.rename(columns={"scenarioId": "Count"}, inplace=True)
        df1 = df1[['scenarioResults', 'Count', 'Percent(%)']]
        df1["Version"] = "0.63.3"
        

        df2 = dataframe2.groupby(['scenarioResults']).count()
        df2= df2.reset_index()
        df2['Percent(%)'] = ((df2['scenarioId'] / df2['scenarioId'].sum()) * 100).round(2)
        df2.rename(columns={"scenarioId": "Count"}, inplace=True)
        # df2 = df2[['scenarioResults', 'Count', 'Percent(%)']]
        df2 = df2[['Count', 'Percent(%)']]
        df2["Version"] = "0.63.6"
        
        # df3 = dataframe3.groupby(['scenarioResults']).count()
        # df3= df3.reset_index()
        # df3['Percent(%)'] = ((df3['scenarioId'] / df3['scenarioId'].sum()) * 100).round(2)
        # df3.rename(columns={"scenarioId": "Count"}, inplace=True)
        # # df2 = df2[['scenarioResults', 'Count', 'Percent(%)']]
        # df3 = df3[['Count', 'Percent(%)']]
        # df3["Version"] = "0.62.1"
        
        # df=pd.concat([df1,df2,df3],axis=1)
        df=pd.concat([df1,df2],axis=1)
        return df
    
    def part_1b(self):
        """
        整体对比，新版本和之前版本的pass率
        """
        #加载data
        # dataframe1 = self.spa.get_scenario_result_v1()
        # dataframe2 = self.spa.get_scenario_result_v2()
        # dataframe3 = self.spa.get_scenario_result_v3()
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")

        df1 = dataframe1.groupby(['scenarioResults']).count()
        df1= df1.reset_index()
        df1['Percent(%)'] = ((df1['scenarioId'] / df1['scenarioId'].sum()) * 100).round(2)
        df1.rename(columns={"scenarioId": "Count"}, inplace=True)
        df1 = df1[['scenarioResults', 'Count', 'Percent(%)']]
        df1["Version"] = "0.63.3"
        

        df2 = dataframe2.groupby(['scenarioResults']).count()
        df2= df2.reset_index()
        df2['Percent(%)'] = ((df2['scenarioId'] / df2['scenarioId'].sum()) * 100).round(2)
        df2.rename(columns={"scenarioId": "Count"}, inplace=True)
        df2 = df2[['scenarioResults', 'Count', 'Percent(%)']]
        # df2 = df2[['Count', 'Percent(%)']]
        df2["Version"] = "0.63.6"
        
        # df3 = dataframe3.groupby(['scenarioResults']).count()
        # df3= df3.reset_index()
        # df3['Percent(%)'] = ((df3['scenarioId'] / df3['scenarioId'].sum()) * 100).round(2)
        # df3.rename(columns={"scenarioId": "Count"}, inplace=True)
        # df3 = df3[['scenarioResults', 'Count', 'Percent(%)']]
        # # df3 = df3[['Count', 'Percent(%)']]
        # df3["Version"] = "0.62.1"
        
        # df=pd.concat([df1,df2,df3],axis=0)
        df=pd.concat([df1,df2],axis=0)
        return df

    def part_2a(self):
        # dataframe1 = self.spa.get_scenario_result_v1()
        # dataframe2 = self.spa.get_scenario_result_v2()
        # dataframe3 = self.spa.get_scenario_result_v3()
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")
        
        jql = "project = PLANNING AND (summary ~ 参考线 OR summary ~ 公交车道  OR  summary ~ 辅道 ) "
        dataframe = self.ja.deal_data(jql)
        
        intersected_df1 = pd.merge(dataframe1, dataframe, on = ['jiraId'], how='inner')
        df1 = intersected_df1.groupby(['scenarioResults']).count()
        df1= df1.reset_index()
        df1['Percent(%)'] = ((df1['scenarioId'] / df1['scenarioId'].sum()) * 100).round(2)
        df1.rename(columns={"scenarioId": "Count"}, inplace=True)
        df1 = df1[['scenarioResults', 'Count', 'Percent(%)']]
        df1["Version"] = "0.63.3"
        
        
        intersected_df2 = pd.merge(dataframe2, dataframe, on = ['jiraId'], how='inner')
        df2 = intersected_df2.groupby(['scenarioResults']).count()
        df2= df2.reset_index()
        df2['Percent(%)'] = ((df2['scenarioId'] / df2['scenarioId'].sum()) * 100).round(2)
        df2.rename(columns={"scenarioId": "Count"}, inplace=True)
        df2 = df2[['scenarioResults','Count', 'Percent(%)']]
        df2["Version"] = "0.63.6"
        
        # intersected_df3 = pd.merge(dataframe3, dataframe, on = ['jiraId'], how='inner')
        # df3 = intersected_df3.groupby(['scenarioResults']).count()
        # df3= df3.reset_index()
        # df3['Percent(%)'] = ((df3['scenarioId'] / df3['scenarioId'].sum()) * 100).round(2)
        # df3.rename(columns={"scenarioId": "Count"}, inplace=True)
        # df3 = df3[['scenarioResults','Count', 'Percent(%)']]
        # df3["Version"] = "0.62.1"
        
        df=pd.concat([df1,df2],axis=0)
        df["Type"] = "Routing"
        return df
        

    def part_2b(self):
        # dataframe1 = self.spa.get_scenario_result_v1()
        # dataframe2 = self.spa.get_scenario_result_v2()
        # dataframe3 = self.spa.get_scenario_result_v3()
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")
        
        jql = "project = PLANNING AND (summary ~ 压实线  OR summary ~ 横向转向过大  OR summary ~ path大  OR summary ~ 马路牙 OR summary ~ path不更新 OR summary ~  抖动 OR summary ~ 摇晃)"
        dataframe = self.ja.deal_data(jql)
        
        intersected_df1 = pd.merge(dataframe1, dataframe, on = ['jiraId'], how='inner')
        df1 = intersected_df1.groupby(['scenarioResults']).count()
        df1= df1.reset_index()
        df1['Percent(%)'] = ((df1['scenarioId'] / df1['scenarioId'].sum()) * 100).round(2)
        df1.rename(columns={"scenarioId": "Count"}, inplace=True)
        df1 = df1[['scenarioResults', 'Count', 'Percent(%)']]
        df1["Version"] = "0.63.3"
        
        
        intersected_df2 = pd.merge(dataframe2, dataframe, on = ['jiraId'], how='inner')
        df2 = intersected_df2.groupby(['scenarioResults']).count()
        df2= df2.reset_index()
        df2['Percent(%)'] = ((df2['scenarioId'] / df2['scenarioId'].sum()) * 100).round(2)
        df2.rename(columns={"scenarioId": "Count"}, inplace=True)
        df2 = df2[['scenarioResults','Count', 'Percent(%)']]
        df2["Version"] = "0.63.6"
        
        # intersected_df3 = pd.merge(dataframe3, dataframe, on = ['jiraId'], how='inner')
        # df3 = intersected_df3.groupby(['scenarioResults']).count()
        # df3= df3.reset_index()
        # df3['Percent(%)'] = ((df3['scenarioId'] / df3['scenarioId'].sum()) * 100).round(2)
        # df3.rename(columns={"scenarioId": "Count"}, inplace=True)
        # df3 = df3[['scenarioResults','Count', 'Percent(%)']]
        # df3["Version"] = "0.62.1"
        
        df=pd.concat([df1,df2],axis=0)
        df["Type"] = "Path"
        return df
    

    def part_2c(self):
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")
        
        jql = "project = PLANNING AND (summary ~ 点刹 OR summary ~ 急刹  OR  summary ~ 莫名减速  OR summary ~ 刹不住 OR summary ~ acceleration OR summary ~ brake)"
        dataframe = self.ja.deal_data(jql)
        
        intersected_df1 = pd.merge(dataframe1, dataframe, on = ['jiraId'], how='inner')
        df1 = intersected_df1.groupby(['scenarioResults']).count()
        df1= df1.reset_index()
        df1['Percent(%)'] = ((df1['scenarioId'] / df1['scenarioId'].sum()) * 100).round(2)
        df1.rename(columns={"scenarioId": "Count"}, inplace=True)
        df1 = df1[['scenarioResults', 'Count', 'Percent(%)']]
        df1["Version"] = "0.63.3"
        
        
        intersected_df2 = pd.merge(dataframe2, dataframe, on = ['jiraId'], how='inner')
        df2 = intersected_df2.groupby(['scenarioResults']).count()
        df2= df2.reset_index()
        df2['Percent(%)'] = ((df2['scenarioId'] / df2['scenarioId'].sum()) * 100).round(2)
        df2.rename(columns={"scenarioId": "Count"}, inplace=True)
        df2 = df2[['scenarioResults','Count', 'Percent(%)']]
        df2["Version"] = "0.63.6"
        
        # intersected_df3 = pd.merge(dataframe3, dataframe, on = ['jiraId'], how='inner')
        # df3 = intersected_df3.groupby(['scenarioResults']).count()
        # df3= df3.reset_index()
        # df3['Percent(%)'] = ((df3['scenarioId'] / df3['scenarioId'].sum()) * 100).round(2)
        # df3.rename(columns={"scenarioId": "Count"}, inplace=True)
        # df3 = df3[['scenarioResults','Count', 'Percent(%)']]
        # df3["Version"] = "0.62.1"
        
        df=pd.concat([df1,df2],axis=0)
        df["Type"] = "速度"
        return df
    

    def part_2d(self):
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")
        
        jql = "project = PLANNING AND (summary ~ 变道 OR summary ~ 提前进入右转道 OR summary ~ change)"
        dataframe = self.ja.deal_data(jql)
        
        intersected_df1 = pd.merge(dataframe1, dataframe, on = ['jiraId'], how='inner')
        df1 = intersected_df1.groupby(['scenarioResults']).count()
        df1= df1.reset_index()
        df1['Percent(%)'] = ((df1['scenarioId'] / df1['scenarioId'].sum()) * 100).round(2)
        df1.rename(columns={"scenarioId": "Count"}, inplace=True)
        df1 = df1[['scenarioResults', 'Count', 'Percent(%)']]
        df1["Version"] = "0.63.3"
        
        
        intersected_df2 = pd.merge(dataframe2, dataframe, on = ['jiraId'], how='inner')
        df2 = intersected_df2.groupby(['scenarioResults']).count()
        df2= df2.reset_index()
        df2['Percent(%)'] = ((df2['scenarioId'] / df2['scenarioId'].sum()) * 100).round(2)
        df2.rename(columns={"scenarioId": "Count"}, inplace=True)
        df2 = df2[['scenarioResults','Count', 'Percent(%)']]
        df2["Version"] = "0.63.6"
        
        # intersected_df3 = pd.merge(dataframe3, dataframe, on = ['jiraId'], how='inner')
        # df3 = intersected_df3.groupby(['scenarioResults']).count()
        # df3= df3.reset_index()
        # df3['Percent(%)'] = ((df3['scenarioId'] / df3['scenarioId'].sum()) * 100).round(2)
        # df3.rename(columns={"scenarioId": "Count"}, inplace=True)
        # df3 = df3[['scenarioResults','Count', 'Percent(%)']]
        # df3["Version"] = "0.62.1"
        
        df=pd.concat([df1,df2],axis=0)
        df["Type"] = "变道"
        return df
    

    def part_2e(self):
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")
        
        jql = "project = PLANNING AND (summary ~ crash OR summary ~ path不更新)"
        dataframe = self.ja.deal_data(jql)
        
        intersected_df1 = pd.merge(dataframe1, dataframe, on = ['jiraId'], how='inner')
        df1 = intersected_df1.groupby(['scenarioResults']).count()
        df1= df1.reset_index()
        df1['Percent(%)'] = ((df1['scenarioId'] / df1['scenarioId'].sum()) * 100).round(2)
        df1.rename(columns={"scenarioId": "Count"}, inplace=True)
        df1 = df1[['scenarioResults', 'Count', 'Percent(%)']]
        df1["Version"] = "0.63.3"
        
        
        intersected_df2 = pd.merge(dataframe2, dataframe, on = ['jiraId'], how='inner')
        df2 = intersected_df2.groupby(['scenarioResults']).count()
        df2= df2.reset_index()
        df2['Percent(%)'] = ((df2['scenarioId'] / df2['scenarioId'].sum()) * 100).round(2)
        df2.rename(columns={"scenarioId": "Count"}, inplace=True)
        df2 = df2[['scenarioResults','Count', 'Percent(%)']]
        df2["Version"] = "0.63.6"
        
        # intersected_df3 = pd.merge(dataframe3, dataframe, on = ['jiraId'], how='inner')
        # df3 = intersected_df3.groupby(['scenarioResults']).count()
        # df3= df3.reset_index()
        # df3['Percent(%)'] = ((df3['scenarioId'] / df3['scenarioId'].sum()) * 100).round(2)
        # df3.rename(columns={"scenarioId": "Count"}, inplace=True)
        # df3 = df3[['scenarioResults','Count', 'Percent(%)']]
        # df3["Version"] = "0.62.1"
        
        df=pd.concat([df1,df2],axis=0)
        df["Type"] = "程序异常"
        return df
    

    def part_2f(self):
        # dataframe1 = self.spa.get_scenario_result_v1()
        # dataframe2 = self.spa.get_scenario_result_v2()
        # dataframe3 = self.spa.get_scenario_result_v3()
        
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")
        
        jql = "project = PLANNING AND (summary ~ 红灯  OR summary ~ 左转  OR summary ~ 黄灯  OR summary ~ 礼让  OR summary ~ cutin OR summary ~ 汇流  OR  summary ~ 无保护  OR summary ~ 左右转弯急刹)"
        dataframe = self.ja.deal_data(jql)
        
        intersected_df1 = pd.merge(dataframe1, dataframe, on = ['jiraId'], how='inner')
        df1 = intersected_df1.groupby(['scenarioResults']).count()
        df1= df1.reset_index()
        df1['Percent(%)'] = ((df1['scenarioId'] / df1['scenarioId'].sum()) * 100).round(2)
        df1.rename(columns={"scenarioId": "Count"}, inplace=True)
        df1 = df1[['scenarioResults', 'Count', 'Percent(%)']]
        df1["Version"] = "0.63.3"
        
        
        intersected_df2 = pd.merge(dataframe2, dataframe, on = ['jiraId'], how='inner')
        df2 = intersected_df2.groupby(['scenarioResults']).count()
        df2= df2.reset_index()
        df2['Percent(%)'] = ((df2['scenarioId'] / df2['scenarioId'].sum()) * 100).round(2)
        df2.rename(columns={"scenarioId": "Count"}, inplace=True)
        df2 = df2[['scenarioResults','Count', 'Percent(%)']]
        df2["Version"] = "0.63.6"
        
        # intersected_df3 = pd.merge(dataframe3, dataframe, on = ['jiraId'], how='inner')
        # df3 = intersected_df3.groupby(['scenarioResults']).count()
        # df3= df3.reset_index()
        # df3['Percent(%)'] = ((df3['scenarioId'] / df3['scenarioId'].sum()) * 100).round(2)
        # df3.rename(columns={"scenarioId": "Count"}, inplace=True)
        # df3 = df3[['scenarioResults','Count', 'Percent(%)']]
        # df3["Version"] = "0.62.1"
        
        # df=pd.concat([df1,df2,df3],axis=0)
        df=pd.concat([df1,df2],axis=0)
        df["Type"] = "其他"
        return df
    
    def part_2g(self):
        # dataframe1 = self.spa.get_scenario_result_v1()
        # dataframe2 = self.spa.get_scenario_result_v2()
        # dataframe3 = self.spa.get_scenario_result_v3()
        
        dataframe1 = pd.read_excel("DataFile/0633.xlsx")
        dataframe2 = pd.read_excel("DataFile/0636.xlsx")
        
        jql = "project = PLANNING AND (summary ~ 无变道)"
        dataframe = self.ja.deal_data(jql)
        
        intersected_df1 = pd.merge(dataframe1, dataframe, on = ['jiraId'], how='inner')
        df1 = intersected_df1.groupby(['scenarioResults']).count()
        df1= df1.reset_index()
        df1['Percent(%)'] = ((df1['scenarioId'] / df1['scenarioId'].sum()) * 100).round(2)
        df1.rename(columns={"scenarioId": "Count"}, inplace=True)
        df1 = df1[['scenarioResults', 'Count', 'Percent(%)']]
        df1["Version"] = "0.63.3"
        
        
        intersected_df2 = pd.merge(dataframe2, dataframe, on = ['jiraId'], how='inner')
        df2 = intersected_df2.groupby(['scenarioResults']).count()
        df2= df2.reset_index()
        df2['Percent(%)'] = ((df2['scenarioId'] / df2['scenarioId'].sum()) * 100).round(2)
        df2.rename(columns={"scenarioId": "Count"}, inplace=True)
        df2 = df2[['scenarioResults','Count', 'Percent(%)']]
        df2["Version"] = "0.63.6"
        
        # intersected_df3 = pd.merge(dataframe3, dataframe, on = ['jiraId'], how='inner')
        # df3 = intersected_df3.groupby(['scenarioResults']).count()
        # df3= df3.reset_index()
        # df3['Percent(%)'] = ((df3['scenarioId'] / df3['scenarioId'].sum()) * 100).round(2)
        # df3.rename(columns={"scenarioId": "Count"}, inplace=True)
        # df3 = df3[['scenarioResults','Count', 'Percent(%)']]
        # df3["Version"] = "0.62.1"
        
        # df=pd.concat([df1,df2,df3],axis=0)
        df=pd.concat([df1,df2],axis=0)
        df["Type"] = "无变道相关"
        return df
        
    def part_3a(self):
        version = "0.63.6"
        jql = "project = PLANNING AND 'Planning Version Number (请只写版本数字，例如 “0.2.1”）' ~" + version
        dataframe = self.ja.deal_data2(jql)
        
        dataframe['问题类别描述'] = dataframe['问题类别描述'].astype(str)
        df = dataframe.groupby(['问题类别描述']).count()
        df= df.reset_index()
        df.rename(columns={"jiraId": "Count"}, inplace=True)

        # df2['Percent'] = (df2['Count'] / df2['Count'].sum()) * 100
        fig = px.pie(values=df["Count"], names=df["问题类别描述"])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        # Edit the layout
        fig.update_layout(
            title={
            'text' : '新增Issues类型分布',
            'x':0.5,
            'xanchor': 'center'},
            width = 1500,
            height= 1200,
            )
        return fig
        # fig.show()
        
    def part_3b(self):
        version = "0.63.3"
        jql1 = "project = PLANNING AND (summary ~ 参考线 OR summary ~ 公交车道  OR  summary ~ 辅道 ) AND 'Planning Version Number (请只写版本数字，例如 “0.2.1”）' ~ "+ version
        df1 = self.ja.deal_data(jql1)
        df1["Type"] = "Routing"
        
        jql2 = "project = PLANNING AND (summary ~ 压实线  OR summary ~ 横向转向过大  OR summary ~ path大  OR summary ~ 马路牙 OR summary ~ path不更新 OR summary ~  抖动 OR summary ~ 摇晃)AND 'Planning Version Number (请只写版本数字，例如 “0.2.1”）' ~ "+ version
        df2 = self.ja.deal_data(jql2)
        df2["Type"] = "Path"
        
        jql3 = "project = PLANNING AND (summary ~ 点刹 OR summary ~ 急刹  OR  summary ~ 莫名减速  OR summary ~ 刹不住 OR summary ~ acceleration OR summary ~ brake) AND 'Planning Version Number (请只写版本数字，例如 “0.2.1”）' ~ "+ version
        df3 = self.ja.deal_data(jql3)
        df3["Type"] = "速度"
        
        jql4 = "project = PLANNING AND (summary ~ 变道 OR summary ~ 提前进入右转道 OR summary ~ change) AND 'Planning Version Number (请只写版本数字，例如 “0.2.1”）' ~ "+ version
        df4 = self.ja.deal_data(jql4)
        df4["Type"] = "变道"
        
        jql5 = "project = PLANNING AND (summary ~ crash OR summary ~ path不更新) AND 'Planning Version Number (请只写版本数字，例如 “0.2.1”）' ~ "+ version
        df5 = self.ja.deal_data(jql5)
        df5["Type"] = "程序异常"
        
        jql6 = "project = PLANNING AND (summary ~ 红灯  OR summary ~ 左转  OR summary ~ 黄灯  OR summary ~ 礼让  OR summary ~ cutin OR summary ~ 汇流  OR  summary ~ 无保护  OR summary ~ 左右转弯急刹) AND 'Planning Version Number (请只写版本数字，例如 “0.2.1”）' ~ "+ version
        df6 = self.ja.deal_data(jql6)
        df6["Type"] = "其他"
        
        dataframe=pd.concat([df1,df2,df3,df4,df5,df6],axis=0)

        df = dataframe.groupby(['Type']).count()
        df= df.reset_index()
        df.rename(columns={"jiraId": "Count"}, inplace=True)

        fig = px.pie(values=df["Count"], names=df["Type"])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        # Edit the layout
        fig.update_layout(
            title={
            'text' : '新增Issues类型分布',
            'x':0.5,
            'xanchor': 'center'},
            width = 1000,
            height= 800,
            )
        return fig
        
    def part_3c(self):
        version = "0.63.3"
        try:
            jql = "project = PLANNING AND 'Planning Version Number (请只写版本数字，例如 “0.2.1”）' ~" + version
            dataframe = self.ja.deal_data2(jql)
            return dataframe
        except:
            pass
        
    """
    单版本仿真结果对比, 需要做完grading
    """
    def part_3d(self):
        version = "0.63.6"
        jql = "project = PLANNING AND 'Planning Version Number (请只写版本数字，例如 “0.2.1”）' ~" + version
        dataframe1 = self.ja.deal_data(jql)
        dataframe1.rename(columns={"Key": "jiraId"}, inplace=True)
        
        dataframe2 = pd.read_excel("DataFile/failedMetrics.xlsx")
        
        intersected_df = pd.merge(dataframe1, dataframe2, on = ['jiraId'], how='inner')
        intersected_df = intersected_df[['jiraId', 'summary', 'scenarioId', 'failedMetrics']]
        return intersected_df
    
    
    def part_4(self):
        return self.spa.get_failed_metrics_sum()

        
        
if __name__ == '__main__':
    ana = analysis()
    ana.part_1a()   
    # print(ana.part_3b())
    # ana.part_2b()
    ana.part_3a()
    print(ana.part_3d())