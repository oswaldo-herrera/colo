from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'landing_app'

urlpatterns = [
    path('',views.landing_view, name='landing')
]
