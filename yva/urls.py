from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('orientation/', views.orientation_test, name='orientation'),
    path('formations/', views.mini_formation, name='formations'),
    path('generate-doc/', views.generate_doc, name='generate_doc'),
    path('conseiller/', views.conseiller_virtuel, name='conseiller'),

]
