from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import json
import logsearch.dbclient as db
import logsearch.sshclient as ssh

paramSelectedIds = 'selectedIds'
paramFromDate = 'fromDate'
paramToDate = 'toDate'
paramKeyword = 'keyWord'
paramTargetLog = 'targetLog'
paramHostIP = 'hostIP'
paramIpAddress = 'ipAddress'

servicesList = list()
targetlog = list()
hosts = None
logs = list()

def logsearch(request):
    print(request.user.username)
    print(db.getUsers())
            
    if request.user.username:
      # Renders the logsearch page.
    
      hosts = db.getHostsJSON()
      print(hosts)
      
      services = db.getServicesJSON()
      
      targetlog = db.getLogfilesJSON()
      
      print(ssh.getDateYearMonth('2024-06-15'))
      
    
      assert isinstance(request, HttpRequest)
      return render(
        request,
        'logsearch.html',
        {
            'logfiles': targetlog,
            'hosts': hosts,
            'services': services,
            'year':datetime.now().year,
        }
    )
    else:
       # REDIRECT TO LOGIN 
       return redirect('../toolsadmin/login/?next=/logsearch/')
    
    

def callsearch(request):
    print('callsearch()... ');
    selectedIds = str(request.GET.get(paramSelectedIds, ''))
    ids = selectedIds[0:len(selectedIds) - 1].split(',')
        
    fromDate = str(request.GET.get(paramFromDate, ''))
    toDate = str(request.GET.get(paramToDate, ''))
    
    keyword = str(request.GET.get(paramKeyword, ''))
    targetLog, defaultPath = db.getLogFilenameAndPathById(request.GET.get(paramTargetLog, ''))
    print(targetLog)
    
    ipAddress = str(request.GET.get(paramIpAddress, ''))
    user, password = db.getServerCredentials(ipAddress, request.user.username)
    
    logs = list()
    print(ids)
    
    for i in ids:
      service = db.getServiceById(i)
      if service:
        for service_id, service_name, service_path, description in service:
          print('searching logs for ' + service_name)
          logResult = ssh.searchServiceLogs(keyword, fromDate, toDate, str(service_path) + str(service_name) + defaultPath, targetLog, ipAddress, user, password)
          loglines = logResult.splitlines()
          for log in loglines:
             logs.append(ssh.parseLogToJson(log, targetLog))
    
    data = json.dumps(logs)
    
    return HttpResponse(data)
    
def onselectedhostchange(request):
    print('onselectedhostchange() ')
    services = db.getAllServices()
    user, password = db.getServerCredentials(request.GET.get(paramHostIP, ''), request.user.username)
    print(request.GET.get(paramHostIP, ''))
    print(user)
    print(password)
    javaProcesses = ssh.getHostAllJavaProcesses(request.GET.get(paramHostIP, ''), user, password)

    availableServices = list()
    if isinstance(javaProcesses, Exception):
       db.lockUserCredentials(request.GET.get(paramHostIP, ''), request.user.username)
       print('Failed to connect to ' + request.GET.get(paramHostIP, '') + '!')
    else:
        for x, y, z, a in services:
            fullPath = z + y
            if fullPath in javaProcesses:
                service = {
                   "serviceId": str(x),
                   "serviceName": str(y)
                   }
                availableServices.append(service)
       

    data = json.dumps(availableServices)
    
    return HttpResponse(data)
    

