from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from duty.models import Duty
from duty.serializers import DutySerializer

# Create your views here.


class DutyApiView(ListAPIView, GenericViewSet):
    queryset = Duty.objects.all()
    serializer_class = DutySerializer
    permission_classes = [IsAuthenticated]
