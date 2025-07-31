from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import User, Chamado, StatusChamado, PrioridadeChamado, MensagemChamado, CategoriaChamado, StatusChamado


# Create your views here.
@login_required
def index(request):
    atual_user = request.user
    
    """
    Render the index page of the Calls application.
    """
    if atual_user.is_superuser:
        # Se o usuário for superuser, redireciona para a página de administração.
        return render(request, 'Calls/dashboard_admin.html', {
            "chamados": Chamado.objects.all(),
            "chamados_andamento": Chamado.objects.filter(status__status='Em andamento'),
            "chamados_resolvidos": Chamado.objects.filter(status__status='Resolvido'),
            "chamados_enviados": Chamado.objects.filter(status__status='Enviado'),
            "status_chamados": StatusChamado.objects.all(),
            "prioridade_chamados": PrioridadeChamado.objects.all(),
            "user": atual_user,})
    else:
        # Se o usuário não for superuser, renderiza a página de index normal.
        chamados = Chamado.objects.filter(usuario=atual_user)
        return render(request, 'Calls/dashboard_user.html', {
            "chamados": chamados,
            "chamados_andamento": Chamado.objects.filter(usuario=atual_user, status__status='Em andamento'),
            "chamados_resolvidos": Chamado.objects.filter(usuario=atual_user, status__status='Resolvido'),
            "user": atual_user,
        })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Lógica de autenticação aqui:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('Calls:index'))
        else:
            # Se a autenticação falhar, renderiza a página de login com uma mensagem de erro.
            return render(request, 'Calls/login.html', {'message': 'Usuário ou senha inválidos'})
    return render(request, 'Calls/login.html')

@login_required
def logout_view(request):
    """
    Faz o logout do usuário e redireciona para a página de login.
    
    """
    logout(request)
    return HttpResponseRedirect(reverse('Calls:login'))

@login_required
def new_call(request):
    """
    Renderiza a página para criar um novo chamado.
    
    """
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        categoria = request.POST.get('categoria')
        prioridade = request.POST.get('prioridade')
        
        # Cria um novo chamado associado ao usuário atual.
        chamado = Chamado.objects.create(titulo=titulo, descricao=descricao, status=StatusChamado.objects.first(),
                                         prioridade=PrioridadeChamado.objects.get(id=prioridade),
                                         categoriaChamado=CategoriaChamado.objects.get(id=categoria),
                                         usuario=request.user)
        
        # Redireciona para a página de detalhes do chamado recém-criado.
        return HttpResponseRedirect(reverse('Calls:view', args=[chamado.id]))
    
    return render(request, 'Calls/new_call.html', 
                  {'user': request.user,
                   'categorias': CategoriaChamado.objects.all(),
                   'prioridades': PrioridadeChamado.objects.all(),
                   })
    
    
@login_required
def view(request, chamado_id):
    """
    Renderiza a página de detalhes de um chamado específico.
    
    """
    chamado = Chamado.objects.get(id=chamado_id)
    allMenssagens = MensagemChamado.objects.filter(chamado=chamado).order_by('data_envio')
    all_status = StatusChamado.objects.all()
    
    if request.method == 'POST':
        mensagem = request.POST['mensagem']
        # imagem = request.FILES.get('imagem')
        # video = request.FILES.get('video')
        
        # Cria uma nova mensagem associada ao chamado e ao usuário atual.
        MensagemChamado.objects.create(chamado=chamado, usuario=request.user, mensagem=mensagem)
        
        # Redireciona para a página de detalhes do chamado.
        return HttpResponseRedirect(reverse('Calls:view', args=[chamado_id]))
    
    if request.user.is_superuser:
        # Se o usuário for superuser, renderiza a página de detalhes do chamado com informações adicionais.
        menssagens = MensagemChamado.objects.exclude(usuario=request.user).filter(chamado=chamado, visualizado=False).order_by('data_envio')
        for mensagem in menssagens:
            mensagem.visualizado = True
            mensagem.save()
        return render(request, 'Calls/view_admin.html', {'chamado': chamado, 'user': request.user, 'mensagens': allMenssagens, 'all_status': all_status})
    else:
        menssagens = MensagemChamado.objects.exclude(usuario=request.user).filter(chamado=chamado, visualizado=False).order_by('data_envio')
        for mensagem in menssagens:
            mensagem.visualizado = True
            mensagem.save()
        return render(request, 'Calls/view.html', {'chamado': chamado, 'user': request.user, 'mensagens': allMenssagens})
    
    
@login_required
def change_status(request, chamado_id):
    """
    Altera o status de um chamado específico.
    
    """
    chamado = Chamado.objects.get(id=chamado_id)
    
    if request.method == 'POST':
        novo_status = request.POST['status']
        chamado.status = StatusChamado.objects.get(status=novo_status)
        chamado.save()
        
        # Redireciona para a página de detalhes do chamado.
        return HttpResponseRedirect(reverse('Calls:view', args=[chamado_id]))
    
    return HttpResponseRedirect(reverse('Calls:view', args=[chamado_id]))
    

@login_required
def user_calls(request):
    """
    Renderiza a página com todos os chamados do usuário atual.
    
    """
    atual_user = request.user
    
    if not atual_user.is_authenticated:
        return HttpResponseRedirect(reverse('Calls:login'))
    
    chamados = Chamado.objects.filter(usuario=atual_user)
    
    return render(request, 'Calls/all_calls_user.html', {'chamados': chamados, 'user': atual_user})

@login_required
def admin_calls(request):
    """
    Renderiza a página com todos os chamados do usuário atual.
    
    """
    atual_user = request.user
    
    if not atual_user.is_authenticated:
        return HttpResponseRedirect(reverse('Calls:login'))
    
    chamados = Chamado.objects.all()
    
    return render(request, 'Calls/all_calls_admin.html', {'chamados': chamados, 'user': atual_user})

@login_required
def users_view(request):
    """
    Renderiza a página com todos os usuários do sistema.
    
    """
    atual_user = request.user
    
    if not atual_user.is_superuser:
        return HttpResponseRedirect(reverse('Calls:login'))
    
    users = User.objects.all()
    
    return render(request, 'Calls/users.html', {'users': users, 'user': atual_user})
  