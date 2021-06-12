from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='drugapp-home'),
    path('update_reaction_affinity/', views.update_reaction_affinity, name='update-reaction-affinity'),
    path('delete_drug/', views.delete_drug, name='delete-drug'),
    path('delete_protein/', views.delete_protein, name='delete-protein'),
    path('listDrugs/', views.listDrugs, name='listDrugs'),
    path('drug/<str:drugid>', views.showDrug, name='showDrug'),
    path('drug_interactions/', views.drug_interactions, name='drug-interactions'),
    path('side_effects/', views.view_side_effects, name='side-effects'),
    path('interacting_targets/', views.view_interacting_targets, name='interacting-targets'),
]
