def mapPropertyFile(rawContent):
    textOutput = rawContent.splitlines()
    
    keyValueList = []
    for row in textOutput:
        cleanRow = row.strip()
        if cleanRow and cleanRow != '' and cleanRow[0:1] != '#':
            propName, value = parseProperty(row)
            keyValueList.append((propName, value))
            
    return keyValueList


def parseProperty(row):
    cleanRow = row.strip()
    propertyName = None
    value = None
    equalIndex = cleanRow.find('=')
    rowLength = len(cleanRow)
    
    if equalIndex > 0:
        propertyName = cleanRow[0:equalIndex].strip()
        if rowLength == equalIndex + 1:
            value = ''
        else:
            value = cleanRow[equalIndex + 1:rowLength]

    return propertyName, value

#NOTES: 
#   - IF propRow starts with # and no '=' is found in the middle, it is recognized at a TAG
#   - IF propRow is an empty space, propertyName and propertyValue are empty strings and disabled is false
def parsePropertyRow(propRow):
   stripPropRow = propRow.strip()
   propertyName = ''
   propertyValue = ''
   disabled = False
   equalIndex = stripPropRow.find('=')
   if equalIndex > 0:
      propertyName = stripPropRow[0:equalIndex]
      propertyValue = stripPropRow[equalIndex + 1:len(stripPropRow)]
   else:
       propertyName = stripPropRow.replace('#', '')
       
   if propertyName[0:1] == '#' and propertyValue:
       disabled = True
       propertyName = propertyName[1:len(propertyName)].strip()
       
   return propertyName, propertyValue, disabled


def parseApplicationProperties(propertiesList, serviceName='', tag=''):
    propertyList = list()
    for i in propertiesList:
       name, value = parsePropertyRow(i)
       propertyList.append((serviceName, name, value, tag))


def parseApplicationPropertiesToPropertyList(propertiesSplitlines, serviceName=''):
    propertyList = list()
    tag = ''
    for prop in propertiesSplitlines:
        name, value, disabled = parsePropertyRow(prop)
        if name and value:
            propertyList.append((serviceName, name, value, tag, not disabled))
        elif name and not disabled:
            tag = name
            
    return propertyList


def processRawApplicationProperties(rawText, serviceName=''):
    lineSplitText = rawText.splitlines()
    propertyList = list()
    deactivatedPropertyList = list()
    tagList = list()
    tag = ''
    
    for prop in lineSplitText:
        stripProp = prop.strip()
        if stripProp:                                       # Check if stripProp IS NOT null or empty
            processProperty = False
            deactivatedProp = False
            if stripProp[0:1] == '#':                       # Check if first character is comment (#)
                stripProp = stripProp[1:len(stripProp)].strip()     # remove 
                if '=' in stripProp:                        # Check if commented line is a deactivated property
                    processProperty = True
                    deactivatedProp = True
                else:                                       # else add to tag
                    tag = stripProp
                    tagList.append(tag)
            else:                                           # else proceed to process property
                processProperty = True
                
            if processProperty:                             # Proceed with process property
                name, value, disabled = parsePropertyRow(stripProp)
                if name and value:
                    if deactivatedProp:
                       deactivatedPropertyList.append((serviceName, name, value, tag, not disabled))
                    else:
                        propertyList.append((serviceName, name, value, tag, not disabled))
                    
    return propertyList, deactivatedPropertyList, tagList


def generateTemplateConfValue(propertyList, seggregateTemplate=False):
    templateList = list()
    confValueList = list()
    if seggregateTemplate:
        seggregatedPropertyList = seggregatePropertiesByTag(propertyList)
        for tag, proplist in seggregatedPropertyList:
            templateList.append('# ' + tag)
            for serviceName, name, value, enabled in proplist:
                if enabled:
                    template = createPropertyTemplate(name)
                    templateList.append(name + '=${' + template + '}')
                    confValueList.append(template + '=' + value)
            templateList.append('')
    else:
        for serviceName, name, value, tag, enabled in propertyList:
            if enabled:
                template = createPropertyTemplate(name)
                templateList.append(name + '=${' + template + '}')
                confValueList.append(template + '=' + value)
        
    return templateList, confValueList



def seggregatePropertiesByTag(propertyList):
    seggregatedPropertyList = list()
    for serviceName, name, value, tag, enabled in propertyList:
        addNewSeggregatedList = True
        for j in seggregatedPropertyList:
            if j[0] == tag:
                j[1].append((serviceName, name.strip(), value.strip(), enabled))
                addNewSeggregatedList = False
            
        if addNewSeggregatedList:
            newList = list()
            newList.append((serviceName, name.strip(), value.strip(), enabled))
            seggregatedPropertyList.append((tag, newList))
            
    return seggregatedPropertyList


def generateApplicationProperties(propertyList, seggregateTemplate=False):
    appPropList = list()
    if seggregateTemplate:
        seggregatedPropList = seggregatePropertiesByTag(propertyList)
        for tag, proplist in seggregatedPropList:
            appPropList.append('# ' + tag)
            for serviceName, name, value, enabled in proplist:
                appPropValue = name + '=' + value
                if not enabled:
                    appPropValue = '# ' + appPropValue
                appPropList.append(appPropValue)
            appPropList.append('')
    else:
        for serviceName, name, value, tag, enabled in propertyList:
            appPropValue = name.strip() + '=' + value.strip()
            if not enabled:
                appPropValue = '# ' + appPropValue
            appPropList.append(appPropValue)
    return appPropList


def mergeTemplateConfValues(templateLines, confLines):
    mergedContent = ''
    value = ''
    template = ''
    nextLine = False
    for tline in templateLines:
        confValueFound = False
        stripLine = tline.strip()
        if '=' in stripLine:
            name, template, disabled = parsePropertyRow(stripLine)
            template = template.replace('${', '').replace('}', '')
            
            for cline in confLines:
                if template in cline:
                    template, value, tempFlag = parsePropertyRow(cline)
                    if nextLine:
                        mergedContent += '\n' 
                    else:
                        nextLine = True
                    mergedContent += tline.replace('${' + template + '}', value)
                    confValueFound = True
                    break
        else:
            if nextLine:
                mergedContent += '\n' 
            else:
                nextLine = True
            mergedContent += tline
                
    return mergedContent


def createPropertyTemplate(prop):
    return prop.upper().replace("-", "_").replace(".", "_").replace("!", "_").replace("~", "_").replace("+", "_")


def generateExternalizerDataJSON(dataSource, environments, envServers, services):
    envList = list()
    servicesList = list()
    
    envList.append({
            "envName": '', 
            "serverList": []
        })
    
    servicesList.append('')
    servicesList.extend(services)
    
    for env in environments:
        serverList = list()
        for server in envServers:
            if env == server.environment.envName:
                serverList.append(server.server.serverName)
                
        environmentJSON = {
            "envName": env, 
            "serverList": serverList
        }
        
        envList.append(environmentJSON)
     
    return {
            "propertyDataSource": dataSource,
            "environments": envList,
            "services": servicesList
        }

#====================================  STANDARD EXTERNALIZATION DATA FUNCTIONS  ==================================
def generateExternalizationJSON(propertyValueList, templateList, confValueList, searchValueList):
    return {
        'propertyValue': propertyValueList,
        'template': templateList,
        'confValues': confValueList,
        'searchValues': searchValueList
    }


def generatePropertyNameList(propertyValueList, templateList, activeOnly=True):
    propertyNameList = list()
    
    if propertyValueList:
        for pv in propertyValueList:
            propertyName, propertyValue, disabled = parsePropertyRow(pv)
        
            if propertyName not in propertyNameList:
                if (activeOnly and propertyValue and not disabled) or (not activeOnly and disabled):
                    propertyNameList.append(propertyName)
       
    if templateList:
        for t in templateList:
            propertyName, propertyValue, disabled = parsePropertyRow(t)
            if propertyName not in propertyNameList:
                if (activeOnly and propertyValue and not disabled) or (not activeOnly and disabled):
                    propertyNameList.append(propertyName)

    return propertyNameList


#NOTE: This function assumes that envServiceProperties contains many properties with multiple values
def generateEnvServicePropertySearchValuesJSON(envServiceProperties, includeValueSource=True):
    searchValues = list()
    for esp in envServiceProperties:
        addProperty = True
        for i in searchValues:
            if i['propertyName'] == esp.serviceProperty.prop.propertyName:
                noValueFound = True
                for sv in i['values']:
                    if esp.propertyValue == sv['value']:
                        if includeValueSource:
                            noEnvFound = True
                            for source in sv['sources']:
                                if source['envName'] == esp.environment.envName:
                                    source['serviceName'] += ',' + esp.serviceProperty.service.serviceName
                                    noEnvFound = False
                                    break
                                    
                            if noEnvFound:
                                sv['sources'].append({
                                    'envName':esp.environment.envName,
                                    'serviceName':esp.serviceProperty.service.serviceName
                                    })
                        noValueFound = False

                if noValueFound:
                    sources = list()
                    if includeValueSource:
                        sources.append({
                            'envName':esp.environment.envName,
                            'serviceName':esp.serviceProperty.service.serviceName
                            })
                    i['values'].append({
                        'value':esp.propertyValue,
                        'sources':sources
                        })
                
                addProperty = False
                break
            
        if addProperty:
            sources = list()
            if includeValueSource:
                sources.append({
                    'envName':esp.environment.envName,
                    'serviceName':esp.serviceProperty.service.serviceName
                    })
            newValues = list()
            newValues.append({
                'value':esp.propertyValue,
                'sources':sources
                })
            searchValues.append({
                'propertyName':esp.serviceProperty.prop.propertyName,
                'values':newValues
                })
    
    return searchValues