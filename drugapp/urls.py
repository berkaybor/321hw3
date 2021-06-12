from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='drugapp-home'),
    path('listDrugs/', views.listDrugs, name='listDrugs'),
    path('drug/<str:drugid>', views.showDrug, name='showDrug')
]
