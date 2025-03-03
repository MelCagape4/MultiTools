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

propTemplatePath = 'dataporterviews.propertiesparser.templatepath'
propProjectSearchPrefix = 'dataporterviews.propertiesparser.projectsearchprefix'
propValuesFolder = 'dataportviews.propertiesparser.valuesfolder'
propValuesFile = 'dataportviews.propertiesparser.valuesfile'
propPropertyFile = 'dataportviews.propertiesparser.propertyfile'

propertyDataSource = ('Services', 'Repositories')

def editor(request):
    if request.user.username: 
        print('editor()')
        # Renders the externalizer page.
        
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'dataporter.html',
            {
                'year':datetime.now().year,
            }
        )
    else:
       # REDIRECT TO LOGIN 
       return redirect('../toolsadmin/login/?next=/dataporter/')
   

def loadDataporterData(request):
    if request.user.username: 
        print('loadDataporterData()')
        
        envList = list()
        env = dbclient.getAllEnvironments()
        for i in env:
            envList.append(i.envName)
        
        payload = propertyParser.generateExternalizerDataJSON(propertyDataSource, envList, dbclient.getEnvServers(), dbclient.getAllServices(True, True))
        
        return HttpResponse(json.dumps(payload))
    else:
       # REDIRECT TO LOGIN 
       return redirect('../toolsadmin/login/?next=/dataporter/')


def propertiesParser(request):
    print(str(request.GET.get(paramSelectedServers, '')))
    
    env = str(request.GET.get(paramEnvironment, '')).strip()
    servers = str(request.GET.get(paramSelectedServers, '')).split(',')
    dataSource = str(request.GET.get(paramPropertyDataSource, ''))
    
    print("propertiesParser()..." + env)

    serviceList = list()
    failedServiceList = list()
    propertyList = list()
    saveServerServices = False
    
    if dataSource == propertyDataSource[0]: # Load from Services
        print('Loading from Services...')
        saveServerServices = True
        # LOOP THROUGH THE LIST OF SERVERS
        servers = dbclient.getServersByEnvironment(env, False, servers)
        for serverName, serverIP in servers:
            print(serverName + ' = ' + serverIP)
        
            # GET SERVER CREDENTIALS
            username, password = dbclient.getServerCredentials(None, serverIP)

            # EXECUTE PS -EF | GREP java 
            javaProcesses = sshclient.getHostAllJavaProcesses(serverIP, username, password).splitlines()
        
            # LOOP THROUGH EACH RESULT
            for javaproc in javaProcesses:
            
                # PARSE SERVICE PATH FROM -jar (check if -jar parameter has "/" which indicates a path of the jar. If none, check --spring.config.location= )
                basePath, serviceName, jar = sshclient.parsePSEFJavaRow(javaproc)
        
                # IF NO BASEPATH, PARSE DATA USING "--spring.config.location=" AS REFERENCE IF "-jar" DOES NOT CONTAIN BASE PATH AND/OR SERVICE NAME
                if not basePath:
                    basePath, serviceName, appProperties = sshclient.parsePSEFJavaRowFromConfigPath(javaproc)
                
                parseProperties = False
                if basePath and serviceName and jar:
                    # STORE PARSED SERVICE DATA IN A LIST
                    serviceList.append((serverName, serviceName, basePath, jar))
                    parseProperties = True
                else:
                    failedServiceList.append(javaproc)
        
                # ASYNC SEND LIST TO FRONTEND

                if parseProperties:
                    # PARSE SERVICE application.properties
                    propertyfile = dbclient.getConfigValue(propPropertyFile)
                    fullpath = basePath + serviceName + '/' + propertyfile
                    tag = ''
                    appProp = sshclient.getApplicationProperties(serverIP, username, password, fullpath).splitlines()
                    servicePropList = propertyParser.parseApplicationPropertiesToPropertyList(appProp, serviceName)
                    if len(servicePropList) > 0:
                        propertyList.extend(servicePropList)
                    
                # SEND LIST TO FRONTEND

    else: # Load from Repositories
        print('Loading from Repositories...')
        
        # GET USER REPOSITORY CREDENTIALS
        repoURL, privateToken = dbclient.getUserRepositoryCredentials(request.user.username)
        print(repoURL + ' , ' + privateToken)
        
        # LOOP THROUGH THE LIST OF REPOSITORIES
        projectSearchPrefix = dbclient.getConfigValue(propProjectSearchPrefix)
        repos = gitlabclient.getAllProjectsByKeyword(repoURL, privateToken, projectSearchPrefix)
        for repo in repos:
            print(repo)
            serviceName = ''
            externalizedIndex = repo.find(projectSearchPrefix)
            if externalizedIndex > -1:
                serviceName = repo[externalizedIndex + 13:len(repo)]
            else:
                serviceName = repo
                
            # GET TEMPLATE - application.properties
            # GET CONF VALUE - {env}.prop.value
            valuesFolder = dbclient.getConfigValue(propValuesFolder)
            valuesFile = dbclient.getConfigValue(propValuesFile)
            template, values = gitlabclient.getProjectTemplateValueContents(repoURL, privateToken, repo, dbclient.getConfigValue(propTemplatePath), valuesFolder + '/' + env.lower() + valuesFile)
            
            # GENERATE application.properties
            appProp = propertyParser.mergeTemplateConfValues(template.splitlines(), values.splitlines())
            print('TEMPLATE:\n' + template + ' \n\nVALUES:\n' + values + '\n' + serviceName)
            
            servicePropList = propertyParser.parseApplicationPropertiesToPropertyList(appProp.splitlines(), serviceName)
            print(servicePropList)
            if len(servicePropList) > 0:
                propertyList.extend(servicePropList)
                serviceList.append(('', serviceName, '', ''))
            else:
                failedServiceList.append(repo)
        
    print('SERVICES')
    # SAVE PARSED SERVICE DATA LIST TO DB
    for serverName, serviceName, basePath, jar in serviceList:
        dbclient.saveUpdateServerServices(serverName, serviceName, basePath, jar, saveServerServices)
        print(serverName + '  ' + serviceName + '  ' + basePath + '  ' + jar)
        

    print('PROPERTIES')
    # SAVE PARSED PROPERTIES LIST TO DB
    for serviceName, name, value, tag, enabled in propertyList:
        dbclient.savePropertyValue(env, serviceName, name, value, tag, enabled)
        print(env + ' == ' + serviceName + ' == ' + name + ' == ' + value + ' == ' + tag)

        
    print('FAILED SERVICES')
    for failed in failedServiceList:
        print(failed)

    return HttpResponse(json.dumps(serviceList))
