from Server_API.models import Category, SellRequest, RequestCategory, Users
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Category
        # Поля, которые мы сериализуем
        fields = ["id", "name_category", "status", "info"]

class SellRequestSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = SellRequest
        # Поля, которые мы сериализуем
        fields = ["id", "date_creation", "date_formation", "date_completion", "status", "id_creator", "id_moderator"]

class RequestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = RequestCategory
        # Поля, которые мы сериализуем
        fields = "__all__"