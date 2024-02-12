from django.contrib import admin
from Server_API import (views)
from django.urls import include, path, re_path
from rest_framework import routers

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [

    path(r'categorys/', views.GetCategory, name='categorys-list'),
    path(r'categorys/new', views.category_post),
    path(r'categorys/<int:id>', views.CategorysDetail.as_view(), name='categorys-detail'),
    path(r'categorys/<int:id>/put', views.category_put),
    path(r'categorys/<int:id>/delete', views.category_delete),
    path(r'categorys/<int:id>/add', views.add_cat_to_req),

    
    path(r'requests/', views.requests_get, name='requests-list'),
    path(r'requests/<int:id>', views.sellrequest_get, name='requests-detail'),
    path(r'requests/delete', views.request_delete),
    path(r'requests/send', views.sendSellRequest, name="sellreq_by_user"),
    path(r'requests/<int:id>/put_admin', views.put_status_admin),
    path(r'requests/<int:id_req>/delete_category/<int:id_cat>', views.delete_category_from_request),
    
    path('', include(router.urls)),
    path('admin', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login',  views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path("put_async/<int:id>", views.UpdateAsync, name="async"),
]