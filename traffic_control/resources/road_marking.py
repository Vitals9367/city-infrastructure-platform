from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from traffic_control.enums import Condition, Lifecycle
from traffic_control.models import (
    MountPlan,
    Owner,
    Plan,
    ResponsibleEntity,
    RoadMarkingPlan,
    RoadMarkingReal,
    TrafficControlDeviceType,
    TrafficSignReal,
)
from traffic_control.models.road_marking import LocationSpecifier, RoadMarkingColor
from traffic_control.resources.common import (
    GenericDeviceBaseResource,
    ResourceEnumIntegerField,
    ResponsibleEntityPermissionImportMixin,
)


class AbstractRoadMarkingResource(ResponsibleEntityPermissionImportMixin, GenericDeviceBaseResource):
    lifecycle = ResourceEnumIntegerField(attribute="lifecycle", enum=Lifecycle, default=Lifecycle.ACTIVE)
    owner__name_fi = Field(attribute="owner", column_name="owner__name_fi", widget=ForeignKeyWidget(Owner, "name_fi"))
    responsible_entity__name = Field(
        attribute="responsible_entity",
        column_name="responsible_entity__name",
        widget=ForeignKeyWidget(ResponsibleEntity, "name"),
    )
    device_type__code = Field(
        attribute="device_type",
        column_name="device_type__code",
        widget=ForeignKeyWidget(TrafficControlDeviceType, "code"),
    )
    location_specifier = ResourceEnumIntegerField(
        attribute="location_specifier",
        enum=LocationSpecifier,
        default=LocationSpecifier.RIGHT_SIDE_OF_LANE,
    )
    color = ResourceEnumIntegerField(attribute="color", enum=RoadMarkingColor, default=RoadMarkingColor.WHITE)

    class Meta(GenericDeviceBaseResource.Meta):
        common_fields = (
            "id",
            "owner__name_fi",
            "responsible_entity__name",
            "lifecycle",
            "location",
            "road_name",
            "lane_number",
            "lane_type",
            "location_specifier",
            "line_direction",
            "device_type__code",
            "arrow_direction",
            "value",
            "material",
            "color",
            "type_specifier",
            "validity_period_start",
            "validity_period_end",
            "seasonal_validity_period_start",
            "seasonal_validity_period_end",
            "symbol",
            "size",
            "length",
            "width",
            "is_raised",
            "is_grinded",
            "additional_info",
            "amount",
        )


class RoadMarkingPlanResource(AbstractRoadMarkingResource):
    mount_plan__id = Field(
        attribute="mount_plan",
        column_name="mount_plan__id",
        widget=ForeignKeyWidget(MountPlan, "id"),
    )
    plan__plan_number = Field(
        attribute="plan",
        column_name="plan__plan_number",
        widget=ForeignKeyWidget(Plan, "plan_number"),
    )

    class Meta(AbstractRoadMarkingResource.Meta):
        model = RoadMarkingPlan

        fields = AbstractRoadMarkingResource.Meta.common_fields + (
            "mount_plan__id",
            "plan__plan_number",
        )
        export_order = fields


class RoadMarkingRealResource(AbstractRoadMarkingResource):
    condition = ResourceEnumIntegerField(attribute="condition", enum=Condition, default=Condition.VERY_GOOD)
    road_marking_plan__id = Field(
        attribute="road_marking_plan",
        column_name="road_marking_plan__id",
        widget=ForeignKeyWidget(RoadMarkingPlan, "id"),
    )
    traffic_sign_real__id = Field(
        attribute="traffic_sign_real",
        column_name="traffic_sign_real__id",
        widget=ForeignKeyWidget(TrafficSignReal, "id"),
    )

    class Meta(AbstractRoadMarkingResource.Meta):
        model = RoadMarkingReal

        fields = AbstractRoadMarkingResource.Meta.common_fields + (
            "condition",
            "installation_date",
            "road_marking_plan__id",
            "traffic_sign_real__id",
            "missing_traffic_sign_real_txt",
        )
        export_order = fields
