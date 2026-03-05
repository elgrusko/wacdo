from django.shortcuts import render
from accounts.decorators import login_required

@login_required
def home(request):
    return render(request, 'core/home.html')
