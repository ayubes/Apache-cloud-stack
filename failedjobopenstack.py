import CloudStack
import json,ast
import time
import dateutil.parser as dp

api = ''
apikey = ''
secret = ''
cloudstack = CloudStack.Client(api, apikey, secret)

request= {'listall': 'true'}

listasync=cloudstack.listAsyncJobs(request)
#Start,The Bug 41 is in TFS
i=0
for job in listasync:
    if ( job['jobstatus'] == 2 ):

         if  'cmd' in listasync and  job['cmd'].endswith('VmWorkStart'):
                accountid = job['accountid']
                jobid=str(job['jobid'])
                date=job['created']
                parsed_t = dp.parse(date)
                t_in_seconds1 = int(parsed_t.strftime('%s'))
                for state in listasync:
                   if  state['accountid'] == accountid :
                       date2=state['created']
                       parsed_t = dp.parse(date2)
                       t_in_seconds2 = int(parsed_t.strftime('%s'))
                       if( t_in_seconds1 - t_in_seconds2 < 50  and state['cmd'].endswith('DeployVMCmd')):
                            listasync[i]['jobstatus']=1
    i += 1
#End Bug 41
data=[]
x = json.dumps(listasync)
for state in listasync:
    accountid = state ['accountid']
    status = state['jobstatus']
   # Remove Status was 0 or Pendding for id 
    if status != '0' and accountid !='id' :
        data.append(state['jobstatus'])

output = {'pending':data.count(0),'error':data.count(2)}
outputs = {'data':output}
result=json.dumps(outputs)
print result
