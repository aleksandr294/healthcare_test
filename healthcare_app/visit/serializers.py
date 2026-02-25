from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from duty.enums import DutyResultStatusChoices
from duty.models import Duty, DutyResult
from duty.serializers import DutySerializer
from user.serializers import UserSerializer
from visit import constants
from visit.constants import MAX_DUTIES
from visit.enums import VisitStatusChoices
from visit.models import Visit


class CreateUpdateVisitSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("patient", "duties", "start_date_time", "description")
        model = Visit

    def validate_start_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(constants.ERROR_START_DATETIME)
        return value

    def validate_duties(self, value):
        if len(value) > MAX_DUTIES:
            raise serializers.ValidationError(constants.ERROR_DUTY_COUNT)
        return value

    def validate_patient(self, value):
        if value.is_staff:
            raise serializers.ValidationError(constants.ERROR_PATIENT)
        return value

    def validate(self, attrs):
        end_date_time = attrs["start_date_time"]

        for duty in attrs["duties"]:
            end_date_time += duty.duration

        attrs["end_date_time"] = end_date_time
        attrs["caregiver"] = self.context["extra_data"]["user"]

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            number = str(instance.pk).zfill(4)
            instance.number = number
            instance.save()
            return instance

    def update(self, instance, validated_data):
        duties = validated_data.pop("duties")

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            end_date_time = instance.start_date_time

            for duty in duties:
                end_date_time += duty.duration

            instance.end_date_time = end_date_time

            instance.save()
            instance.duties.all().delete()
            instance.duties.set(duties)


class VisitSerializer(serializers.ModelSerializer):
    patient = UserSerializer()
    caregiver = UserSerializer()
    duties = DutySerializer(many=True)

    class Meta:
        fields = (
            "id",
            "patient",
            "caregiver",
            "duties",
            "start_date_time",
            "end_date_time",
            "description",
        )
        model = Visit


class EnterDutyResultListSerializer(serializers.ListSerializer):

    def validate(self, data):
        visit = self.context["extra_data"]["visit"]

        duty_ids_from_request = [item["duty_id"].id for item in data]
        duty_ids_from_visit = set(visit.duties.values_list("id", flat=True))

        missing = set(duty_ids_from_request) - duty_ids_from_visit
        if missing:
            raise serializers.ValidationError({"id": constants.DUTIES_NOT_FOUND.format(missing)})

        if len(duty_ids_from_request) != len(set(duty_ids_from_request)):
            raise serializers.ValidationError(constants.DUPLICATE_DUTIES)

        return data

    def create(self, validated_data):
        visit = self.context["extra_data"]["visit"]
        duty_results = [DutyResult(visit=visit, duty=item["duty_id"], status=item["status"]) for item in validated_data]
        return DutyResult.objects.bulk_create(duty_results)

    def save(self, **kwargs):
        with transaction.atomic():
            instances = super().save(**kwargs)
            visit = self.context["extra_data"]["visit"]

            if not visit.duty_results.filter(status=DutyResultStatusChoices.NOT_DONE).exists():
                visit.status = VisitStatusChoices.COMPLETED
                visit.save()

            return instances


class EnterDutyResultSerializer(serializers.Serializer):
    duty_id = PrimaryKeyRelatedField(queryset=Duty.objects.all())
    status = serializers.CharField()

    class Meta:
        list_serializer_class = EnterDutyResultListSerializer


class DutyResults(serializers.ModelSerializer):
    duty = DutySerializer()
    status = serializers.CharField()

    class Meta:
        model = DutyResult
        fields = ("id", "duty", "status")
