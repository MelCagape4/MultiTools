from django.db import models
from django.contrib.auth.models import User

class Server(models.Model):
    serverID = models.AutoField(primary_key=True)
    serverName = models.CharField(unique=True, max_length=30)
    serverIP = models.CharField(unique=True, max_length=20)
    description = models.CharField(blank=True, max_length=300)
    defaultUser = models.CharField(blank=True, max_length=30)
    defaultPassword = models.CharField(blank=True, max_length=30)
    lockoutCredentials = models.BooleanField(default=False)
    
    class Meta:
        managed = True
        db_table = 'servers'
        verbose_name = "Server"
        verbose_name_plural = "Servers"
        ordering = ["-serverIP"]
    
    def __str__(self):
        return f"{self.serverName}"
    

class Service(models.Model):
    serviceID = models.AutoField(primary_key=True)
    serviceName = models.CharField(unique=True, max_length=50)
    description = models.CharField(blank=True, max_length=300)
    
    class Meta:
        managed = True
        db_table = 'services'
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["-serviceName"]
    
    def __str__(self):
        return f"{self.serviceName}"
    

class LogFile(models.Model):
    logfileID = models.AutoField(primary_key=True)
    logFilename = models.CharField(unique=True, max_length=50)
    description = models.CharField(blank=True, max_length=300)
    defaultPath = models.CharField(max_length=200)
    
    class Meta:
        managed = True
        db_table = 'logfiles'
        verbose_name = "LogFile"
        verbose_name_plural = "LogFiles"
        ordering = ["-logFilename"]
    
    def __str__(self):
        return f"{self.logFilename}"
    

class ServiceLogFile(models.Model):
    serviceLogfileID = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    logfile = models.ForeignKey(LogFile, on_delete=models.DO_NOTHING)
    filePath = models.CharField(blank=True, max_length=200)
    
    class Meta:
        managed = True
        db_table = 'service_logfiles'
        unique_together = (('service', 'logfile'),)
        ordering = ["-service"]
        
    def __str__(self):
        return f"{self.service.serviceName} ({self.logfile.logFilename})"


class ServerService(models.Model):
    serverserviceID = models.AutoField(primary_key=True)
    server = models.ForeignKey(Server, on_delete=models.DO_NOTHING)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    servicePath = models.CharField(blank=True, max_length=200)
    jarFile = models.CharField(blank=True, max_length=50)
    
    class Meta:
        managed = True
        db_table = 'server_services'
        unique_together = (('server', 'service'),)
        ordering = ["-server"]
        
    def __str__(self):
        return f"{self.server.serverName} ({self.service.serviceName})"
    

class ServerUser(models.Model):
    serveruserID = models.AutoField(primary_key=True)
    server = models.ForeignKey(Server, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    loginUser = models.CharField(max_length=50)
    loginPassword = models.CharField(max_length=50)
    lockoutCredentials = models.BooleanField(default=False)
    
    class Meta:
        managed = True
        db_table = 'server_users'
        unique_together = (('server', 'user'),)
        ordering = ["-server"]
        
    def __str__(self):
        return f"{self.server.serverName} ({self.user.get_username()})"
    

class SysConfig(models.Model):
    configID = models.AutoField(primary_key=True)
    configProperty = models.CharField(unique=True, max_length=100)
    configValue = models.CharField(max_length=500)
    
    class Meta:
        managed = True
        db_table = 'sys_config'
        verbose_name = 'configuration'
        verbose_name_plural = 'configurations'
        ordering = ["configProperty"]
        
    def __str__(self):
        return f"{self.configProperty} = {self.configValue}"