from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usuarios.views import home, registros, pagos, general, CustomLoginView

urlpatterns = [
    path('', home, name='home'),
    path('alta/', registros, name='registros'),
    path('pagos/', pagos, name='pagos'),
    path('general/', general, name='general'),
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('alumnos/', include('alumnos.urls')), 
]
