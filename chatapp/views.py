from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import *



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


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == "GET":
        print(sender, receiver, "++++++++++++++++")
        return render(request, "messages.html", {
            'users': User.objects.exclude(username = request.user.username),
            'receiver': User.objects.get(id=receiver),
            'messages' : Message.objects.filter(sender_id=sender, receiver_id=receiver) | Message.objects.filter(sender_id=receiver, receiver_id=sender)

        })


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request':request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



