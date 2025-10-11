from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def registros(request):
    return render(request, 'registros.html')

@login_required
def pagos(request):
    return render(request, 'pagos.html')

@login_required
def general(request):
    return render(request, 'general.html')
