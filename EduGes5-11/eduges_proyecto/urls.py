from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from home.views import home, CustomLoginView

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sistema/', include('home.urls')),
]
