import CloudStack
import json,ast
import sys
api = ''
apikey = ''
secret = ''
cloudstack = CloudStack.Client(api, apikey, secret)
clusterid=str(sys.argv[1])
request= {'listall':'true','type':'Routing','clusterid':clusterid}

listhosts=cloudstack.listHosts(request)
data=[]
for vm in listhosts:
    output={'data':data}
    data.append({'{#ID}':vm['id'],'{#NAME}':vm['name']})
#print data
output={'data':data}
y=json.dumps(output)
print y
