from django.shortcuts import render
from django.views import View
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse


class Main(View):
    def get(self, request):
        # request.session["get_me_from_the_consumer"] = "hi this is me"
        # print(request.session.get("get_me_from_the_main_page"))

        # data = {
        #     "type": "recevier.function",
        #     "message": "hi this event is from the views",
        # }

        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)("test", data)

        if request.user.is_authenticated:
            return redirect(reverse('home'))

        return render(request=request, template_name="chat/main.html")


class Login(View):
    def get(self, request):
        return render(request=request, template_name="chat/login.html")

    def post(self, request):

        data = request.POST.dict()
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request=request, username=username, password=password)

        if user != None:
            login(request=request, user=user)
            return redirect(reverse('home'))

        context = {"error":"there is something wrong"}
        return render(request=request, template_name="chat/login.html", context=context)


class Register(View):
    def get(self, request):
        return render(request=request, template_name="chat/register.html")

    def post(self, request):
        context = {}
        data = request.POST.dict()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        try:
            new_user = User()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.save()

            user = authenticate(request=request, username=username, password=password)
            if user != None:
                login(request=request, user=user)
                return redirect(reverse('home'))
        except:
            context.update({"error":"the data is wrong"})

        return render(request=request, template_name="chat/register.html", context=context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('main'))


class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            users = User.objects.all()
            context = {"user":request.user, "users":users}
            return render(request=request, template_name="chat/home.html",context=context)

        return redirect(reverse('main'))


class ChatPerson(View):
    def get(self, request, id):

        person = User.objects.get(id=id)
        me = request.user

        context = {"person": person, "me": me}


        return render(request=request, template_name="chat/chat_person.html",context=context)


# Create your views here.
