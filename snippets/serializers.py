from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


# Los Serializers se usan para nuestras representaciones de datos.
# Usando la class Serializer(BaseSerializer): de rest_framework --> serializers Tutorial1
class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    owner = serializers.ReadOnlyField(source='owner.username')


# Usando la class ModelSerializer(Serializer): de rest_framework --> serializers
class SnippetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')

    def create(self, validated_data):
        """
        Cree y devuelva una nueva instancia de `Snippet`, dados los datos validados.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualice y devuelva una instancia de `Snippet` existente, dados los datos validados.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


# Serializer de usuario tutorial 4 parte 1 el campo owner
class UserSerializerNotOwner(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


# Serializer de usuario tutorial 4 parte 2
class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets', 'owner')


"""
Tutorial 5 Hyperlinked
El HyperlinkedModelSerializer tiene las siguientes diferencias de ModelSerializer:
No incluye el id campo por defecto.
Incluye un url campo, usando HyperlinkedIdentityField.
Las relaciones usan HyperlinkedRelatedField, en lugar de PrimaryKeyRelatedField.
"""


class SnippetSerializerHyperLinked(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        # highlight apunta al 'snippet-highlight' patrón de url, en lugar del 'snippet-detail'patrón de url.
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializerHyperLinked(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')

