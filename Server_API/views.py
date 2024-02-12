from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from Server_API.serializers import CategorySerializer, SellRequestSerializer, RequestCategorySerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import viewsets
from .permissions import *
from django.conf import settings
import redis
import uuid
from django.contrib.sessions.models import Session
from django.views.decorators.http import require_http_methods
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Connect to our Redis instance
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)




class CurrentUserSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls._get_user()
        return cls._instance

    @classmethod
    def _get_user(cls):
        return CustomUser.objects.get(
            email="check@list.ru",
            password="pbkdf2_sha256$600000$XjFy1vVc2KoGlNI6tDpWVb$r7ahJQyjwhRmtacF8Td2+FubN6Ny3wLwuqgnvqT6kYg=",
        )

@api_view(["GET"])
def GetCategory(request):

    title = request.query_params.get("category")
    categorys = Category.objects.filter(status="Действует")

    if title:
        categorys = categorys.filter(name_category__icontains=title)
    try:
        ssid = request.COOKIES["session_id"]
        email = session_storage.get(ssid).decode("utf-8")
        current_user = CustomUser.objects.get(email=email)
        sell_req = SellRequest.objects.get(
            id_user=current_user, status="Черновик"
        )
        # .latest("creation_date")
        serializer = CategorySerializer(categorys, many=True)
        sellreq_serializer = SellRequestSerializer(sell_req)

        result = {
            "sellreq_id": sellreq_serializer.data["id"],
            "categorys": serializer.data,
        }
        return Response(result)
    except:
        serializer = CategorySerializer(categorys, many=True)
        result = {"categorys": serializer.data}
        return Response(result)

@api_view(["POST"])
@permission_classes([IsManager])
def category_post(request):
    serializer = CategorySerializer(data=request.data)
    serializer.data["status"] = "Действует"
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
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

@swagger_auto_schema(method='put', request_body=CategorySerializer)
@api_view(["PUT"])
@permission_classes([IsManager])
def category_put(request, id):
    if not Category.objects.filter(id=id).exists():
        return Response(f"Категории с таким id нет")
    category = get_object_or_404(Category, id=id)
    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
@permission_classes([IsManager])
def category_delete(request, id):
    if not Category.objects.filter(id=id).exists():
        return Response(f"Категории с таким id нет")
    category = Category.objects.get(id=id)
    category.status = "Удалена"
    category.save()

    category = Category.objects.filter(status="Действует")
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=RequestCategorySerializer)
@api_view(["POST"])
@permission_classes([IsAuth])
def add_cat_to_req(request, id):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode("utf-8")
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response("Сессия не найдена")

    try:
        sellreq = SellRequest.objects.filter(
            id_user=current_user, status="Черновик"
        ).latest("date_creation")
    except:
        sellreq = SellRequest(
            status="Черновик",
            date_creation=datetime.now(),
            id_user=current_user,
        )
        sellreq.save()
    sellreq_id = sellreq
    try:
        category = Category.objects.get(id=id, status="Действует")
    except Category.DoesNotExist:
        return Response("Такой категории нет", status=400)
    try:
        req_cat = RequestCategory.objects.get(
            id_request=sellreq_id, id_category=category
        )
        return Response("Такая категория уже есть в заявке")
    except RequestCategory.DoesNotExist:
        req_cat = RequestCategory(
            id_request=sellreq_id,
            id_category=category,
        )
        req_cat.save()
    addedCategory = Category.objects.get(id=id)
    serializer = CategorySerializer(addedCategory)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuth])
def requests_get(request):

    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode("utf-8")
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response("Сессия не найдена")

    date_format = "%Y-%m-%d"
    start_date_str = request.query_params.get("from_date")
    end_date_str = request.query_params.get("to_date")
    start = datetime.strptime(start_date_str, date_format).date()
    end = datetime.strptime(end_date_str, date_format).date()

    status = request.data.get("status")

    if current_user.is_superuser:  # Модератор может смотреть заявки всех пользователей
        print("модератор")
        sell_req = SellRequest.objects.filter(
            ~Q(status="Удалена"), date_creation__range=(start, end)
        )
    else:  # Авторизованный пользователь может смотреть только свои заявки
        print("user")
        sell_req = SellRequest.objects.filter(
            ~Q(status="Удалена"),
            id_user=current_user.id,
            date_creation__range=(start, end),
            )

    if status:
        sell_req = sell_req.filter(status=status)
    sell_req = sell_req.order_by("date_creation")
    serializer = SellRequestSerializer(sell_req, many=True)

    return Response(serializer.data)
@api_view(["GET"])
@permission_classes([IsAuth])
def sellrequest_get(request, id):

    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode("utf-8")
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response("Сессия не найдена")

    try:
        sell_req = SellRequest.objects.get(id=id)
        if sell_req.status == "Удалена" or not sell_req:
            return Response("Заявки с таким id нет")
        sell_req_serializer = SellRequestSerializer(sell_req)

        if (
                    not current_user.is_superuser
                    and current_user.id == sell_req_serializer.data["id_user"]
        ) or (current_user.is_superuser):
            cat_req = RequestCategory.objects.filter(
                id_request=sell_req
            )
            category_ids = [category.id for category in cat_req]
            category_queryset = Category.objects.filter(id__in=category_ids)
            category_serializer = CategorySerializer(category_queryset, many=True)
            response_data = {
                "sell_req": sell_req_serializer.data,
                "category": category_serializer.data,
            }
            return Response(response_data)
        else:
            return Response("Заявки с таким id нет")

    except SellRequest.DoesNotExist:
        return Response("Заявки с таким id нет")

@api_view(["DELETE"])
@permission_classes([IsAuth])
def request_delete(request):

    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode("utf-8")
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response("Сессия не найдена")
    try:
        sell_req = SellRequest.objects.get(
            id_user=current_user, status="Черновик"
        )
        sell_req.status = "Удалена"
        sell_req.save()
        return Response({"status": "Success"})
    except:
        return Response("У данного пользователя нет заявки", status=400)


@api_view(["PUT"])
@permission_classes([IsAuth])
def sendSellRequest(request):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode("utf-8")
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response("Сессия не найдена")

    try:
        sell_req = get_object_or_404(
            SellRequest, id_user=current_user, status="Черновик"
        )
    except:
        return Response("Такой заявки не зарегистрировано")

    sell_req.status = "Сформирована"
    sell_req.date_formation = datetime.now()
    sell_req.save()
    serializer = SellRequestSerializer(sell_req)
    return Response(serializer.data)



@api_view(["PUT"])
@permission_classes([IsManager])
def put_status_admin(request, id):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode("utf-8")
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response("Сессия не найдена")

    if not SellRequest.objects.filter(id=id).exists():
        return Response(f"Заявки с таким id нет")
    sell_req = SellRequest.objects.get(id=id)
    if sell_req.status != "Сформирована":
        return Response("Такой заявки нет на проверке")
    if request.data["status"] not in ["Отклонена", "Завершена"]:
        return Response("Неверный статус!")
    sell_req.status = request.data["status"]
    sell_req.date_completion = datetime.now()
    sell_req.id_moderator = current_user
    sell_req.save()
    serializer = SellRequestSerializer(sell_req)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuth])
def delete_category_from_request(request):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode("utf-8")
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response("Сессия не найдена")
    sell_req = get_object_or_404(
        SellRequest, id_user=current_user, status="Черновик"
    )
    try:
        category = Category.objects.get(id=id, status="Действует")
        req_from_cat = RequestCategory.objects.filter(
            id_request=sell_req
        )
        try:
            sell_req_cat = get_object_or_404(
                RequestCategory, id_request=sell_req, id_category=category
            )
            sell_req_cat.delete()
            if len(req_from_cat) == 0:
                sell_req = get_object_or_404(
                    SellRequest, id_user=current_user, status="Черновик"
                )
                sell_req.status = "Удалена"
                sell_req.save()
            return Response("Категория удалена", status=200)

        except RequestCategory.DoesNotExist:
            return Response("Заявка не найдена", status=404)
    except Category.DoesNotExist:
        return Response("Такого продукта нет", status=400)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    model_class = CustomUser
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        print("req is", request.data)
        if self.model_class.objects.filter(email=request.data["email"]).exists():
            return Response({"status": "Exist"}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.model_class.objects.create_user(
                email=serializer.data["email"],
                password=serializer.data["password"],
                # full_name=serializer.data["full_name"],
                # phone_number=serializer.data["phone_number"],
                is_superuser=serializer.data["is_superuser"],
                is_staff=serializer.data["is_staff"],
            )
            random_key = str(uuid.uuid4())
            session_storage.set(random_key, serializer.data["email"])
            user_data = {
                "email": request.data["email"],
                # "full_name": request.data["full_name"],
                # "phone_number": request.data["phone_number"],
                "is_superuser": False,
            }

            print("user data is ", user_data)
            response = Response(user_data, status=status.HTTP_201_CREATED)
            # response = HttpResponse("{'status': 'ok'}")
            response.set_cookie("session_id", random_key)
            return response
            # return Response({'status': 'Success'}, status=200)
        return Response(
            {"status": "Error", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )



@swagger_auto_schema(method="post", request_body=UserSerializer)
@api_view(["Post"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, email=username, password=password)

    if user is not None:
        print(user)
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        user_data = {
            "id": user.id,
            "email": user.email,
            # "full_name": user.full_name,
            # "phone_number": user.phone_number,
            "password": user.password,
            "is_superuser": user.is_superuser,
        }
        response = Response(user_data, status=status.HTTP_201_CREATED)
        response.set_cookie(
            "session_id", random_key, samesite="Lax", max_age=30 * 24 * 60 * 60
        )
        return response
    else:
        return HttpResponse("login failed", status=400)

@api_view(["POST"])
@permission_classes([IsAuth])
def logout_view(request):
    ssid = request.COOKIES["session_id"]
    if session_storage.exists(ssid):
        session_storage.delete(ssid)
        response_data = {"status": "Success"}
    else:
        response_data = {"status": "Error", "message": "Session does not exist"}
    return Response(response_data)



SECRET_KEY = "pdmw51Doy84"

@csrf_exempt
@require_http_methods(["PUT"])
def UpdateAsync(request, id):
    # Проверка ключа авторизации
    data = json.loads(request.body)
    print(data)
    secret_key = data.get("secretKey")
    if secret_key != SECRET_KEY:
        return JsonResponse({"message": "Неавторизованный запрос"}, status=401)

    try:
        result = data["result"]
        # Обновление статуса заявки
        sell_req = SellRequest.objects.get(id=id)
        sell_req.status_priority = result
        sell_req.save()
        return JsonResponse({"message": "Статус заявки обновлён"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Неверный формат данных"}, status=400)
    except SellRequest.DoesNotExist:
        return JsonResponse({"message": "Заявка не найдена"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

