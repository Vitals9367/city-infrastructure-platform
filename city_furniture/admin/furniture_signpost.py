from django.contrib.gis import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from enumfields.admin import EnumFieldListFilter

from city_furniture.forms import FurnitureSignpostPlanModelForm, FurnitureSignpostRealModelForm
from city_furniture.models import (
    FurnitureSignpostPlan,
    FurnitureSignpostPlanFile,
    FurnitureSignpostReal,
    FurnitureSignpostRealFile,
    FurnitureSignpostRealOperation,
)
from city_furniture.resources.furniture_signpost import (
    FurnitureSignpostPlanResource,
    FurnitureSignpostPlanTemplateResource,
    FurnitureSignpostRealResource,
)
from traffic_control.admin.audit_log import AuditLogHistoryAdmin
from traffic_control.admin.common import OperationalAreaListFilter, TrafficControlOperationInlineBase
from traffic_control.admin.utils import (
    DeviceComparisonAdminMixin,
    MultiResourceExportActionAdminMixin,
    ResponsibleEntityPermissionAdminMixin,
    ResponsibleEntityPermissionFilter,
    SimplifiedRelatedFieldListFilter,
    TreeModelFieldListFilter,
)
from traffic_control.constants import HELSINKI_LATITUDE, HELSINKI_LONGITUDE
from traffic_control.forms import AdminFileWidget
from traffic_control.mixins import (
    EnumChoiceValueDisplayAdminMixin,
    Point3DFieldAdminMixin,
    SoftDeleteAdminMixin,
    UserStampedAdminMixin,
    UserStampedInlineAdminMixin,
)
from traffic_control.resources.common import CustomImportExportActionModelAdmin

__all__ = (
    "FurnitureSignpostPlanAdmin",
    "FurnitureSignpostPlanFileInline",
    "FurnitureSignpostRealAdmin",
    "FurnitureSignpostRealFileInline",
)


class FurnitureSignpostPlanFileInline(admin.TabularInline):
    formfield_overrides = {models.FileField: {"widget": AdminFileWidget}}
    model = FurnitureSignpostPlanFile


class FurnitureSignpostRealFileInline(admin.TabularInline):
    formfield_overrides = {models.FileField: {"widget": AdminFileWidget}}
    model = FurnitureSignpostRealFile


class FurnitureSignpostRealOperationInline(TrafficControlOperationInlineBase):
    model = FurnitureSignpostRealOperation


class AbstractFurnitureSignpostAdmin(
    ResponsibleEntityPermissionAdminMixin,
    EnumChoiceValueDisplayAdminMixin,
    SoftDeleteAdminMixin,
    UserStampedAdminMixin,
    Point3DFieldAdminMixin,
    admin.OSMGeoAdmin,
    AuditLogHistoryAdmin,
    CustomImportExportActionModelAdmin,
):
    default_lon = HELSINKI_LONGITUDE
    default_lat = HELSINKI_LATITUDE
    default_zoom = 12

    ordering = ("-created_at",)
    list_filter = SoftDeleteAdminMixin.list_filter + [
        ResponsibleEntityPermissionFilter,
        ("responsible_entity", TreeModelFieldListFilter),
        ("owner", SimplifiedRelatedFieldListFilter),
        ("target", SimplifiedRelatedFieldListFilter),
        ("device_type", SimplifiedRelatedFieldListFilter),
        ("lifecycle", EnumFieldListFilter),
        OperationalAreaListFilter,
        ("created_by", SimplifiedRelatedFieldListFilter),
        "validity_period_start",
    ]
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "source_name",
        "source_id",
    )
    list_display = (
        "id",
        "device_type",
        "location_name_fi",
        "lifecycle",
    )
    _fieldset_general_information = (
        _("General information"),
        {
            "fields": (
                "owner",
                "responsible_entity",
                "device_type",
                "target",
                "mount_type",
                "additional_material_url",
                "source_id",
                "source_name",
            )
        },
    )
    _fieldset_location_information = (
        _("Location information"),
        {
            "fields": (
                ("location", "z_coord"),
                "location_name_fi",
                "location_name_sw",
                "location_name_en",
                "location_additional_info",
                "direction",
                "height",
            )
        },
    )
    _fieldset_physical_properties = (
        _("Content and physical properties"),
        {
            "fields": (
                "arrow_direction",
                "color",
                "pictogram",
                "value",
                "text_content_fi",
                "text_content_sw",
                "text_content_en",
                "content_responsible_entity",
                "size",
            )
        },
    )
    _fieldset_validity = (
        _("Validity"),
        {
            "fields": (
                "validity_period_start",
                "validity_period_end",
                "lifecycle",
            )
        },
    )
    _fieldset_metadata = (
        _("Metadata"),
        {"fields": (("created_at", "updated_at", "created_by", "updated_by"),)},
    )


@admin.register(FurnitureSignpostPlan)
class FurnitureSignpostPlanAdmin(MultiResourceExportActionAdminMixin, AbstractFurnitureSignpostAdmin):
    resource_class = FurnitureSignpostPlanResource
    extra_export_resource_classes = [
        FurnitureSignpostPlanTemplateResource,
    ]
    form = FurnitureSignpostPlanModelForm
    fieldsets = (
        AbstractFurnitureSignpostAdmin._fieldset_general_information,
        AbstractFurnitureSignpostAdmin._fieldset_location_information,
        AbstractFurnitureSignpostAdmin._fieldset_physical_properties,
        (_("Related models"), {"fields": ("plan", "mount_plan", "parent")}),
        AbstractFurnitureSignpostAdmin._fieldset_validity,
        AbstractFurnitureSignpostAdmin._fieldset_metadata,
    )
    raw_id_fields = ("plan", "mount_plan")
    list_filter = AbstractFurnitureSignpostAdmin.list_filter
    inlines = (FurnitureSignpostPlanFileInline,)


@admin.register(FurnitureSignpostReal)
class FurnitureSignpostRealAdmin(
    DeviceComparisonAdminMixin,
    UserStampedInlineAdminMixin,
    AbstractFurnitureSignpostAdmin,
):
    plan_model_field_name = "furniture_signpost_plan"
    resource_class = FurnitureSignpostRealResource
    form = FurnitureSignpostRealModelForm
    fieldsets = (
        AbstractFurnitureSignpostAdmin._fieldset_general_information,
        AbstractFurnitureSignpostAdmin._fieldset_location_information,
        AbstractFurnitureSignpostAdmin._fieldset_physical_properties,
        (_("Related models"), {"fields": ("furniture_signpost_plan", "mount_real", "parent")}),
        (
            _("Installation information"),
            {
                "fields": (
                    "installation_date",
                    "installation_status",
                    "condition",
                ),
            },
        ),
        AbstractFurnitureSignpostAdmin._fieldset_validity,
        AbstractFurnitureSignpostAdmin._fieldset_metadata,
    )
    raw_id_fields = ("furniture_signpost_plan", "mount_real")
    list_filter = AbstractFurnitureSignpostAdmin.list_filter + [
        ("condition", EnumFieldListFilter),
        "installation_date",
    ]
    search_fields = (
        "value",
        "size",
        "height",
        "source_id",
        "source_name",
        "text_content_fi",
        "text_content_sw",
        "text_content_en",
        "location_name_fi",
        "location_name_en",
        "location_name_sw",
    )
    inlines = (FurnitureSignpostRealFileInline, FurnitureSignpostRealOperationInline)
