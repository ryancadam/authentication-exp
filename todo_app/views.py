from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo_app/home.html')


def usersignup(request):
    if request.method == 'GET':
        return render(request, 'todo_app/usersignup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current')
            except IntegrityError:
                return render(request, 'todo_app/usersignup.html', {'form': UserCreationForm(), 'error': 'Username taken. Try another...'})
        else:
            return render(request, 'todo_app/usersignup.html', {'form': UserCreationForm(), 'error': 'Passwords do not match'})


def userlogin(request):
    if request.method == 'GET':
        return render(request, 'todo_app/userlogin.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo_app/userlogin.html', {'form': AuthenticationForm(), 'error': 'username and password didn\'t match'})
        else:
            login(request, user)
            return redirect('current')


@login_required
def userlogout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'todo_app/create.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo_app/create.html', {'form': TodoForm(), 'error': 'bad info entered. What\'s a matter with you? '})


@login_required
def current(request):
    todos = Todo.objects.filter(user=request.user, completion_date__isnull=True)
    return render(request, 'todo_app/current.html', {'todos': todos})


@login_required
def completed(request):
    todos = Todo.objects.filter(user=request.user, completion_date__isnull=False).order_by('-completion_date')
    return render(request, 'todo_app/completed.html', {'todos': todos})


@login_required
def seetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo)
        return render(request, 'todo_app/seetodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo_app/seetodo.html', {'todo': todo, 'form': form, 'error': 'bad data'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completion_date = timezone.now()
        todo.save()
        return redirect('current')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current')


