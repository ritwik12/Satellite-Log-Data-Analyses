# Satellite-Log-Data-Analysis
Performance and Scale team Red Hat

This tool is created for getting all the data related to a consumer-id and for analizing data in Satellite logs.<br>

### For consumer-id tool
We can print all the data related to all the consumer-ids using:
```
python3 main.py --all
```
Or print data related to a particular consumer-id:
```
python3 main.py --consumer-id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```
### For analize tool 
```
python3 main.py --analize
```
### For trace tool
```
python3 main.py --trace
```
### For specific time range
```
python3 main.py --all 2018-05-27T03:32:27 2018-07-01T05:13:36 2018-07-02T03:32:27 2018-07-13T15:13:36
```
```
python3 main.py --consumer-id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx 2018-07-02T03:32:27 2018-07-13T15:13:36
```
```
python3 main.py --analize 2018-07-02T03:32:27 2018-07-13T15:13:36
```
```
python3 main.py --trace 2018-07-02T03:32:27 2018-07-13T15:13:36
```
### Requirements
Install [ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html) API of Python
```
pip install elasticsearch
```
Install [tqdm](https://pypi.org/project/tqdm/) for progress bar
```
pip install tqdm
```
## Consumer-id Tool

We are not reading data directly from a file, we are using filebeat to read data from log files and pass it to logstash which later passes it to ElasticSearch where it get indexed in syntaxed JSON.<br>
We are reading that indexed data in ElasticSearch using <b>elasticsearch-py API</b>. There is a limit to elasticsearch, it can only read maximum of 10000 lines at most at a time. So, for this we are using <b>scroll API</b>. We are scrolling all the data in elasticsearch for 10 minutes at a rate of 10000 at a time.

The flow of data is from a consumer-id in production.log to candlepin.log of Satellite logs.

### Production.log

![production](https://user-images.githubusercontent.com/20038775/42319386-71fbf3f6-806f-11e8-8447-fc1f0d47ff25.png)

Here, In this image we can see production.log file of Satellite logs. A consumer-id is highlighted in this image which is 36 characters long in the form <b>xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx</b>.

This consumer-id is then extracted and we look for the lines related to this consumer id in candlepin.log.

### Candlepin.log

![candlepin](https://user-images.githubusercontent.com/20038775/42319627-2dc97554-8070-11e8-8f61-27df5a573ae4.png)

Here, In this image we can see candlepin.log file of Satellite logs. This file consists of logs related to consumer-id.
Every log is having a <b>csid</b>. A csid is highlighted in this image which is 8 characters long in the form <b>xxxxxxxx</b>.

After finding lines with csid, we are finding all the csid and grouping all the log lines related to a particular log together.

### All log data related to consumer-id with different csid(s)

![tool](https://user-images.githubusercontent.com/20038775/42320681-cb60c774-8073-11e8-8be3-8deede96fc64.png)
### All log data related to a particular consumer-id with different csid(s)
![consumer-id](https://user-images.githubusercontent.com/20038775/42320853-7a79fad2-8074-11e8-8188-6e7a4518e969.png)

## Analize Tool
This tool is related to fetching particular data such as <b>ActiveRecord, Views, totaltime, ID, etc</b> from production.log indexed data in ElasticSearch. We are getting data directly from ElasticSearch instead of a log file.<br>

After getting all the required data, we are formatting it in JSON format so as to be later used in a script to create new index in ElasticSearch which is later displayed in the form of visualizations on Kibana. [production_es.json](https://github.com/ritwik12/Satellite-Log-Data-Analysis/blob/master/Production_es/production_es.json) consists of the output JSON form data.

### analize.json

![production_es_json](https://user-images.githubusercontent.com/20038775/42321525-ebff09ac-8076-11e8-9a61-5dd45f2cdfaf.png)

After getting all the data in json format we are creating a new index in ElasticSearch which can be seen on Kibana.

### Analize Index

![kibana index](https://user-images.githubusercontent.com/20038775/42321630-443ac228-8077-11e8-8c1e-ce15e22f97d4.png)

### Kibana Dashboard for Visualizations

![dashboard](https://user-images.githubusercontent.com/20038775/42321719-8b7bb552-8077-11e8-8325-292d7e61be01.png)

### Visualizations

![views bar](https://user-images.githubusercontent.com/20038775/42321854-f67d26b0-8077-11e8-8d8e-8b191012ef66.png)

![activerecord](https://user-images.githubusercontent.com/20038775/42321852-f6179890-8077-11e8-9a56-d03eb5d47e30.png)

![totaltime](https://user-images.githubusercontent.com/20038775/42321853-f6486eb6-8077-11e8-917f-53e18ba07ca0.png)

## Trace tool
Able to display the trace records for stack traces that may appear in production.log. It is able to handle multiline logs also.

![trace](https://user-images.githubusercontent.com/20038775/42684935-3613a4d8-86af-11e8-9366-1001c266860b.png)
