from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from user.emums import UserRoleChoices
from user.models import User
from user.serializers import UserSerializer

# Create your views here.


class PatientApiView(ListAPIView, GenericViewSet):
    queryset = User.objects.filter(role=UserRoleChoices.PATIENT)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CaregiveApiView(ListAPIView, GenericViewSet):
    queryset = User.objects.filter(role=UserRoleChoices.CAREGIVER)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
