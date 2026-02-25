from rest_framework.routers import DefaultRouter

from user.views import CaregiveApiView, PatientApiView

router = DefaultRouter()


router.register(r"patients", PatientApiView, basename="patient")
router.register(r"caregivers", CaregiveApiView, basename="caregiver")

urlpatterns = router.urls
