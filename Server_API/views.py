from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from Server_API.serializers import CategorySerializer, SellRequestSerializer, RequestCategorySerializer, UsersSerializer
from Server_API.models import Category, SellRequest, RequestCategory, Users
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
import base64, io
from PIL import Image
from minio import Minio
from minio.error import S3Error
from config import Config


class UserSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.user_get()
        return cls._instance

    @classmethod
    def user_get(cls):
        return Users.objects.create(name_user="UserConst", password="123", moderator_sign=False)



class CategorysList(APIView):
    model_class = Category
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        """
        Возвращает список категорий
        """

        categorys = Category.objects.filter(name_category__icontains=request.GET.get('category')).filter(status='Действует')
        sell_req = SellRequest.objects.filter(status='Черновик').last()

        if categorys is None:
            categorys = Category.objects.all()

        serializer = CategorySerializer(categorys, many=True)
        serializer2 = SellRequestSerializer(sell_req)
        data = {
            "request": serializer2.data,
            "categorys": serializer.data
        }


        return Response(data)

    def post(self, request, format=None):
        """
        Добавляет новую категорию
        """

        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        client = Minio(
            endpoint="localhost:9000",
            access_key="minio",
            secret_key="minio124",
            secure=False,
        )
        try:
            cat = request.data.get('name_category')
            img_name = f"{cat}.jpeg"
            file_path = f"templates/{request.data.get('image')}"
            client.fput_object(
                bucket_name="server-api", object_name=img_name, file_path=file_path
            )
            image_name = f"minio:http://localhost:9000/server-api/{img_name}"
            new_cat = Category.objects.create(name_category=cat, status=request.data.get('status'),
                                              info=request.data.get('info'), image=image_name)
        except Exception as e:
            return Response({"error": str(e)})
        serializer = CategorySerializer(new_cat)
        return Response(serializer.data)


class CategorysDetail(APIView):
    model_class = Category
    model_class_2 = SellRequest
    serializer_class = CategorySerializer
    serializer_class_2 = SellRequestSerializer

    def get(self, request, id, format=None):
        """
        Возвращает информацию о категории
        """
        categorys = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(categorys)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        """
        Обновляет информацию о категории
        """
        categorys = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(categorys, data=request.data, partial=True)

        if serializer.is_valid():
            client = Minio(
                endpoint="localhost:9000",
                access_key="minio",
                secret_key="minio124",
                secure=False,
            )
            try:
                cat = Category.objects.get(id=id)
                name_cat = cat.name_category
                img_name = f"{name_cat}.jpeg"
                file_path = f"templates/{request.data.get('image')}"
                client.fput_object(
                    bucket_name="server-api", object_name=img_name, file_path=file_path
                )
                cat.image = f"minio:http://localhost:9000/server-api/{img_name}"
                cat.save()
            except Exception as e:
                return Response({"error": str(e)})
            serializer = CategorySerializer(cat)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        """
        Удаляет категорию
        """
        category = get_object_or_404(self.model_class, id=id)
        category.status = "Удален"
        return Response(status=status.HTTP_204_NO_CONTENT)







@api_view(["POST"])
def add_cat_to_req(request, id):
    if not Category.objects.filter(id=id).exists():
        return Response(f"Категории с таким id не существует!")

    category = Category.objects.get(id=id)


    sell_req = SellRequest.objects.filter(status='Черновик').last()
    const_user = UserSingleton.get_instance()

    if sell_req is None:
        sell_req = SellRequest.objects.create(id_creator=const_user, date_creation=datetime.now())
        sell_req.save()
    sell_req_2 = SellRequest.objects.get(id=sell_req.id)
    request_cat = RequestCategory.objects.create(id_category=category, id_request=sell_req_2)

    serializer = RequestCategorySerializer(request_cat, many=True)
    return Response(serializer.data)

class RequestsList(APIView):
    model_class = SellRequest
    serializer_class = SellRequestSerializer

    def get(self, request, format=None):
        """
        Возвращает список заявок
        """

        STATUS = (

            'Завершен',
            'Отклонен',
            'Сформирован'
        )
        sell_req = SellRequest.objects.filter(Q(status='Завершен') | Q(status='Отклонен') | Q(status='Сформирован'))

        if request.GET.get('status') is not None:
            status_cmd = request.GET.get('status')
            if status_cmd not in STATUS:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            sell_req = sell_req.filter(status=status_cmd)
        if request.GET.get('from_date') is not None:
            from_date = request.GET.get('from_date')
            sell_req = sell_req.filter(date_formation__gte=datetime.strptime(from_date, '%Y-%m-%d %H:%M'))
        if request.GET.get('to_date') is not None:
            to_date = request.GET.get('to_date')
            sell_req = sell_req.filter(date_formation__lte=datetime.strptime(to_date, '%Y-%m-%d %H:%M'))
        serializer = SellRequestSerializer(sell_req, many=True)
        return Response(serializer.data)


class RequestsDetail(APIView):
    model_class = SellRequest
    serializer_class = SellRequestSerializer
    model_class2 = Category
    serializer_class2 = CategorySerializer

    def get(self, request, id, format=None):

        request = SellRequest.objects.get(id=id)
        categorys = Category.objects.filter(requestcategory__id_request=id)
        data_cat = []
        for cat in categorys:
            serializer2 = CategorySerializer(cat)
            data_cat.append(serializer2.data)
        serializer = SellRequestSerializer(request)

        data = {
            "request:": serializer.data,
            "categorys:": data_cat
        }
        return Response(data)





    def delete(self, request, id, format=None):
        """
        Удаляет информацию заявку
        """
        sell_req = get_object_or_404(self.model_class, id=id)
        sell_req = SellRequest.objects.get(id=id)
        sell_req.status = "Удален"
        sell_req.save()
        request_cat = RequestCategory.objects.filter(id_request=id)
        request_cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["PUT"])
def put_status_user(request, id):
    if not SellRequest.objects.filter(id=id).exists():
        return Response(f"Заявки с таким id не существует!")

    STATUS = (
        'Сформирован',
        'Удален'
    )
    request_status = request.data["status"]

    if request_status not in STATUS:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    sell_request = SellRequest.objects.get(id=id)
    sell_request_status = sell_request.status

    if sell_request_status == 'Удален':
        return Response("Статус изменить нельзя")

    sell_request.status = request_status
    sell_request.date_formation = datetime.now()
    sell_request.save()
    serializer = SellRequestSerializer(sell_request, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
def put_status_admin(request, id):
    if not SellRequest.objects.filter(id=id).exists():
        return Response(f"Заявки с таким id не существует!")
    STATUS = (

        'Завершен',
        'Отклонен',
        'Удален',
    )
    request_status = request.data["status"]

    if request_status not in STATUS:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    sell_request = SellRequest.objects.get(id=id)

    sell_request_status = sell_request.status

    if sell_request_status == 'Удален':
        return Response("Статус изменить нельзя")

    sell_request.status = request_status
    if request_status == "Завершен":
        sell_request.date_completion = datetime.now()
        user_mod = Users.objects.filter(moderator_sign=True).last()

        if user_mod is None:
            user_mod = Users.objects.create(name_user="admin", password="321", moderator_sign=True)
            user_mod.save()
        sell_request.id_moderator = user_mod
    sell_request.save()

    serializer = SellRequestSerializer(sell_request, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def search_categorys(request):

    category = Category.objects.filter(name_category__icontains=request.GET.get('category')).filter(status='Действует')
    if category is None:
        category = Category.objects.all()

    serializer = CategorySerializer(category, many=True)

    return Response(serializer.data)

@api_view(["DELETE"])
def delete_category_from_request(request, id_req, id_cat):
    if not SellRequest.objects.filter(id=id_req).exists():
        return Response(f"Заявки с таким id не существует")

    if not Category.objects.filter(id=id_cat).exists():
        return Response(f"Категории с таким id не существует")

    request_cat = RequestCategory.objects.filter(Q(id_request=id_req) & Q(id_category=id_cat))
    request_cat.delete()

    serializer = RequestCategorySerializer(request_cat, many=True)
    return Response(serializer.data)

