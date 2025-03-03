"""
WebAppCollection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from logsearch import logSearchViews
from morningcheck import morningCheckViews
from externalizer import externalizerViews
from dataporter import dataporterViews
from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings

admin.site.site_title = "Tools Collection Site Admin"
admin.site.site_header = "Tools Collection Administration"
admin.site.index_title = "Site Administration"

urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('toolsadmin/', admin.site.urls, name='mainlogin'),
    
    # morningcheck URLS
    path('morningcheck/', morningCheckViews.morningcheck, name='morningcheck'),

    # logsearch URLs
    path('logsearch/', logSearchViews.logsearch, name='logsearch'),
    path('logsearch/callsearch/', logSearchViews.callsearch, name='callsearchlogs'),
    path('logsearch/onselectedhostchange/', logSearchViews.onselectedhostchange, name='logsearchhostchange'),
    
    # externalizer URLs
    path('externalizer/', externalizerViews.editor, name='externalizer'),
    path('externalizer/search/properties', externalizerViews.searchProperty, name='searchproperties'),
    path('externalizer/data', externalizerViews.loadExternalizerData, name='externalizerdata'),
    path('externalizer/externalize', externalizerViews.externalizeData, name='externalizedata'),
    

    # dataporter URLs
    path('dataporter/', dataporterViews.editor, name='dataporter'),
    path('dataporter/data', dataporterViews.loadDataporterData, name='externalizerdata'),
    path('dataporter/parser/properties', dataporterViews.propertiesParser, name='parser'),
    
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

