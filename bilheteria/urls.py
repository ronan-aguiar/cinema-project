from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('filme/<int:filme_id>/', views.filme_detalhes, name='filme_detalhes'),
    path('sessao/<int:sessao_id>/', views.sessao_detalhes, name='sessao_detalhes'),
    path('compra_sucesso/', views.compra_sucesso, name='compra_sucesso'),
]
