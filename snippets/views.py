from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework import status, mixins, generics, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework import renderers
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse  # Para devolver direcciones URL completamente calificadas
from rest_framework import viewsets
from rest_framework.decorators import action

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, SnippetModelSerializer
from snippets.serializers import UserSerializerNotOwner, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


#####################
# Vistas tutorial 1 #
#####################
@csrf_exempt
def snippet_list_t1(request):

    # Lista todos los fragmentos de código o crea uno nuevo.

    # Listar (Depurado y funciona)
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    # Crear
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# Función para un fragmento individual.
@csrf_exempt
def snippet_detail_t1(request, pk):

    # Comprueba que existe (Depurado, el fragmento solicitado por PK lo almacena en la variable snippet).
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    # Listar un fragmento por PK (Depurado me devuelve el fragmento si existe su PK)
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    # Actualizar (No depurada)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # Eliminar (No depurada)
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


#####################
# Vistas tutorial 2 #
#####################
@api_view(['GET', 'POST'])
def snippet_list_t2(request, format=None):
    # Lista todos los fragmentos de código o crea uno nuevo.

    # Listar (Depurado me lista todos los fragmentos).
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    # Crear (Depurado, crea fragmento)
    # Ejemplo usando Httpie: http --form POST http://127.0.0.1:8080/snippets_t2/ code="print 123" --> Usando FORM data
    # Ejemplo usando Httpie: http --json POST http://127.0.0.1:8080/snippets_t2/ code="print 456" --> Usando JSON
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Función para un fragmento individual.
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):

    # Comprueba que existe por PK
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Muestra el fragmento solicitado por PK
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    # Metodo Put editar todos los campos del fragmento solicitado
    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Elimina el fragmento solicitado
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


###############################################
# Vistas tutorial 3 basadas en clases parte 1 #
###############################################
class SnippetListT3P1(APIView):
    # Lista todos los fragmentos de código o crea uno nuevo.

    # Listar (Depurado)
    # Usando Httpie: http http://127.0.0.1:8080/snippets_t3/
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    # Crear (Depurado)
    # Usando Httpie: http http://127.0.0.1:8080/snippets_t3/ code=1989
    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetailT3P1(APIView):

    # Recoge el objeto si existe(Depurado)
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    # Muestra GET Retrieve (Depurado)
    # Usando Httpie: http http://127.0.0.1:8080/snippets_t3/5/
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    # Edita PUT
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Elimina DELETE (Depurado)
    # Usando Httpie: http DELETE http://127.0.0.1:8080/snippets_t3/5/
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


##############################################
# Vistas tutorial 3 Parte 2 Utilizando Mixin #
##############################################
class SnippetListT3P2(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # Lista todos los fragmentos de código o crea uno nuevo.

    # Lista (Depurado)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # Crear (Depurado)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetDetailT3P2(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # Recoge el objeto, lo muestra, edita o elimina.

    # Muestra (Depurado)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # Edita
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # Elimina
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


################################################################
# Vistas tutorial 3 Parte 3 Vistas genéricas basadas en clases #
################################################################
class SnippetListT3P3(generics.ListCreateAPIView):  # Lista todos los fragmentos de código o crea uno nuevo.
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # (Depurado listar y crear)


class SnippetDetailT3P3(generics.RetrieveUpdateDestroyAPIView):  # Recoge el objeto, lo muestra, edita o elimina.
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # (Depurado eliminar y listar)


##############################################
# Vistas tutorial 4 autenticación y permisos #
##############################################

# Tutorial 4 Permisos y autenticacion Sin owner
# ListAPIViewy RetrieveAPIView las vistas genéricas basadas en clases
class UserListNotOwner(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerNotOwner


class UserDetailNotOwner(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerNotOwner


# Tutorial 4 Permisos y autenticacion con owner #
# ListAPIViewy RetrieveAPIView las vistas genéricas basadas en clases
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerNotOwner


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetListT4P2(generics.ListCreateAPIView):  # Lista todos los fragmentos de código o crea uno nuevo.
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # Gestionando el guardado de la instancia con el metodo perfom_create
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetailT4P2(generics.RetrieveUpdateDestroyAPIView):  # Recoge el objeto, lo muestra, edita o elimina.
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


# Tutorial 5 Relaciones y APIs hipervinculadas
# Highlight para tratar con HTML pre-renderizado
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# Vista regular basada en funciones con @api_view ya no es necesario con los routers
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # Reverse función del marco REST devuelve direcciones URL completamente calificadas
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


########################################
# Vistas tutorial 6 ViewSets & Routers #
########################################
# Refactorizando las vistas usando ViewSet
class UserViewSetT6(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializerNotOwner


class SnippetViewSetT6(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Snippet.objects.all()
    # Cambie SnippetSerializer por SnipetModelSerializer debido al error que me da ese serializador
    serializer_class = SnippetModelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # Este decorador se puede usar para agregar puntos finales personalizados que no se ajusten al estilo.
    # methods argumento si quisiéramos una acción que respondiera a las solicitud POST.
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)






