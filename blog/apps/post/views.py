from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.urls import reverse_lazy
from .models import *
from .forms import PostForm
# vista para crear posteo
def crearPost(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST or None, request.FILES or None)
        if post_form.is_valid():
            post_form.save()
            return redirect('crear_post')
    else:
        post_form = PostForm()
    return render(request, 'post/crear_post.html', {'post_form': post_form})

class MostrarPost(View):
    template_name = 'post/posteos.html'
    
    def get(self, request):
        posteos = Post.objects.all()
        categorias = Categoria.objects.all()
        context = {
            'posteos': posteos,
            'categorias': categorias,

        }
        return render (request, self.template_name, context)

    def post(self, request):
        categorias = Categoria.objects.all()
        cate = request.POST.get('categoria', None)
        fecha = request.POST.get('fecha', None)
        if cate and fecha:
            posteos = Post.objects.filter(categoria__nombre=cate, fecha_creacion=fecha)
        elif cate:
            posteos = Post.objects.filter(categoria__nombre=cate)
        elif fecha:
             posteos = Post.objects.filter(fecha_creacion=fecha)
        context = {
            'posteos': posteos,
            'categorias': categorias,

        }
        return render (request, self.template_name, context)
# Create your views here

def leerPost(request, id):
    if request.method=='GET':
        post = Post.objects.get(id=id)
        comentarios = Comentario.objects.filter(posteo=id)
        context = {
            'post': post,
            'comentarios':comentarios
        }
    return render(request, 'post/posteo.html', context)



@login_required
def comentar_Post(request):

    com = request.POST.get('comentario',None)
    usu = request.user
    noti = request.POST.get('id_post', None)
    post = Post.objects.get(id = noti) 
    Comentario.objects.create(usuario = usu, posteo = post, texto = com)

    return redirect(reverse_lazy('posteo', kwargs={'id': noti}))

