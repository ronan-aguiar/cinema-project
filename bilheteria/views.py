from django.shortcuts import render, get_object_or_404, redirect
from .models import Filme, Sessao, Ingresso
from django.contrib import messages

def index(request):
    filmes = Filme.objects.all()
    return render(request, 'bilheteria/index.html', {'filmes': filmes})

def filme_detalhes(request, filme_id):
    filme = get_object_or_404(Filme, pk=filme_id)
    sessoes = Sessao.objects.filter(filme=filme).order_by('horario')
    return render(request, 'bilheteria/filme_detalhes.html', {'filme': filme, 'sessoes': sessoes})

def sessao_detalhes(request, sessao_id):
    sessao = get_object_or_404(Sessao, pk=sessao_id)
    
    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        # Em um app real, o vendedor seria o usuário logado
        ingresso = Ingresso.objects.create(
            sessao=sessao,
            forma_pagamento=forma_pagamento
        )
        return redirect('compra_sucesso')

    return render(request, 'bilheteria/sessao_detalhes.html', {'sessao': sessao})

def compra_sucesso(request):
    return render(request, 'bilheteria/compra_sucesso.html')
