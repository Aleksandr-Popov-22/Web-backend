from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from Server_API.serializers import CategorySerializer, SellRequestSerializer, RequestCategorySerializer
from Server_API.models import Category, SellRequest, RequestCategory, Users
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Q


class CategorysList(APIView):
    model_class = Category
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        """
        Возвращает список категорий
        """
        categorys = self.model_class.objects.all()
        serializer = self.serializer_class(categorys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Добавляет новую категорию
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        """
        Удаляет категорию
        """
        categorys = get_object_or_404(self.model_class, id=id)
        categorys.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["POST"])
def add_cat_to_req(request, id):
    if not Category.objects.filter(id=id).exists():
        return Response(f"Категории с таким id не существует!")

    category = Category.objects.get(id=id)


    sell_req = SellRequest.objects.filter(status='Черновик').last()

    if sell_req is None:
        sell_req = SellRequest.objects.create()
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
        requests = self.model_class.objects.all()
        serializer = self.serializer_class(requests, many=True)
        return Response(serializer.data)


class RequestsDetail(APIView):
    model_class = SellRequest
    serializer_class = SellRequestSerializer

    def get(self, request, id, format=None):
        """
        Возвращает информацию о заявке
        """
        requests = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(requests)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        """
        Обновляет информацию о заявке
        """
        requests = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(requests, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        """
        Удаляет информацию заявку
        """
        sell_req = get_object_or_404(self.model_class, id=id)
        sell_req.delete()
        request_cat = RequestCategory.objects.filter(id_request=id)
        request_cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(["GET"])
def get_requests_category(request):

    sell_req = SellRequest.objects.filter(status="Черновик")
    category = Category.objects.filter(requestcategory__id_request__in=sell_req)


    serializer = CategorySerializer(category, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def get_categorys_request(request, id):
    if not SellRequest.objects.filter(id=id).exists():
        return Response(f"Заявки с таким id не существует!")


    categorys = Category.objects.filter(requestcategory__id_request=id)


    serializer = CategorySerializer(categorys, many=True)

    return Response(serializer.data)


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

