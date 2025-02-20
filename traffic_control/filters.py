from django.contrib.gis.db.models import GeometryField
from django.utils.translation import gettext_lazy as _
from django_filters import ChoiceFilter, Filter
from django_filters.rest_framework import FilterSet
from rest_framework.exceptions import NotFound
from rest_framework_gis.filters import GeometryFilter

from traffic_control.enums import DeviceTypeTargetModel, TRAFFIC_SIGN_TYPE_CHOICES
from traffic_control.models import (
    AdditionalSignContentPlan,
    AdditionalSignContentReal,
    AdditionalSignPlan,
    AdditionalSignReal,
    AdditionalSignRealOperation,
    BarrierPlan,
    BarrierReal,
    BarrierRealOperation,
    MountPlan,
    MountReal,
    MountRealOperation,
    MountType,
    OperationalArea,
    Owner,
    Plan,
    PortalType,
    ResponsibleEntity,
    RoadMarkingPlan,
    RoadMarkingReal,
    RoadMarkingRealOperation,
    SignpostPlan,
    SignpostReal,
    SignpostRealOperation,
    TrafficControlDeviceType,
    TrafficLightPlan,
    TrafficLightReal,
    TrafficLightRealOperation,
    TrafficSignPlan,
    TrafficSignReal,
    TrafficSignRealOperation,
)


class OperationalAreaFilter(Filter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            operational_area = OperationalArea.objects.filter(id=value).first()
            if operational_area is None:
                raise NotFound({"operational_area": f"Operational area with ID `{value}` was not found."})
            qs = qs.filter(location__contained=operational_area.location)
        return qs


class GenericMeta:
    model = None
    fields = "__all__"
    filter_overrides = {
        GeometryField: {
            "filter_class": GeometryFilter,
            "extra": lambda f: {"lookup_expr": "intersects"},
        },
    }


class AdditionalSignContentPlanFilterSet(FilterSet):
    operational_area = OperationalAreaFilter()

    class Meta(GenericMeta):
        model = AdditionalSignContentPlan


class AdditionalSignContentRealFilterSet(FilterSet):
    operational_area = OperationalAreaFilter()

    class Meta(GenericMeta):
        model = AdditionalSignContentReal


class AdditionalSignPlanFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = AdditionalSignPlan


class AdditionalSignRealFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = AdditionalSignReal


class BarrierPlanFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = BarrierPlan


class BarrierRealFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = BarrierReal


class MountPlanFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = MountPlan


class MountRealFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = MountReal


class MountTypeFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = MountType


class OwnerFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = Owner


class PlanFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = Plan


class PortalTypeFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = PortalType


class RoadMarkingPlanFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = RoadMarkingPlan


class RoadMarkingRealFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = RoadMarkingReal


class SignpostPlanFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = SignpostPlan


class SignpostRealFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = SignpostReal


class TrafficLightPlanFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = TrafficLightPlan


class TrafficLightRealFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = TrafficLightReal


class TrafficControlDeviceTypeFilterSet(FilterSet):
    traffic_sign_type = ChoiceFilter(
        label=_("Traffic sign type"),
        choices=TRAFFIC_SIGN_TYPE_CHOICES,
        method="filter_traffic_sign_type",
    )

    target_model = ChoiceFilter(
        label=_("Target data model"),
        choices=DeviceTypeTargetModel.choices(),
    )

    class Meta(GenericMeta):
        model = TrafficControlDeviceType

    def filter_traffic_sign_type(self, queryset, name, value):
        if value:
            queryset = queryset.filter(code__startswith=value)
        return queryset


class TrafficSignPlanFilterSet(FilterSet):
    operational_area = OperationalAreaFilter()

    class Meta(GenericMeta):
        model = TrafficSignPlan


class TrafficSignRealFilterSet(FilterSet):
    operational_area = OperationalAreaFilter()

    class Meta(GenericMeta):
        model = TrafficSignReal


# Operations
class BarrierRealOperationFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = BarrierRealOperation


class TrafficLightRealOperationFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = TrafficLightRealOperation


class TrafficSignRealOperationFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = TrafficSignRealOperation


class AdditionalSignRealOperationFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = AdditionalSignRealOperation


class MountRealOperationFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = MountRealOperation


class SignpostRealOperationFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = SignpostRealOperation


class RoadMarkingRealOperationFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = RoadMarkingRealOperation


class ResponsibleEntityFilter(Filter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            selected_object = ResponsibleEntity.objects.filter(id=value).first()
            if selected_object is None:
                raise NotFound({"responsible_entity": f"Responsible Entity with ID `{value}` was not found."})

            descendant_ids = selected_object.get_descendants(include_self=True).values_list("id", flat=True).distinct()
            qs = qs.filter(responsible_entity__id__in=descendant_ids)
        return qs


class ResponsibleEntityFilterSet(FilterSet):
    class Meta(GenericMeta):
        model = ResponsibleEntity
