# from django.urls import path
# from .views import *

# urlpatterns = [
#             path('aporte/<int:pk>', AporteDeleteUpdate.as_view()),
#             path('aporte/', AporteView.as_view()),
# ]


from rest_framework.routers import SimpleRouter
from .views import AporteModelViewSet#, CorrigeModelViewSet

router = SimpleRouter()
router.register("aporte", AporteModelViewSet)
# router.register("corrige", CorrigeModelViewSet)


urlpatterns = router.urls