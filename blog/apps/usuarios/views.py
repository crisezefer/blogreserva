from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import *
from django.views import generic

# Create your views here.


# Registrar un usuario

class RegistroUsuario(CreateView):
    success_url = reverse_lazy('login')
    model = User
    template_name = 'Login/registrar.html'
    form_class = ResgistroForm
    


# Login 

class Login(FormView):
    template_name = 'login/login.html'
    form_class = FormularioLogin

    success_url = reverse_lazy('posteos')

    @method_decorator(csrf_protect) # Este decorador agrega protección CSRF
    @method_decorator(never_cache)
    def dispatch(self, request, *args , **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else: 
            return super(Login,self).dispatch(request, *args, **kwargs)

    def form_valid(self, form) :
        login(self.request,form.get_user())
        return super(Login, self).form_valid(form)


def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/usuario/login')

def home_base(request):
    return render(request, 'login/home.html')

def objetivos(request):
    return render(request, 'objetivos.html')

def proyectos(request):
    return render(request, 'proyectos.html')
    
def quienes(request):
    return render(request, 'quienes.html')