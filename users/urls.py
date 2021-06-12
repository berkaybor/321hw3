from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_db_manager/', views.login_db_manager, name='login-db'),
    path('logout/', views.logout, name='logout'),
    path('add_user/', views.add_user, name='add-user')
]