from elasticsearch import Elasticsearch
import re
import timeit
import time
# progress bar
from tqdm import tqdm 
start = timeit.default_timer()
es = Elasticsearch()
# scroll 10000 lines per scroll of all data for 10m, using maximum value for size i.e 10000 
res = es.search(index="file1",scroll="10m", size="10000", body={"query": {"match_all": {}}}) 
# scroll id to mark scroll
sid = res['_scroll_id'] 
scroll_size = res['hits']['total']
# create production.json for storing all the data fetched from ES 
file =open("production_es.json","w")
# Start scrolling
while (scroll_size > 0):
    # _id count starting from 0
    i=0
    res = es.scroll(scroll_id = sid, scroll = '10m')
	# Update the scroll ID
    sid = res['_scroll_id']
	# Get the number of results that we returned in the last scroll
    scroll_size = len(res['hits']['hits'])
    # tqdm is used for progress bar
    for doc in tqdm(res['hits']['hits']):
        # progress bar speed (iterations/sec)
        time.sleep(0.0000000000001) 
        s = "%s)%s" % ( doc['_source']['source'],doc['_source']['message'])
        line = "%s" % ( doc['_source']['message'])
        # For production.log realated data only containing "Views"
        if s.find("production.log")!=-1 and line.find("Views")!=-1:
            i=i+1
            # Extract ID
            id = line[27:32]
            # Extract time
            log_time = line[11:19]
            # Extract total time 
            totaltime = line[line.find("in")+3: line.find("in")+8]
            # Extract Views
            Views = line[line.find("Views")+7: line.find("Views")+12]
            # Extract ActiveRecord
            ActiveRecord = line[line.find("ActiveRecord")+14: line.find("ActiveRecord")+20]
            # Store data in JSON format to be indexed in ElasticSearch
            json = """{"index":{"_index":"production","_id":"""+'"'+str(i-1)+'"'+"""}} \n {"time":"""+'"'+log_time+'"'+""","Totaltime":"""+'"'+totaltime+'"'+""","ID ":"""+'"'+id+'"'+""","Views":"""+'"'+Views+'"'+""","ActiveRecord":"""+'"'+ActiveRecord+'"'+"}"+"\n"
            # Write JSON formatted data to production_es.json
            file.write(json)
stop = timeit.default_timer()
print(stop - start) 