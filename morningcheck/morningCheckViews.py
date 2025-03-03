from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

def morningcheck(request):
    """Renders the home page."""
    
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'morningcheck.html',
        {
            'year':datetime.now().year,
        }
    )