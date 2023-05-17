# SimAPITest
```

├── analysis.py  //调用module里的内容所做的analysis
├── DataFile //module/simplatform接口的内容写入本file，直接调用CI会十分慢
│   ├── 0621.xlsx
│   ├── 0633.xlsx
│   ├── 0636.xlsx
│   └── failedMetrics.xlsx
├── example.xlsx
├── feature_improve.py  //自定义功能测试脚本
├── get_feature_id.csv
├── JSON_List  //根据Feature划分scenario合集 Cr: Yaoqi Tan
│   ├── example.json
│   ├── path自检.json
│   ├── specified_list.json
│   ├── 不合理变道.json
│   ├── 不按规定路线行驶.json
│   ├── 不明停止线.json
│   ├── 主动压实线绕障.json
│   ├── 冲红灯.json
│   ├── 减少abnstatic误判.json
│   ├── 压实线行驶.json
│   ├── 实线变道.json
│   ├── 无变道.json
│   ├── 狭窄路口禁止压实线变道.json
│   ├── 规划角度过大.json
│   └── 跟行慢速车辆.json
├── module
│   ├── jira_api.py  //Jira API
│   └── simplatform.py  //Simplatform API
├── module_versions_config.json
├── output.xlsx
├── README.md
├── Report.ipynb //仿真report
├── Repro.ipynb  //同版本仿真比路测结果对比
├── requirements.txt
├── RT.ipynb
├── submit_workflow.py
└── test.py