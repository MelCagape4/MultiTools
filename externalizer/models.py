from django.db import models
from logsearch.models import Service, Server
from django.contrib.auth.models import User


class Environment(models.Model):
    envID = models.AutoField(primary_key=True)
    envName = models.CharField(unique=True, max_length=30)
    
    class Meta:
        managed = True
        db_table = 'environments'
        verbose_name = "Environment"
        verbose_name_plural = "Environments"
        ordering = ["envID"]
        
    def __str__(self):
        return f"{self.envName}"
    

class Property(models.Model):
    propertyID = models.AutoField(primary_key=True)
    propertyName = models.CharField(unique=True, max_length=250)
    environmentSpecific = models.BooleanField(default=False)
    serviceSpecific = models.BooleanField(default=False)
    
    def _get_externalized_value(self):
        return str(self.propertyName).upper().replace('.', '_').replace('-', '_')
    
    externalizedValue = property(_get_externalized_value)
    
    class Meta:
        managed = True
        db_table = 'properties'
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ["-propertyName"]
        
    def __str__(self):
        return f"{self.propertyName}"
    

class EnvironmentProperty(models.Model):
    envpropID = models.AutoField(primary_key=True)
    environment = models.ForeignKey(Environment, on_delete=models.DO_NOTHING)
    prop = models.ForeignKey(Property, on_delete=models.DO_NOTHING)
    propertyValue = models.CharField(blank=True, max_length=1000)
    
    class Meta:
        managed = True
        db_table = 'env_property'
        verbose_name = "EnvProperty"
        verbose_name_plural = "EnvProperties"
        ordering = ["-prop"]
        
    def __str__(self):
        return f"{self.prop.propertyName} ({self.environment.envName})"
    

class ServiceProperty(models.Model):
    servicepropID = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    prop = models.ForeignKey(Property, on_delete=models.DO_NOTHING)
    propertyValue = models.CharField(blank=True, max_length=1000)
    
    class Meta:
        managed = True
        db_table = 'service_property'
        verbose_name = 'ServiceProperty'
        verbose_name_plural = 'ServiceProperties'
        ordering = ["prop"]
        
    def __str__(self):
        return f"{self.service.serviceName} ({self.prop.propertyName})"
    

class EnvServiceProperty(models.Model):
    envservicepropID = models.AutoField(primary_key=True)
    serviceProperty = models.ForeignKey(ServiceProperty, on_delete=models.DO_NOTHING)
    environment = models.ForeignKey(Environment, on_delete=models.DO_NOTHING)
    propertyValue = models.CharField(blank=True, max_length=1000)
    propertyTag = models.CharField(max_length=250, default='')
    propertyEnabled = models.BooleanField(default=True)
    
    class Meta:
        managed = True
        db_table = 'env_service_property'
        verbose_name = 'envServiceProperty'
        verbose_name_plural = 'envServiceProperties'
        ordering = ["-serviceProperty"]
        
    def __str__(self):
        return f"{self.serviceProperty.__str__()} ({self.environment.envName})"
    

class EnvServer(models.Model):
    envserverID = models.AutoField(primary_key=True)
    environment = models.ForeignKey(Environment, on_delete=models.DO_NOTHING)
    server = models.ForeignKey(Server, on_delete=models.DO_NOTHING)
    
    class Meta:
        managed = True
        db_table = 'env_server'
        verbose_name = 'envServer'
        verbose_name_plural = 'envServers'
        ordering = ["-server"]
        
    def __str__(self):
        return f"{self.environment.envName} - {self.server.serverName}"
    

class UserDetails(models.Model):
    userDetailsID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    repositoryURL = models.CharField(blank=True, max_length=1000)
    repositoryPrivateToken = models.CharField(blank=True, max_length=1000)
    
    class Meta:
        managed = True
        db_table = 'user_details'
        verbose_name = 'userDetails'
        verbose_name_plural = 'usersDetails'
        ordering = ["user"]
        
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
