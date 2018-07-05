from elasticsearch import Elasticsearch
import re
import timeit
import sys
import time
# progress bar
from tqdm import tqdm

# Run the code only if the arguments passed are --all or --consumer-id
if "--all" in sys.argv or "--consumer-id" in sys.argv:
    start = timeit.default_timer()
    es = Elasticsearch()
    # scroll 10000 lines per scroll of all data for 10m, using maximum value for size i.e 10000 
    res = es.search(index="file1",scroll="10m", size="10000", body={"query": {"match_all": {}}})
    # scroll id to mark scroll
    sid = res['_scroll_id']
    scroll_size = res['hits']['total']
    count=0
    ID= ""
    csid=""
    data={}
    if "--consumer-id" in sys.argv:
      # Fetch consumer-id from second argument passed 
        id=sys.argv[2]
    # Start scrolling
    while (scroll_size > 0):
        res = es.scroll(scroll_id = sid, scroll = '10m')
        # Update the scroll ID
        sid = res['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(res['hits']['hits'])
        # tqdm is used for progress bar
        for doc in tqdm(res['hits']['hits']):
            # progress bar speed (iterations/sec)
            time.sleep(0.0000000000001)
            # Extarct log line from ElasticSearch
            log_line = "%s)%s" % ( doc['_source']['source'],doc['_source']['message'])  
            # Extract lines consisting only message from log lines
            line = "%s" % ( doc['_source']['message'])
            # Find all the consumer ids present in ElasticSearch
            consumer_id=re.search('[-a-zA-Z0-9]{36}', log_line)
            # For production.log realated data only 
            if consumer_id and log_line.find("production.log")!=-1:
                # Extract consumer id from a line
                ID = log_line[consumer_id.start():consumer_id.end()]
            # For candlepin.log realated data only 
            if log_line.find("candlepin.log")!=-1 and ID!="":
                # Find data for a particular consumer id 
                if "--consumer-id" in sys.argv:
                    if log_line.find(id)!=-1:
                        if line.find("csid")!=-1:
                            csid = line[line.find("csid")+5:line.find("csid")+13]
                            if csid!="" and csid.find("]")==-1 and len(csid)==8:
                                if csid not in data: 
                                    # Adding csid as keys in dictionary i.e data
                                    data.update({csid:line})
                                else:
                                    # Adding message lines as valeus in dictionary i.e data related to their respective csid
                                    data[csid] = [data[csid],line]
                # Find all the data                     
                elif "--all" in sys.argv:
                    if line.find("csid")!=-1:
                            csid = line[line.find("csid")+5:line.find("csid")+13]
                            if csid!="" and csid.find("]")==-1 and len(csid)==8:
                                if csid not in data:
                                    # Adding csid as keys in dictionary i.e data
                                    data.update({csid:line})
                                else:
                                    # Adding message lines as valeus in dictionary i.e data related to their respective csid
                                    data[csid] = [data[csid],line]
    for key,value in data.items():
        print("-------------------------------------------------------------------------------------------------------")
        print("CSID ->",key,"\n \n")
        print(str(value).replace(", '","\n \n").strip("[").strip("'").strip("]"),"\n \n")
        print("-------------------------------------------------------------------------------------------------------")
    stop = timeit.default_timer()
    print(stop - start) 
else:
    print("Wrong choice of arguments, Please use --all or --consumer-id")