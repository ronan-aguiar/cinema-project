from django.shortcuts import render, get_object_or_404, redirect
from .models import Filme, Sessao, Ingresso
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from django.contrib.auth.models import User

@login_required
def index(request):
    filmes = Filme.objects.all()
    return render(request, 'bilheteria/index.html', {'filmes': filmes})

@login_required
def filme_detalhes(request, filme_id):
    filme = get_object_or_404(Filme, pk=filme_id)
    sessoes = Sessao.objects.filter(filme=filme).order_by('horario')
    return render(request, 'bilheteria/filme_detalhes.html', {'filme': filme, 'sessoes': sessoes})

@login_required
def sessao_detalhes(request, sessao_id):
    sessao = get_object_or_404(Sessao, pk=sessao_id)
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo_ingresso')
        forma_pagamento = 'DINHEIRO'  # Por enquanto fixo
        
        # Lógica de preços
        preco = 0
        if tipo == 'INTEIRA':
            preco = 16.00
        elif tipo == 'MEIA':
            preco = 8.00
        # ESTUDANTE e CORTESIA continuam 0
        
        # Registra o vendedor
        ingresso = Ingresso.objects.create(
            sessao=sessao,
            tipo=tipo,
            valor_pago=preco,
            forma_pagamento=forma_pagamento,
            vendedor=request.user
        )
        return redirect('compra_sucesso')

    return render(request, 'bilheteria/sessao_detalhes.html', {'sessao': sessao})

@login_required
def compra_sucesso(request):
    return render(request, 'bilheteria/compra_sucesso.html')
@login_required
def relatorios(request):
    sessao_id = request.GET.get('sessao_id')
    sessoes_lista = Sessao.objects.select_related('filme').order_by('-horario')[:50] # Últimas 50 sessões
    
    sessao_selecionada = None
    vendas_sessao = None
    metricas = {}

    if sessao_id:
        sessao_selecionada = get_object_or_404(Sessao, pk=sessao_id)
        vendas_sessao = Ingresso.objects.filter(sessao=sessao_selecionada)
        
        from django.db.models import Q
        resumo = vendas_sessao.aggregate(
            qtd_inteira=Count('id', filter=Q(tipo='INTEIRA')),
            qtd_meia=Count('id', filter=Q(tipo='MEIA')),
            total_qtd=Count('id'),
            total_receita=Sum('valor_pago')
        )
        
        vendedores = User.objects.filter(ingresso__sessao=sessao_selecionada).annotate(
            qtd=Count('ingresso'),
            total=Sum('ingresso__valor_pago')
        ).order_by('-total')
        
        metricas = {
            'resumo': resumo,
            'vendedores': vendedores
        }

    context = {
        'sessoes_lista': sessoes_lista,
        'sessao_selecionada': sessao_selecionada,
        'metricas': metricas,
    }
    return render(request, 'bilheteria/relatorios.html', context)
