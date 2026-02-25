from rest_framework.routers import DefaultRouter

from visit.views import VisitViewSet

router = DefaultRouter()


router.register(r"", VisitViewSet, basename="currency")

urlpatterns = router.urls
