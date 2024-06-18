from django.urls import path
from .views import dates, search, LikeView,HomeListView,PostDetailView,CategoryListView,AuthorListView,PostCreateView,PostUpdateView,PostDeleteView,AboutPageView,TagListView
from .views import profile, password_change

urlpatterns = [
    #PAGINA DE INICIO
    path('', HomeListView.as_view(), name='home'),

    #DETALLE DEL POST
    path('post/<pk>',PostDetailView.as_view(), name='post'),

    #PAGINA FILTRADO DE CATEGORIAS
    path('category/', CategoryListView.as_view(), name='category'),

    #PAGINA FILTRADO DE etiquetas
    path('tag/', TagListView.as_view(), name='tag'),

    #PAGINA FILTRADO DE AUTOR
    path('author/',AuthorListView.as_view(), name='author'),
 
    #PAGINA FILTRADO POR FECHA
    path('dates/<int:month_id>/<int:year_id>', dates, name='dates'),

    #LIKES DE UN POST
    path('like/<int:pk>', LikeView, name='like_post'),

    #crear post
    path('create/',PostCreateView.as_view(), name='create'),

    #editar post
    path('update/<int:pk>',PostUpdateView.as_view(), name='update'),

    #eliminar post
    path('delete/<int:pk>',PostDeleteView.as_view(), name='delete'),

    #About - Acerca de nosotros
    path('about/',AboutPageView.as_view(), name='about'),

    #Filtrado por busqueda
    path('search/', search, name='search'),

    #estaban en core de Allauth
    path('accounts/profile/', profile, name='profile' ),
    path('accounts/password/change/', password_change, name='account_change_password' ),
]