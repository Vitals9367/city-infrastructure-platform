from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers

from traffic_control.models import (
    BarrierPlan,
    BarrierReal,
    MountPlan,
    MountReal,
    RoadMarkingPlan,
    RoadMarkingReal,
    SignpostPlan,
    SignpostReal,
    TrafficLightPlan,
    TrafficLightReal,
    TrafficSignCode,
    TrafficSignPlan,
    TrafficSignReal,
)


class TrafficLightPlanSerializer(
    EnumSupportSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = TrafficLightPlan
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class TrafficLightRealSerializer(
    EnumSupportSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = TrafficLightReal
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class TrafficSignPlanSerializer(
    EnumSupportSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = TrafficSignPlan
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class TrafficSignRealSerializer(
    EnumSupportSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = TrafficSignReal
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class SignpostPlanSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = SignpostPlan
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class SignpostRealSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = SignpostReal
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class MountPlanSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MountPlan
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class MountRealSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MountReal
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class BarrierPlanSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = BarrierPlan
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class BarrierRealSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = BarrierReal
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class RoadMarkingPlanSerializer(
    EnumSupportSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = RoadMarkingPlan
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class RoadMarkingRealSerializer(
    EnumSupportSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = RoadMarkingReal
        fields = "__all__"
        read_only_fields = ("created_by", "updated_by", "deleted_by", "deleted_at")


class TrafficSignCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficSignCode
        fields = "__all__"
