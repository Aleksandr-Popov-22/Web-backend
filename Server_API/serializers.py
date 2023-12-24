from Server_API.models import Category, SellRequest, RequestCategory, Users
from rest_framework import serializers



class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Users
        # Поля, которые мы сериализуем
        fields = ["name_user"]


class SellRequestSerializer(serializers.ModelSerializer):
    creator = UsersSerializer(source='id_creator', read_only=True)
    moderator = UsersSerializer(source='id_moderator', read_only=True)
    class Meta:
        # Модель, которую мы сериализуем
        model = SellRequest
        # Поля, которые мы сериализуем
        #fields = "__all__"
        fields = ["id", "date_creation", "date_formation", "date_completion", "status", "creator", "moderator"]

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
        #fields = ["id", "name_category", "status", "info", "image"]
