from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from traffic_control.enums import Lifecycle
from traffic_control.models import MountPlan, MountReal, MountType, Owner, Plan, PortalType, ResponsibleEntity
from traffic_control.resources.common import (
    GenericDeviceBaseResource,
    ResourceEnumIntegerField,
    ResponsibleEntityPermissionImportMixin,
)


class AbstractMountResource(ResponsibleEntityPermissionImportMixin, GenericDeviceBaseResource):
    lifecycle = ResourceEnumIntegerField(attribute="lifecycle", enum=Lifecycle, default=Lifecycle.ACTIVE)
    owner__name_fi = Field(attribute="owner", column_name="owner__name_fi", widget=ForeignKeyWidget(Owner, "name_fi"))
    responsible_entity__name = Field(
        attribute="responsible_entity",
        column_name="responsible_entity__name",
        widget=ForeignKeyWidget(ResponsibleEntity, "name"),
    )
    mount_type__code = Field(
        attribute="mount_type", column_name="mount_type__code", widget=ForeignKeyWidget(MountType, "code")
    )
    portal_type__id = Field(
        attribute="portal_type", column_name="portal_type__id", widget=ForeignKeyWidget(PortalType, "id")
    )

    class Meta(GenericDeviceBaseResource.Meta):
        common_fields = (
            "id",
            "owner__name_fi",
            "responsible_entity__name",
            "lifecycle",
            "location",
            "height",
            "mount_type__code",
            "base",
            "portal_type__id",
            "material",
            "validity_period_start",
            "validity_period_end",
            "txt",
            "electric_accountable",
            "is_foldable",
            "cross_bar_length",
        )


class MountPlanResource(AbstractMountResource):
    plan__plan_number = Field(
        attribute="plan",
        column_name="plan__plan_number",
        widget=ForeignKeyWidget(Plan, "plan_number"),
    )

    class Meta(AbstractMountResource.Meta):
        model = MountPlan

        fields = AbstractMountResource.Meta.common_fields + ("plan__plan_number",)
        export_order = fields


class MountRealResource(AbstractMountResource):
    mount_plan__id = Field(
        attribute="mount_plan",
        column_name="mount_plan__id",
        widget=ForeignKeyWidget(MountPlan, "id"),
    )

    class Meta(AbstractMountResource.Meta):
        model = MountReal

        fields = AbstractMountResource.Meta.common_fields + (
            "inspected_at",
            "diameter",
            "mount_plan__id",
        )
        export_order = fields
