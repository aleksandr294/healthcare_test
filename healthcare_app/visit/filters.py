from django_filters import rest_framework as filters

from visit.models import Visit


class VisitFilterSet(filters.FilterSet):
    number = filters.CharFilter(field_name="number", lookup_expr="exact")
    caregiver_full_name = filters.CharFilter(field_name="caregiver__full_name", lookup_expr="ilike")
    patient_full_name = filters.CharFilter(field_name="patient__full_name", lookup_expr="ilike")
    status = filters.CharFilter(field_name="status", lookup_expr="icontains")
    date = filters.DateFromToRangeFilter(method="filter_by_date")

    def filter_by_date(self, queryset, name, value):
        if not value:
            return queryset

        start = value.start
        end = value.stop

        if start and end:
            return queryset.filter(start_date_time__lte=end, end_date_time__gte=start)

        if start:
            return queryset.filter(end_date_time__gte=start)

        if end:
            return queryset.filter(start_date_time__lte=end)

        return queryset

    class Meta:
        model = Visit
        fields = ("number", "caregiver_full_name", "patient_full_name", "status")
