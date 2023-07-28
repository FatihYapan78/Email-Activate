from django.contrib import admin
from django.urls import path
from Appemailactivate.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login', Login, name='Login'),
    path('register', Register, name='Register'),
    path('activate/<str:uidb64>/<str:token>/', Activate,name='Activate')
]
