from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroForm, LoginForm


def index(req):
    return render(req, "index.html")

# Registro y Login

def registro(req):
    if req.method == "POST":
        form = RegistroForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistroForm()
    return render(req, "auth/registro.html", {"form": form})

# def login_usuario(req):
#     if req.method == "POST":
#         username = req.POST["username"]
#         password = req.POST["password"]
#         user = authenticate(req, username=username, password=password)

#         if user is not None:
#             login(req, user)
#             return redirect("index")

#         else:
#             return render(req, "auth/login.html", {"error": "Usuario y/o contraseña incorrectos."})
        
#     return render(req, "auth/login.html")

def login_usuario(req):
    if req.method == "POST":
        form = LoginForm(req.POST)

        if form.is_valid():
            username = req.POST["username"]
            password = req.POST["password"]
            user = authenticate(req, username=username, password=password)
        
            if user is not None:
                login(req, user)
                return redirect("index")
            else:
                return render(req, "auth/login.html", {"error": "Usuario y/o contraseña incorrectos."})
    else:
        form = LoginForm()
    return render(req, "auth/login.html", {"form": form})

def logout_usuario(req):
    logout(req)
    return redirect("login")