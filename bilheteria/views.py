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
    hoje = timezone.localtime(timezone.now()).date()
    vendas_hoje = Ingresso.objects.filter(data_venda__date=hoje)
    
    # Resumo Geral
    total_receita = vendas_hoje.aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0
    total_ingressos = vendas_hoje.count()
    
    # Vendas por Sessão (com detalhamento de tipos)
    from django.db.models import Q
    vendas_por_sessao = Sessao.objects.filter(horario__date=hoje).annotate(
        qtd_inteira=Count('ingresso', filter=Q(ingresso__tipo='INTEIRA')),
        qtd_meia=Count('ingresso', filter=Q(ingresso__tipo='MEIA')),
        total_vendas=Count('ingresso'),
        receita=Sum('ingresso__valor_pago')
    ).order_by('horario')
    
    # Vendas por Vendedor
    vendas_por_vendedor = User.objects.filter(ingresso__data_venda__date=hoje).annotate(
        qtd=Count('ingresso'),
        total=Sum('ingresso__valor_pago')
    ).order_by('-total')

    context = {
        'hoje': hoje,
        'total_receita': total_receita,
        'total_ingressos': total_ingressos,
        'vendas_por_sessao': vendas_por_sessao,
        'vendas_por_vendedor': vendas_por_vendedor,
    }
    return render(request, 'bilheteria/relatorios.html', context)
