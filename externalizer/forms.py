from django.forms import ModelForm

from externalizer.models import EnvServer, Environment, Property, EnvironmentProperty, ServiceProperty, EnvServiceProperty, UserDetails

class EnvironmentAdminForm(ModelForm):
    
    class Meta:
        model = Environment
        fields = ["envName"]
        
    def save(self, commit=True):
        return super().save(commit)
    

class PropertyAdminForm(ModelForm):
    class Meta:
        model = Property
        fields = ["propertyName", "environmentSpecific", "serviceSpecific"]
        
    def save(self, commit=True):
        return super().save(commit)
    

class EnvironmentPropertyAdminForm(ModelForm):
    
    class Meta:
        model = EnvironmentProperty
        fields = ["environment", "prop", "propertyValue"]
        
    def save(self, commit=True):
        return super().save(commit)
    

class ServicePropertyAdminForm(ModelForm):
    class Meta:
        model = ServiceProperty
        fields = ["service", "prop", "propertyValue"]
        
    def save(self, commit=True):
        return super().save(commit)

        
class EnvServicePropertyAdminForm(ModelForm):
    class Meta:
        model = EnvServiceProperty
        fields = ["serviceProperty", "environment", "propertyValue", "propertyTag", "propertyEnabled"]
        
    def save(self, commit=True):
        return super().save(commit)

    
class EnvServerAdminForm(ModelForm):
    class Meta:
        model = EnvServer
        fields = ["environment", "server"]
        
    def save(self, commit=True):
        return super().save(commit)
    

class UserDetailsAdminForm(ModelForm):
    class Meta:
        model = UserDetails
        fields = ["user", "repositoryURL", "repositoryPrivateToken"]
        
    def save(self, commit=True):
        return super().save(commit)
    

