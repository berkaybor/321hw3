from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='drugapp-home'),
    path('update_reaction_affinity/', views.update_reaction_affinity, name='update-reaction-affinity'),
    path('listDrugs/', views.listDrugs, name='listDrugs'),
    path('drug/<str:drugid>', views.showDrug, name='showDrug')
]
