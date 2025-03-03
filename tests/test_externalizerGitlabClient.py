from unittest import TestCase
from externalizer import gitlabclient

class propertyParserTestCase(TestCase):
    
    url = ''
    token = ''
    searchPrefix = ''
    testRepo01 = ''
    testRepo02 = ''
    templatePath = ''
    valuePath = ''
    
    def test_getAllProjects(self):
        projects = gitlabclient.getAllProjectsByKeyword(self.url, self.token, self.searchPrefix)
        assert len(projects) > 0
        
        
        template, value = gitlabclient.getProjectTemplateValueContents(self.url, self.token, self.testRepo01, self.templatePath, self.valuePath)
        
        assert template != ''
        assert value != ''
        

    def test_getAllRepositoryFiles(self):
        envNamelist = list()
        envNamelist.extend(("DEV", "SIT", "SIT1", "SIT2", "UAT", "UAT-SKYNET"))
        template, values = gitlabclient.getAllRepositoryFiles(self.url, self.token, envNamelist, self.testRepo)
        print(template)
        for v in values:
            print('')
            print(v['envName'])
            for c in v['values']:
                print(c)
        