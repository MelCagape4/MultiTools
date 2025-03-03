from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from externalizer import dbclient, propertyParser, gitlabclient
from logsearch import sshclient
import json

paramEnvironment = 'environment'
paramSelectedServers = 'servers'
paramSelectedService = 'service'
paramSearchKeyword = 'keyword'
paramPropertyDataSource = 'propertyDataSource'

propertyDataSource = ('Services', 'Repositories')

def editor(request):
    if request.user.username: 
        print('editor()')
        # Renders the externalizer page.
        
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'externalizer.html',
            {
                'year':datetime.now().year,
            }
        )
    else:
       # REDIRECT TO LOGIN 
       return redirect('../toolsadmin/login/?next=/externalizer/')
   

def searchProperty(request):
    if request.user.username: 
        if request.method == 'GET':
            env = request.GET.get(paramEnvironment, '')
            selectedService = request.GET.get(paramSelectedService, '')
            searchKeyword = request.GET.get(paramSearchKeyword, '')
            searchProperties = dbclient.getPropertiesByPropertyKeyword(searchKeyword, env, selectedService, True)
            propertyList = list()
            print(searchKeyword + '  ' + env + '  ' + selectedService)
            for i in searchProperties:
                propertyList.append((i.serviceProperty.service.serviceName, i.serviceProperty.prop.propertyName, i.propertyValue, i.serviceProperty.service.serviceName + '(' + i.environment.envName + ')', i.propertyEnabled))
                
            appPropList = propertyParser.generateApplicationProperties(propertyList, True)
            templateList, confValueList = propertyParser.generateTemplateConfValue(propertyList, True)
            payload = {
                'propertyValue': json.loads(json.dumps(appPropList)),
                'template': json.loads(json.dumps(templateList)),
                'confValue': json.loads(json.dumps(confValueList))
            }
            return HttpResponse(json.dumps(payload))
        return HttpResponse('')
    else:
       # REDIRECT TO LOGIN 
       return redirect('../toolsadmin/login/?next=/externalizer/')


def loadExternalizerData(request):
    if request.user.username: 
        print('loadExternalizerData()')
        
        envList = list()
        env = dbclient.getAllEnvironments()
        for i in env:
            envList.append(i.envName)
        
        payload = propertyParser.generateExternalizerDataJSON(propertyDataSource, envList, dbclient.getEnvServers(), dbclient.getAllServices(True, True))
        
        return HttpResponse(json.dumps(payload))
    else:
       # REDIRECT TO LOGIN 
       return redirect('../toolsadmin/login/?next=/externalizer/')


def externalizeData(request):
    if request.user.username: 
        print('externalizeData()...')
        propertyValueList = None
        selectedService = ''

        if request.method == 'POST': # POST request for "Externalize Property-Value"
            print('POST Request')
            print(request.POST)
            propertyValueList = request.POST.get('propval')
            selectedService = request.POST.get(paramSelectedService, '')
        
        envNamelist = list()
        for env in dbclient.getAllEnvironments():
            envNamelist.append(env.envName)

        repoURL, privateToken = dbclient.getUserRepositoryCredentials(request.user.username)
        repos = gitlabclient.getAllProjectsByKeyword(repoURL, privateToken, selectedService)
        
        templateList, confValueList = gitlabclient.getAllRepositoryFiles(repoURL, privateToken, envNamelist, repos[0])
        propertyNameList = propertyParser.generatePropertyNameList(propertyValueList.splitlines(), '')
        envServiceProperties = dbclient.getEnvServicePropertiesByPropertyNameList(propertyNameList)
        searchValueList = propertyParser.generateEnvServicePropertySearchValuesJSON(envServiceProperties)
        
        return HttpResponse(json.dumps(propertyParser.generateExternalizationJSON(propertyValueList, templateList, confValueList, searchValueList)))
    else:
       # REDIRECT TO LOGIN 
       return redirect('../toolsadmin/login/?next=/externalizer/')
