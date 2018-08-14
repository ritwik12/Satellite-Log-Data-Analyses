import sys
id = set([])
views = ""
lines = tuple(open("production.log", 'r'))
file =open("analyse.json","w") 
for i in range(1, len(lines)):
	line = lines[i]
	if line.find("Views")!=-1:
		id = line[20:28]
		log_time = line[12:19]
		totaltime = line[line.find("in")+2: line.find("in")+7]
		Views = line[line.find("Views")+6: line.find("Views")+13]
		ActiveRecord = line[line.find("ActiveRecord")+14: line.find("ActiveRecord")+19]
		# Store data in JSON format to be indexed in ElasticSearch
		analyse_data = "ID:"+id+" "+"Time:"+log_time+" "+"Totaltime:"+totaltime+" "+"Views:"+Views+" "+"ActiveRecord:"+ActiveRecord
		if "json" in sys.argv:
			json = """{"index":{"_index":"production","_id":"""+'"'+str(i-1)+'"'+"""}} \n {"ID ":"""+'"'+id+'"'+""","Time":"""+'"'+log_time+'"'+""","Totaltime":"""+'"'+totaltime+'"'+""","Views":"""+'"'+Views+'"'+""","ActiveRecord":"""+'"'+ActiveRecord+'"'+"}"+"\n"
            		# Write JSON formatted data to analyse.json
			file.write(json)
		else:
			print("---------------------------------------------------------------------------------------------------------")
			print(analyse_data)
			print("---------------------------------------------------------------------------------------------------------")
