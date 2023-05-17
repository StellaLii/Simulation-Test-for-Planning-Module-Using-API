import plotly.graph_objs as go
from jira import JIRA
import pandas as pd
import datetime
from IPython.display import display, HTML

USER = 'simulationTest0'
PASSWD = '123456Qq.'


class JiraAPI(object):
    '''
    query issues to dataframe
    '''
    def __init__(self):
        self.jira = self.authority(USER, PASSWD)

    def authority(self, user, passwd):
        options = {"server": "https://jira.deeproute.ai/"}
        jira = JIRA(options, basic_auth=(user, passwd))
        return jira

    def search_issues(self, jql):
        block_size = 1000
        block_num = 0
        all_issues = []
        while True:
            start_idx = block_num * block_size
            issues = self.jira.search_issues(jql, start_idx, block_size)
            if len(issues) == 0:
                break
            block_num += 1
            for issue in issues:
                all_issues.append(issue)
        return all_issues

    def deal_data(self, jql):
        all_issues = self.search_issues(jql)
        issue_dicts = []
        for issue in all_issues:
            issue_dict = {
                'key': issue.key,
                'summary': issue.fields.summary,
                # 'assignee': issue.fields.assignee,
                # 'status': issue.fields.status.name,
                #'reporter': issue.fields.reporter,
                # 'created': issue.fields.created,
                #'priority': issue.fields.priority.name,
                # 'components': [c.name for c in issue.fields.components],
                # 'labels': issue.fields.labels
            }
            issue_dicts.append(issue_dict)

        data_frame = pd.DataFrame(issue_dicts)
        
        data_frame.rename(columns={"key": "jiraId"}, inplace=True)
        # data_frame['created'] = data_frame['created'].str.replace("T", " ")
        # data_frame['created']=[x[:19] for x in data_frame['created']]
        # data_frame['components'] = data_frame['components'].astype(str).str.replace("[", "", regex=True)
        # data_frame['components'] = data_frame['components'].astype(str).str.replace("]", "", regex=True)
        # data_frame['components'] = data_frame['components'].astype(str).str.replace("'", "", regex=True)
        # data_frame['labels'] = data_frame['labels'].astype(str).str.replace("[", "", regex=True)
        # data_frame['labels'] = data_frame['labels'].astype(str).str.replace("]", "", regex=True)
        # data_frame['labels'] = data_frame['labels'].astype(str).str.replace("'", "", regex=True)
        return data_frame
    
    def deal_data2(self, jql):
        all_issues = self.search_issues(jql)
        issue_dicts = []
        for issue in all_issues:
            issue_dict = {
                'key': issue.key,
                'summary': issue.fields.summary,
                # 'assignee': issue.fields.assignee,
                # 'status': issue.fields.status.name,
                #'reporter': issue.fields.reporter,
                # 'created': issue.fields.created,
                #'priority': issue.fields.priority.name,
                # 'components': [c.name for c in issue.fields.components],
                '问题类别描述': issue.fields.customfield_11404,
                # 'labels': issue.fields.labels
            }
            issue_dicts.append(issue_dict)

        data_frame = pd.DataFrame(issue_dicts)
        
        data_frame.rename(columns={"key": "jiraId"}, inplace=True)
        # data_frame['created'] = data_frame['created'].str.replace("T", " ")
        # data_frame['created']=[x[:19] for x in data_frame['created']]
        # data_frame['components'] = data_frame['components'].astype(str).str.replace("[", "", regex=True)
        # data_frame['components'] = data_frame['components'].astype(str).str.replace("]", "", regex=True)
        # data_frame['components'] = data_frame['components'].astype(str).str.replace("'", "", regex=True)
        # data_frame['labels'] = data_frame['labels'].astype(str).str.replace("[", "", regex=True)
        # data_frame['labels'] = data_frame['labels'].astype(str).str.replace("]", "", regex=True)
        # data_frame['labels'] = data_frame['labels'].astype(str).str.replace("'", "", regex=True)
        def link_func(
            ob): return '[%s](https://jira.deeproute.ai/browse/%s)' % (ob, ob)

        deal_key = pd.DataFrame(
            {"jiraId": data_frame["jiraId"], "jiraId1": data_frame["jiraId"].apply(link_func)})
        merge_data = pd.merge(deal_key, data_frame)
        merge_data.rename(
            columns=({"jiraId": "jiraIds", "jiraId1": "jiraId"}), inplace=True)
        merge_data = merge_data.drop('jiraIds', axis=1)
        return merge_data


if __name__ == '__main__':

    # jql = 'project = OB AND created >= ' + yesterday + \
    #     ' AND created <= ' + today + ' ORDER BY priority DESC, updated DESC'
    # jql = 'project = PLANNING AND "Planning Version Number (请只写版本数字，例如 “0.2.1”）" ~ 0.61.0'
    jql = 'project = PLANNING AND "Planning Version Number (请只写版本数字，例如 “0.2.1”）" ~ 0.61.0'
    ja = JiraAPI()
    
    kk = ja.deal_data2(jql)

    # print(kk['问题类别描述'].dtypes)
    # file_name = 'MarksData.xlsx'
  
    # # saving the excel
    # kk.to_excel(file_name)