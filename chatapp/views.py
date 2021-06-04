from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User



# Create your views here.



def index(request):
    if request.user.is_authenticated:
        return redirect('/chat/')
    if request.method == 'GET':
        return render(request, 'index.html', {})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('/chat/')


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print(user, "@@@@@@@@@@@@@@")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            print("!!!!!!!!!!")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/chat/')

    else:
        form = SignUpForm()
    template = 'register.html'
    context = {'form':form}
    return render(request, template, context)


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render(request, 'chat.html', {'users':User.objects.exclude(username=request.user.username )})


def logout_view(request):
    logout(request)
    return redirect('/')