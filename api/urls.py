from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovimientoFinancieroViewSet, inicio, registro_usuario
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'movimientos', MovimientoFinancieroViewSet, basename='movimiento')

urlpatterns = [
    path('', inicio, name='inicio'),
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/registro/', registro_usuario, name='registro_usuario'),
] 