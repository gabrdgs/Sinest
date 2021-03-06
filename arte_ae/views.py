from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from arte_ae.forms import EventoForm
from arte_ae.models import *

from django.http import JsonResponse
from django.core import serializers

# Create your views here.
@login_required
def painel_de_controle(request):
  eventos = Evento.objects.filter(user=request.user)
  context = {
    'user': request.user,
    'eventos': eventos
  }
  return render(request, 'painel-de-controle.html', context)

@login_required
def cadastro_evento(request):
  form = EventoForm(request.POST, request.FILES)
  if form.is_valid():
    form.instance.user = request.user
    form.save()
    context = {
      'msg': 'Evento cadastrado com sucesso'
    }
    return render(request, 'cadastro-evento.html', context)
  context = {
    'form': form
  }
  return render(request, 'cadastro-evento.html', context)

def get_evento(request, id):
  evento = Evento.objects.filter(id=id)
  evento_serialized = serializers.serialize('json', evento)
  return JsonResponse(evento_serialized, safe=False)

def index(request):
  eventos = Evento.objects.all()
  context = {
    'eventos': eventos
  }
  return render(request, 'index.html', context)

def do_login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/painel')
    
  return render(request, 'login.html')

def do_logout(request):
  logout(request)
  return redirect('/login')

def cadastro_usuario(request):
  form = UserCreationForm(request.POST)
  if form.is_valid():
    form.save()
    context = {
      'msg': 'Cadastrado com sucesso'
    }
    return render(request, 'cadastro-usuario.html', context)
  context = {
    'form': form
  }
  return render(request, 'cadastro-usuario.html', context)