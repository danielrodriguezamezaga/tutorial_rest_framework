from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    #Punto final de API que permite a los usuarios ver o editar.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    #Punto final de API que permite ver o editar grupos.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
