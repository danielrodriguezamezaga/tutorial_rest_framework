from django.urls import path, re_path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from snippets import views
from snippets.views import SnippetViewSetT6, UserViewSetT6  # , api_root


# Tutorial 6 Enlazar ViewSets a URLs explícitamente
# vinculando los métodos http a la acción requerida para cada vista.
snippet_list_t6 = SnippetViewSetT6.as_view({
    'get': 'list',
    'post': 'create'
})

snippet_detail_t6 = SnippetViewSetT6.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

snippet_highlight_t6 = SnippetViewSetT6.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list_t6 = UserViewSetT6.as_view({
    'get': 'list'
})

user_detail_t6 = UserViewSetT6.as_view({
    'get': 'retrieve'
})

# Tutorial 6 Routers
# Crea un enrutador y registra nuestros conjuntos de vistas con él.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSetT6)
router.register(r'users', views.UserViewSetT6)


urlpatterns = [
    path('snippets/t1/list/', views.snippet_list_t1),  # Views del tutorial 1 snippet_list_t1
    path('snippets/t1/detail/<int:pk>/', views.snippet_detail_t1),  # Views del tutorial 1 snippet_detail_t1

    path('snippets/t2/list/', views.snippet_list_t2),  # View del tutorial 2 snippet_list_t2
    path('snippets/t2/detail/<int:pk>/', views.snippet_detail),  # View del tutorial 2 snippet_detail_t2

    path('snippets/t3p1/list', views.SnippetListT3P1.as_view()),  # View del tutorial 3 snippet_list_t3_1
    path('snippets/t3p1/detail/<int:pk>/', views.SnippetDetailT3P1.as_view()),  # View del tutorial 3 snippet_list_t3_1

    path('snippets/t3p2/list/', views.SnippetListT3P2.as_view()),  # View del tutorial 3 snippet_list_t2
    path('snippets/t3p2/detail/<int:pk>/', views.SnippetDetailT3P2.as_view()),  # View del tutorial 3 snippet_list_t2

    path('snippets/t3p3/list/', views.SnippetListT3P3.as_view()),  # View del tutorial 3 snippet_list_t3
    path('snippets/t3p3/detail/<int:pk>/', views.SnippetDetailT3P3.as_view()),  # View del tutorial 3 snippet_list_t3

    path('users/t4/p1/list/', views.UserListNotOwner.as_view()),  # P4 auth/permisos list usuarios sin owner
    path('users/t4/p1/detail/<int:pk>/', views.UserDetailNotOwner.as_view()),  # P4 auth/permisos detail user sin owner

    path('users/t4/p2/list/', views.UserList.as_view()),  # P4_2 auth/permisos list usuarios sin owner
    path('users/t4/p2/detail/<int:pk>/', views.UserDetail.as_view()),  # P4_2 auth/permisos detail user sin owner

    # path('', views.api_root),
    path('snippets/t5/<int:pk>/highlight/', views.SnippetHighlight.as_view()),  # Para los resaltados del fragmento

    # API endpoints Tutorial 5 hiperlinks
    # path('', views.api_root),
    path('snippets/t5/', views.SnippetListT3P2.as_view(), name='snippet-list'),
    path('snippets/t5/<int:pk>/', views.SnippetDetailT3P2.as_view(), name='snippet-detail'),
    path('snippets/t5/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
    path('users/t5/', views.UserList.as_view(), name='user-list'),
    path('users/t5/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    # Tutorial 6: suprimo esta url ya viene del tutorial 5 "path('', views.api_root),"
    path('snippets/t6/', snippet_list_t6, name='snippet-list'),
    path('snippets/t6/<int:pk>/', snippet_detail_t6, name='snippet-detail'),
    path('snippets/t6/<int:pk>/highlight/', snippet_highlight_t6, name='snippet-highlight'),
    path('users/t6/', user_list_t6, name='user-list'),
    path('users/t6/<int:pk>/', user_detail_t6, name='user-detail'),

    # Routers url: conecta los recursos en vistas y url automaticamente
    path('', include(router.urls)),
]




