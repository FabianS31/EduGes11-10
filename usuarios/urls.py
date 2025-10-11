from django.shortcuts import render
from django.contrib.auth.views import LoginView

# Login personalizado
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return self.get_redirect_url() or '/'

# Vistas de las páginas
def home(request):
    return render(request, 'home.html')

def registros(request):
    return render(request, 'registros.html')

def pagos(request):
    return render(request, 'pagos.html')

def general(request):
    return render(request, 'general.html')
