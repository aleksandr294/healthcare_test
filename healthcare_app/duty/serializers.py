from rest_framework import serializers

from duty.models import Duty


class DutySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "duration")
        model = Duty
