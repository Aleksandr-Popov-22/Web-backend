from django.contrib import admin
from Server_API import (views)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [

    path(r'categorys/', views.CategorysList.as_view(), name='categorys-list'),
    path(r'categorys/search/', views.search_categorys),
    path(r'categorys/<int:id>/', views.CategorysDetail.as_view(), name='categorys-detail'),
    path(r'categorys/requests/', views.get_requests_category),
    path(r'categorys/<int:id>/add/', views.add_cat_to_req),
    
    path(r'requests/', views.RequestsList.as_view(), name='requests-list'),
    path(r'requests/<int:id>/', views.RequestsDetail.as_view(), name='requests-detail'),
    path(r'requests/<int:id>/categorys/', views.get_categorys_request),
    path(r'requests/<int:id>/put_status_user/', views.put_status_user),
    path(r'requests/<int:id>/put_status_admin/', views.put_status_admin),
    path(r'requests/<int:id_req>/delete_category/<int:id_cat>/', views.delete_category_from_request),
    
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]