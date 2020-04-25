from .auth import urls as urls_auth
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AporteModelViewSet

app_name = 'api'

router = SimpleRouter()
router.register("aporte", AporteModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(urls_auth)),

]
