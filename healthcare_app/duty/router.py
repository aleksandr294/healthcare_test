from rest_framework.routers import DefaultRouter

from duty.views import DutyApiView

router = DefaultRouter()


router.register(r"", DutyApiView, basename="duty")
urlpatterns = router.urls
