from Server_API.models import Category, SellRequest, RequestCategory, CustomUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_staff', 'is_superuser']

class SellRequestSerializer(serializers.ModelSerializer):
    creator = UserSerializer(source='id_creator', read_only=True)
    moderator = UserSerializer(source='id_moderator', read_only=True)
    class Meta:
        # Модель, которую мы сериализуем
        model = SellRequest
        # Поля, которые мы сериализуем
        fields = "__all__"
        #fields = ["id", "date_creation", "date_formation", "date_completion", "status", "creator", "moderator", "status_priority"]

class RequestCategorySerializer(serializers.ModelSerializer):

    class Meta:
        # Модель, которую мы сериализуем
        model = RequestCategory
        # Поля, которые мы сериализуем
        fields = "__all__"
        #fields = ["id_request", "id_category"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Category
        # Поля, которые мы сериализуем
        fields = "__all__"
        #fields = ["id", "name_category", "info", "image"]
