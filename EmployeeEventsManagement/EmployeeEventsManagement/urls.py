from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path

urlpatterns = [
    path('api_v1/', include("api_v1.urls")),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
