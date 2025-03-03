from unittest import TestCase
from externalizer import propertyParser, dbclient

class propertyParserTestCase(TestCase):
    rawAppProperties = """#pop settings
pop.name=my-service
pop.version=0.0.1
server.port=7777

# popping
#  popping.floor.root=INFO
popping.floor.org.springframework=ERROR
popping.floor.sql=ERROR
popping.file=poplication.log
popping.path=/opt/poplications/goodservice/my-service/captainslogs
popping.pattern.file=%d{aaaaaa} %5p [${pop.name}, ${s.name:%X{ip}}:${r.port}, %X{Id}] ${xID:- } --- [%t] %-40.40blogger{5} : %mEx{5}

# create and drop tables and sequences, loads import.sql
lake.main.banner-mode=off
lake.jpa.bear.ddl-auto=none
lake.jpa.show-sql=false
lake.michael.deserialization.fail-on-unknown-properties=false

lake.data.work.return-body-on-create=true
lake.data.work.return-body-on-update=true
lake.data.work.basePath=/work/api

lake.jersey.poplication-path=/war

# athens settings
lake.outlet.url=driver:@host.myhost.yourhost.intern:3214/env
lake.outlet.username=myname
lake.outlet.password=youshallnotpassword"""


    rawTemplate = """#pop settings
pop.name=${POP_NAME}
pop.version=${POP_VERSION}
server.port=${SERVER_PORT}

# popping
#  popping.floor.root=${POPPING_FLOOR_ROOT}
popping.floor.org.springframework=${POPPING_FLOOR_ORG_SPRINGFRAMEWORK}
popping.floor.sql=${POPPING_FLOOR_SQL}
popping.file=${POPPING_FILE}
popping.path=${POPPING_PATH}
popping.pattern.file=${POPPING_PATTERN_FILE}"""


    rawConf = """POP_NAME=my-service
POP_VERSION=0.0.1
SERVER_PORT=7777
POPPING_FLOOR_ORG_SPRINGFRAMEWORK=ERROR
POPPING_FLOOR_SQL=ERROR
POPPING_FILE=poplication.log
POPPING_PATH=/opt/poplications/goodservice/my-service/captainslogs
POPPING_PATTERN_FILE=%d{aaaaaa} %5p [${pop.name}, ${s.name:%X{ip}}:${r.port}, %X{Id}] ${xID:- } --- [%t] %-40.40blogger{5} : %mEx{5}"""


    rawAppProp = """#pop settings
pop.name=my-service
pop.version=0.0.1
server.port=7777

# popping
popping.floor.org.springframework=ERROR
popping.floor.sql=ERROR
popping.file=poplication.log
popping.path=/opt/poplications/goodservice/my-service/captainslogs
popping.pattern.file=%d{aaaaaa} %5p [${pop.name}, ${s.name:%X{ip}}:${r.port}, %X{Id}] ${xID:- } --- [%t] %-40.40blogger{5} : %mEx{5}"""


    def test_parseProperty(self):
        propertyName, value = propertyParser.parseProperty('app.name=mbs-casa-service')
        assert propertyName == 'app.name'
        assert value == 'mbs-casa-service'
        

    def test_parsePropertyWithEmptyValue(self):
        propertyName, value = propertyParser.parseProperty('app.name=')
        assert propertyName == 'app.name'
        assert value == ''
        
        propertyName, value = propertyParser.parseProperty('app.name = ')
        assert propertyName == 'app.name'
        assert value == ''
        
        propertyName, value = propertyParser.parseProperty('app.name = \n')
        assert propertyName == 'app.name'
        assert value == ''
        

    def test_mapPropertyFile(self):
        #rawContent = '#app settings\napp.name=mbs-casa-service\napp.version=0.0.1\nserver.port=8111\n\n# logging\nlogging.level.root=INFO\nlogging.level.org.springframework=ERROR\nlogging.level.sql=ERROR\nlogging.file=application.log\nlogging.path=/opt/Applications/mbsservices/mbs-casa-service/logs'
        rawContent = '# test01\nTest-property02=test-service-property-valueUpdate02'
        mapList = propertyParser.mapPropertyFile(rawContent)
        #for propName, value in mapList:
        #    print(propName)
        assert len(mapList) == 1
        

    def test_parsePropertyRow(self):
        propRow = 'logging.path=/opt/myapps/myservice/mycasa/logs'
        name, value, disabled = propertyParser.parsePropertyRow(propRow)
        assert name == 'logging.path'
        assert value == '/opt/myapps/myservice/mycasa/logs'
        
        propRow = 'spring.jpa.show-sql=true'
        name, value, disabled = propertyParser.parsePropertyRow(propRow)
        assert name == 'spring.jpa.show-sql'
        assert value == 'true'
        
        propRow = 'rhsso.url=https://rhsso/mytoken/yourtoken/token?='
        name, value, disabled = propertyParser.parsePropertyRow(propRow)
        assert name == 'rhsso.url'
        assert value == 'https://rhsso/mytoken/yourtoken/token?='


    def test_createPropertyTemplate(self):
        result = propertyParser.createPropertyTemplate('Test-property01.prop01+test01!prop01~test01')
        assert result == 'TEST_PROPERTY01_PROP01_TEST01_PROP01_TEST01'
        

    def test_processRawApplicationProperties(self):
        propertyList, deactivatedPropertyList, tagList = propertyParser.processRawApplicationProperties(self.rawAppProperties, 'testService')
        
        assert len(propertyList) == 19
        assert len(deactivatedPropertyList) == 1
        assert len(tagList) == 4
        assert tagList[3] == 'Delphi settings'
        assert propertyList[18][1] == 'lake.outlet.password'
        assert deactivatedPropertyList[0][2] == 'INFO'
        

    def test_generateTemplateConfValue(self):
        propertyList, deactivatedPropertyList, tagList = propertyParser.processRawApplicationProperties(self.rawAppProperties)
        templateList, confValueList = propertyParser.generateTemplateConfValue(propertyList)
        
        assert len(templateList) == len(confValueList) == 19
        assert templateList[18] == 'lake.outlet.password=${LAKE_OUTLET_PASSWORD}'
        assert confValueList[18] == 'LAKE_OUTLET_PASSWORD=youshallnotpassword'
        
        templateList, confValueList = propertyParser.generateTemplateConfValue(propertyList, True)
        print(len(templateList))
        assert len(templateList) == 27  # 19 properties + 4 tags + 4 empty lines
        

    def test_seggregatePropertiesByTag(self):
        testList = list()
        testList.append(('service01', 'name01', 'value01', 'TAG01', True))
        testList.append(('service02', 'name02', 'value02', 'TAG02', True))
        testList.append(('service03', 'name03', 'value03', 'TAG03', True))
        testList.append(('service04', 'name04', 'value04', 'TAG02', True))
        testList.append(('service05', 'name05', 'value05', 'TAG01', True))
        testList.append(('service06', 'name06', 'value06', 'TAG03', True))
        testList.append(('service07', 'name07', 'value07', 'TAG01', True))
        result = propertyParser.seggregatePropertiesByTag(testList)
        assert len(result) == 3
        assert result[0][0] == 'TAG01'
        assert len(result[0][1]) == 3
        

    def test_generateApplicationProperties(self):
         propertyList, deactivatedPropertyList, tagList = propertyParser.processRawApplicationProperties(self.rawAppProperties)
         appPropList = propertyParser.generateApplicationProperties(propertyList)
         
         assert len(appPropList) == 19
         assert appPropList[18] == 'lake.outlet.password=youshallnotpassword'
         

    def test_mergeTemplateConfValues(self):
        result = propertyParser.mergeTemplateConfValues(self.rawTemplate.splitlines(), self.rawConf.splitlines())
        assert result == self.rawAppProp
 

    def test_generateExternalizerDataJSON(self):
        envServers = dbclient.getEnvServers()
        dataSource = list(("dataSource01", "dataSource02"))
        env = dbclient.getAllEnvironments()
        envList = list()
        for i in env:
            envList.append(i.envName)
            
        services = list(("service01", "service02", "service03"))
        result = propertyParser.generateExternalizerDataJSON(dataSource, envList, envServers, services)
        print(result)
        print(type(result['environments']))
        print(len(result['environments']))
        print(type(result['environments'][1]))
        print(result['environments'][1])
        
        assert result['environments'][0]['envName'] == ''
        assert len(result['environments'][0]['serverList']) == 0
        assert result['services'][0] == ''
        

    def test_generateExternalizationJSON(self):
        
        result = propertyParser.generateExternalizationJSON()


    def test_generatePropertyNameList(self):
        result = propertyParser.generatePropertyNameList(self.rawAppProperties.splitlines(), self.rawTemplate.splitlines())
        print(len(result))
        for i in result:
            print(i)


    def test_generateEnvServicePropertySearchValuesJSON(self):
        envServiceProperties = dbclient.getPropertiesByPropertyKeyword('liquibase', '', None, True)
        print(envServiceProperties)
        result = propertyParser.generateEnvServicePropertySearchValuesJSON(envServiceProperties)
        print(result)