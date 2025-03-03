from externalizer import dbclient
from externalizer.models import Environment, Property, ServiceProperty, EnvironmentProperty, EnvServiceProperty
from logsearch.models import Service
from unittest import TestCase

class DbClientTestCase(TestCase):
    value = ''


    #
    #  PROPERTY VALUE PRIORITY: env_service_property -> env_property -> service_property
    #
    def test_getProperty(self):
        envServiceProp = dbclient.getProperty('TEST01', 'test-service01', 'Test-property01')
        assert isinstance(envServiceProp, EnvServiceProperty)
        
        serviceProp = dbclient.getProperty(None, 'test-service02', 'Test-property02')
        assert isinstance(serviceProp, ServiceProperty)
        
        envProp = dbclient.getProperty('TEST01', None, 'Test-property03')
        assert isinstance(envProp, EnvironmentProperty)
        
        with self.assertRaises(ValueError):  # NULL property name raises a ValueError
            envProp = dbclient.getProperty(None, None, None)
            
        with self.assertRaises(ValueError):  # NULL environment name and service name raises a ValueError
            envProp = dbclient.getProperty(None, None, 'Test-property03')
            
        with self.assertRaises(Property.DoesNotExist):  # Non-existing Property raises a Property.DoesNotExist
            envProp = dbclient.getProperty('TEST01', None, 'Test-property05')
            
        with self.assertRaises(Service.DoesNotExist):  # Non-existing Service raises a Service.DoesNotExist
            envProp = dbclient.getProperty('TEST04', 'test-service04', 'Test-property01')
            
        with self.assertRaises(Environment.DoesNotExist):  # Non-existing Environment raises a Environment.DoesNotExist
            envProp = dbclient.getProperty('TEST04', 'test-service01', 'Test-property01')
        

    def test_savePropertyValueToEnvServiceProperty(self):
        self.value = 'test-env-property-valueUpdate01'
        result = dbclient.savePropertyValue('TEST01', 'test-service01', 'Test-property01', self.value)
        assert isinstance(result, EnvServiceProperty)
        

    def test_savePropertyValueToServiceProperty(self):
        self.value = 'test-service-property-valueUpdate02'
        result = dbclient.savePropertyValue(None, 'test-service02', 'Test-property02', self.value)
        assert isinstance(result, ServiceProperty)
        
        
    def test_savePropertyValueToEnvProperty(self):
        self.value = 'test-env-property-valueUpdate03'
        result = dbclient.savePropertyValue('TEST01', None, 'Test-property03', self.value)
        assert isinstance(result, EnvironmentProperty)


    def test_savePropertyValueWithEnvironmentSpecificProperty(self):
        self.value = 'INFO'
        result = dbclient.savePropertyValue('TEST01', None, 'Test-property04', self.value)
        assert isinstance(result, EnvironmentProperty)
        assert result.environment.envName == 'TEST01'
        assert result.prop.propertyName == 'Test-property04'
        assert result.propertyValue == 'INFO'
        

    def test_savePropertyValueWithEnvServiceProperty(self):
        self.value = 'test-service01-property01-value03'
        result = dbclient.savePropertyValue('TEST01', 'test-service01', 'Test-property01', self.value)
        assert isinstance(result, EnvServiceProperty)
        assert result.environment.envName == 'TEST01'
        assert result.serviceProperty.service.serviceName == 'test-service01'
        assert result.serviceProperty.prop.propertyName == 'Test-property01'
        assert result.propertyValue == 'test-service01-property01-value03'
        

    def test_getEnvServicePropertiesByProperty(self):
        result = dbclient.getEnvServicePropertiesByProperty('Test-property02')
            
        assert len(result) == 1


    # ENVIRONMENTS
    def test_getAllEnvironments(self):
        result = dbclient.getAllEnvironments()
        assert not result.filter(envName__istartswith='test').exists()
        
        result = dbclient.getAllEnvironments(False)
        assert result.filter(envName__istartswith='test').exists()
        

    def test_getServersByEnvironment(self):
        result = dbclient.getServersByEnvironment('TEST01')
        assert len(result) == 2
        for i in result:
            assert len(i) == 2
            
        result = dbclient.getServersByEnvironment('TEST01', True)
        assert len(result) == 2
        for i in result:
            assert isinstance(i, str)
            
        serverNames = list()
        serverNames.append('test-server-02')
        result = dbclient.getServersByEnvironment('TEST01', True, serverNames)
        assert len(result) == 1
        for i in result:
            assert isinstance(i, str)
            assert i == 'test-server-02'
            

    def test_getEnvServers(self):
        result = dbclient.getEnvServers(envName='TEST01', excludeTests=False)
        assert len(result) == 2
        

    # SERVICES
    def test_getAllServices(self):
        result = dbclient.getAllServices()
        assert not result.filter(serviceName__istartswith='test-').exists()
        
        result = dbclient.getAllServices(False)
        assert result.filter(serviceName__istartswith='test-').exists()
        
        result = dbclient.getAllServices(False, True)
        assert isinstance(result[0], str)
        
        result = dbclient.getAllServices(True, True)
        #assert isinstance(result[0], str)


    def test_getEnvironmentServiceProperties(self):
        result = dbclient.getEnvironmentServiceProperties('TEST01', 'test-service01')
        assert len(result) == 3
        assert result[0].serviceProperty.prop.propertyName == 'Test-property01'
            

    def test_getPropertiesByPropertyKeyword(self):
        result = dbclient.getPropertiesByPropertyKeyword('Test-property', 'TEST01')
        assert isinstance(result[0], EnvironmentProperty)
        
        result = dbclient.getPropertiesByPropertyKeyword('Test-property', None, 'test-service01')
        assert isinstance(result[0], ServiceProperty)
        
        result = dbclient.getPropertiesByPropertyKeyword('Test-property', 'TEST01', 'test-service01')
        assert isinstance(result[0], EnvServiceProperty)
        
        result = dbclient.getPropertiesByPropertyKeyword('Test-property', None, 'test-service01', True)
        assert isinstance(result[0], EnvServiceProperty)
        
        result = dbclient.getPropertiesByPropertyKeyword('Test-property', 'TEST01', None, True)
        assert isinstance(result[0], EnvServiceProperty)


    def test_getPropertiesContainingKeyword(self):
        result = dbclient.getPropertiesContainingKeyword('Test-property')
        assert len(result) == 4
        assert isinstance(result[0], Property)
        
        result = dbclient.getPropertiesContainingKeyword('Test-property', False)
        assert len(result) == 4
        assert isinstance(result[0], dict)
        

    def test_savePropertyFile(self):
        #rawContent = '#app settings\napp.name=mbs-casa-service\napp.version=0.0.1\nserver.port=8111\n\n# logging\nlogging.level.root=INFO\nlogging.level.org.springframework=ERROR\nlogging.level.sql=ERROR\nlogging.file=application.log\nlogging.path=/opt/Applications/mbsservices/mbs-casa-service/logs'
        rawContent = '# test01\nTest-property01=test-service01-property01-value01\n\n# test02\nTest-property02=test-service01-property02-value02\nTest-property03=test-service01-property03-value03'
        savedList, failedList = dbclient.savePropertyFile('TEST01', 'test-service01', rawContent)
        assert len(savedList) == 3
        assert len(failedList) == 0
        
        rawContent = '# test01\nTest-property02=test-service-property-valueUpdate02'
        savedList, failedList = dbclient.savePropertyFile(None, 'test-service02', rawContent)
        assert len(savedList) == 1
        assert len(failedList) == 0
 