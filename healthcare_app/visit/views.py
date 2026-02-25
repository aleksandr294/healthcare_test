from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.permissions import IsPatient, IsStaff
from visit.enums import VisitStatusChoices
from visit.filters import VisitFilterSet
from visit.models import Visit
from visit.serializers import (
    CreateUpdateVisitSerializer,
    DutyResults,
    EnterDutyResultSerializer,
    VisitSerializer,
)

# Create your views here.


class VisitViewSet(viewsets.ModelViewSet):
    SERIALIZERS = {
        "list": VisitSerializer,
        "create": CreateUpdateVisitSerializer,
        "update": CreateUpdateVisitSerializer,
        "enter_duty_results": EnterDutyResultSerializer,
        "duty_results": DutyResults,
    }
    PERMISSIONS = {
        "list": [IsStaff | IsPatient],
        "create": [IsStaff],
        "update": [IsStaff],
        "partial_update": [IsStaff],
        "destroy": [IsStaff],
        "enter_duty_results": [IsStaff],
        "duty_results": [IsStaff | IsPatient],
    }
    queryset = (
        Visit.objects.select_related("patient", "caregiver")
        .prefetch_related("duties")
        .filter(archived_stamp__isnull=True)
    )
    filterset_class = VisitFilterSet
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        return self.SERIALIZERS.get(self.action, VisitSerializer)

    def get_permissions(self):
        return [permission() for permission in self.PERMISSIONS.get(self.action, [IsAuthenticated])]

    def get_serializer_context(self):
        context = super(VisitViewSet, self).get_serializer_context()

        if self.request.user:
            context["extra_data"] = {"user": self.request.user}

        return context

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == VisitStatusChoices.COMPLETED:
            instance.archived_stamp = timezone.now()
            instance.save()
            instance.duty_results.all().update(archived_stamp=timezone.now())
            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            return queryset.filter(patient=self.request.user)

        return queryset.filter(caregiver=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        url_path="enter-duty-results",
        url_name="enter-duty-results",
    )
    @extend_schema(
        request=EnterDutyResultSerializer(many=True),
        responses=EnterDutyResultSerializer(many=True),
    )
    def enter_duty_results(self, request, *args, **kwargs):
        visit = self.get_object()
        serializer_class = self.get_serializer_class()

        context = self.get_serializer_context()
        context["extra_data"].update({"visit": visit})

        serializer = serializer_class(data=request.data, many=True, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="duty-results", url_name="duty-results")
    @extend_schema(responses=DutyResults(many=True))
    def duty_results(self, request, *args, **kwargs):
        visit = self.get_object()
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(visit.duty_results.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
