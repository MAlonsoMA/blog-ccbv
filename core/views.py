import shutil
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Post, Category, Tag
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.base import TemplateView
from django.db.models import Q
import os

from .forms import PostForm

# Home
class HomeListView(ListView):
    model=Post
    paginate_by=4
    template_name='core/home.html'

    def get_queryset(self): 
        return Post.objects.filter(published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Detalle del Post
class PostDetailView(DetailView):
    model=Post
    template_name='core/detail.html'
    context_object_name='post'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        post=self.get_object()
        total_likes=post.total_likes()
        liked=False
        if post.likes.filter(id=self.request.user.id).exists():
            liked=True
        context['total_likes']=total_likes
        context['liked']=liked
        return context


# Filtrado por Categoría
class CategoryListView(ListView):
    model:Category
    template_name='core/category.html'
    
    def get_queryset(self):
        category_id=self.request.GET['cat']
        if category_id:
            return Post.objects.filter(category=category_id, published=True)
        return super().get_queryset()
    def get_context_data(self, **kwargs):
        context=super(CategoryListView,self).get_context_data(**kwargs)
        context['category']=Category.objects.get(id=self.request.GET['cat'])
        return context
    
# Filtrado por Etiqueta
class TagListView(ListView):
    model:Tag
    template_name='core/tag.html'
    
    def get_queryset(self):
        tag_id=self.request.GET['tag']
        if tag_id:
            return Post.objects.filter(tags=tag_id)
        return super().get_queryset()
    def get_context_data(self, **kwargs):
        context=super(TagListView,self).get_context_data(**kwargs)
        context['tag']=Tag.objects.get(id=self.request.GET['tag'])
        return context

# Filtrado por Author
class AuthorListView(ListView):
    model:User
    template_name='core/author.html'
    
    def get_queryset(self):
        author_id=self.request.GET['aut']
        if author_id:
            return Post.objects.filter(author=author_id, published=True)
        return super().get_queryset()
    def get_context_data(self, **kwargs):
        context=super(AuthorListView,self).get_context_data(**kwargs)
        context['author']=User.objects.get(id=self.request.GET['aut'])
        return context
    

def dates(request, month_id, year_id):

    meses = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }

    if month_id > 12 or month_id < 1:
        return render(request, 'core/404.html')

    posts = Post.objects.filter(published=True, created__month=month_id, created__year=year_id)
    return render(request, 'core/dates.html', {'posts':posts, 'month':meses[month_id], 'year':year_id})

# Likes en un post
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post', args=[str(pk)]))

# Crear post
class PostCreateView(CreateView):
    model=Post
    form_class=PostForm

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    success_url=reverse_lazy('home')

# Editar el post
class PostUpdateView(UpdateView):
    model=Post
    form_class=PostForm
    template_name_suffix = '_update_form'

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('update', args=[self.object.id]) + '?ok'
    

# Eliminar el post
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('home')

# Página About
class AboutPageView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
# Búsqueda
def search(request):
    queryset=request.GET.get("search")
    if queryset:
        posts=Post.objects.filter(
            Q(title__icontains=queryset) | 
            Q(excerpt__icontains=queryset) |
            Q(content__icontains=queryset),
            published=True,
        ).distinct()
    else:
        posts={}

    return render(request,'core/search.html',{'posts':posts,'queryset':queryset})

#Allauth
def profile(request):
    return render(request, 'account/profile.html')

def password_change(request):
    return render(request, 'account/password_change.html')