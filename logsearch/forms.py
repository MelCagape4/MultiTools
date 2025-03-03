from django.forms import ModelForm

from logsearch.models import LogFile, Server, ServerService, ServerUser, Service, ServiceLogFile, ServerService, ServerUser, SysConfig


class ServerAdminForm(ModelForm):

    class Meta:
        model = Server
        fields = ["serverName", "serverIP", "description", "defaultUser", "defaultPassword", "lockoutCredentials"]
        

    def save(self, commit=True):
        return super().save(commit)
    

class ServiceAdminForm(ModelForm):
    
    class Meta:
        model = Service
        fields = ["serviceName", "description"]

    def save(self, commit=True):
        return super().save(commit)
    

class LogFileAdminForm(ModelForm):
                       
    class Meta:
        model = LogFile
        fields = ["logFilename", "description", "defaultPath"]
        
    def save(self, commit=True):
        return super().save(commit)
    

class ServiceLogFileAdminForm(ModelForm):
    
    class Meta:
        model = ServiceLogFile
        fields = ["service", "logfile", "filePath"]
        
    def save(self, commit=True):
        return super().save(commit)
    

class ServerServiceAdminForm(ModelForm):
    
    class Meta:
        model = ServerService
        fields = ["server", "service", "servicePath", "jarFile"]
        
    def save(self, commit=True):
        return super().save(commit)
    

class ServerUserAdminForm(ModelForm):
    
    class Meta:
        model = ServerUser
        fields = ["server", "user", "loginUser", "loginPassword", "lockoutCredentials"]
        
    def save(self, commit=True):
        return super().save(commit)
    

class SysConfigAdminForm(ModelForm):
    class Meta:
        model = SysConfig
        fields = ["configProperty", "configValue"]
        
    def save(self, commit=True):
        return super().save(commit)