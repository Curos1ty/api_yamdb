from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import send_mail, UserViewSet, create_token

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/users/', UserViewSet),
    path('v1/auth/signup/', send_mail),
    path('v1/auth/token/', create_token),
]
