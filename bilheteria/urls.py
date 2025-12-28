from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('filme/<int:filme_id>/', views.filme_detalhes, name='filme_detalhes'),
    path('sessao/<int:sessao_id>/', views.sessao_detalhes, name='sessao_detalhes'),
    path('compra_sucesso/', views.compra_sucesso, name='compra_sucesso'),
]
