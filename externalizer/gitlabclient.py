import gitlab
from externalizer import dbclient
import json
import base64


propTemplatePath = 'gitlabclient.getallrepositoryfiles.templatepath'
propValuesFolder = 'gitlabclient.getallrepositoryfiles.valuesfolder'
propValuesFile = 'gitlabclient.getallrepositoryfiles.valuesfile'
propFileFormat = 'gitlabclient.getprojecttemplatevaluecontents.fileformat'

def getAllProjectsByKeyword(repoUrl, token, keyword, projectNamesOnly=True, returnNameSpaces=True):
    projects = list()
    
    with gitlab.Gitlab(url=repoUrl, private_token=token, api_version=4, ssl_verify=False) as gl:
        
        for project in gl.projects.list(search=keyword, get_all=True):
            if projectNamesOnly:
                parsedJSON = json.loads(json.loads(json.dumps(project.to_json())))
                if returnNameSpaces:
                    projects.append(parsedJSON['path_with_namespace'])
                else:
                    projects.append(parsedJSON['name'])
            else:
                projects.append(project.to_json())
        
    return projects
        

def getProjectTemplateValueContents(repoUrl, token, projectWithNamespaces, template_path, value_path, branch='develop'):
    with gitlab.Gitlab(url=repoUrl, private_token=token, api_version=4, ssl_verify=False) as gl:
        
        project = gl.projects.get(projectWithNamespaces)
        
        try:
            template_content = None
            value_content = None
            fileFormat = dbclient.getConfigValue(propFileFormat)
            
            if template_path and branch:
                f = project.files.get(file_path=template_path, ref=branch)
                template_content = base64.b64decode(f.content).decode(fileFormat).replace('\\n', '\n')
                
            if value_path and branch:
                v = project.files.get(file_path=value_path, ref=branch)
                value_content = base64.b64decode(v.content).decode(fileFormat).replace("\\n", "\n")
            
            return template_content, value_content
        except gitlab.exceptions.GitlabGetError:
            print('Error Gitlab GET! ')
            
    return '', ''


def getAllRepositoryFiles(repoUrl, token, envNameList, projectWithNamespaces, branch='develop'):
    template = ''
    confValues = list()
    for envName in envNameList:
        valueContent = None
        valuePath = dbclient.getConfigValue(propValuesFolder) + '/' + envName.strip().lower() + dbclient.getConfigValue(propValuesFile)
        if template:
            temp, valueContent = getProjectTemplateValueContents(repoUrl, token, projectWithNamespaces, '', valuePath, branch)
        else:
            templatePath = dbclient.getConfigValue(propTemplatePath)
            template, valueContent = getProjectTemplateValueContents(repoUrl, token, projectWithNamespaces, templatePath, valuePath, branch)
            
        if valueContent:
            confValues.append({
                'envName':envName,
                'values':valueContent
                })
            
    return template, confValues