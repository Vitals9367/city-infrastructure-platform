from enumfields.drf import EnumSupportSerializerMixin
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from traffic_control.enums import DeviceTypeTargetModel
from traffic_control.models import (
    BarrierPlan,
    BarrierPlanFile,
    BarrierReal,
    BarrierRealFile,
    OperationType,
    TrafficControlDeviceType,
)
from traffic_control.models.barrier import BarrierRealOperation
from traffic_control.serializers.common import HideFromAnonUserSerializerMixin


class BarrierPlanFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarrierPlanFile
        fields = "__all__"


class BarrierPlanSerializer(
    EnumSupportSerializerMixin,
    HideFromAnonUserSerializerMixin,
    serializers.ModelSerializer,
):
    files = BarrierPlanFileSerializer(many=True, read_only=True)
    device_type = serializers.PrimaryKeyRelatedField(
        queryset=TrafficControlDeviceType.objects.for_target_model(DeviceTypeTargetModel.BARRIER)
    )

    class Meta:
        model = BarrierPlan
        read_only_fields = (
            "created_by",
            "updated_by",
            "deleted_by",
            "deleted_at",
        )
        exclude = ("is_active", "deleted_at", "deleted_by")


class BarrierPlanGeoJSONSerializer(BarrierPlanSerializer):
    location = GeometryField()


class BarrierRealFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarrierRealFile
        fields = "__all__"


class BarrierRealOperationSerializer(serializers.ModelSerializer):
    operation_type = serializers.StringRelatedField()
    operation_type_id = serializers.PrimaryKeyRelatedField(
        queryset=OperationType.objects.filter(barrier=True),
        source="operation_type",
    )

    class Meta:
        model = BarrierRealOperation
        fields = ("id", "operation_type", "operation_type_id", "operation_date")

    def create(self, validated_data):
        # Inject related object to validated data
        barrier_real = BarrierReal.objects.get(pk=self.context["view"].kwargs["barrier_real_pk"])
        validated_data["barrier_real"] = barrier_real
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Inject related object to validated data
        barrier_real = BarrierReal.objects.get(pk=self.context["view"].kwargs["barrier_real_pk"])
        validated_data["barrier_real"] = barrier_real
        return super().update(instance, validated_data)


class BarrierRealSerializer(
    EnumSupportSerializerMixin,
    HideFromAnonUserSerializerMixin,
    serializers.ModelSerializer,
):
    files = BarrierRealFileSerializer(many=True, read_only=True)
    device_type = serializers.PrimaryKeyRelatedField(
        queryset=TrafficControlDeviceType.objects.for_target_model(DeviceTypeTargetModel.BARRIER)
    )
    operations = BarrierRealOperationSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = BarrierReal
        read_only_fields = (
            "created_by",
            "updated_by",
            "deleted_by",
            "deleted_at",
        )
        exclude = ("is_active", "deleted_at", "deleted_by")


class BarrierRealGeoJSONSerializer(BarrierRealSerializer):
    location = GeometryField()
