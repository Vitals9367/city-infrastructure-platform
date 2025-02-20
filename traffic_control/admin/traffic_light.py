from django.contrib.gis import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from enumfields.admin import EnumFieldListFilter

from traffic_control.admin.audit_log import AuditLogHistoryAdmin
from traffic_control.admin.common import TrafficControlOperationInlineBase
from traffic_control.admin.utils import (
    DeviceComparisonAdminMixin,
    ResponsibleEntityPermissionAdminMixin,
    ResponsibleEntityPermissionFilter,
    TreeModelFieldListFilter,
)
from traffic_control.constants import HELSINKI_LATITUDE, HELSINKI_LONGITUDE
from traffic_control.forms import AdminFileWidget
from traffic_control.mixins import (
    EnumChoiceValueDisplayAdminMixin,
    SoftDeleteAdminMixin,
    UserStampedAdminMixin,
    UserStampedInlineAdminMixin,
)
from traffic_control.models import TrafficLightPlan, TrafficLightPlanFile, TrafficLightReal, TrafficLightRealFile

__all__ = (
    "TrafficLightPlanAdmin",
    "TrafficLightPlanFileInline",
    "TrafficLightRealAdmin",
    "TrafficLightRealFileInline",
)

from traffic_control.models.traffic_light import TrafficLightRealOperation


class TrafficLightPlanFileInline(admin.TabularInline):
    formfield_overrides = {
        models.FileField: {"widget": AdminFileWidget},
    }
    model = TrafficLightPlanFile


@admin.register(TrafficLightPlan)
class TrafficLightPlanAdmin(
    ResponsibleEntityPermissionAdminMixin,
    EnumChoiceValueDisplayAdminMixin,
    SoftDeleteAdminMixin,
    UserStampedAdminMixin,
    admin.OSMGeoAdmin,
    AuditLogHistoryAdmin,
):
    default_lon = HELSINKI_LONGITUDE
    default_lat = HELSINKI_LATITUDE
    default_zoom = 12
    fieldsets = (
        (
            _("General information"),
            {
                "fields": (
                    "owner",
                    "responsible_entity",
                    "device_type",
                    "type",
                    "vehicle_recognition",
                    "push_button",
                    "sound_beacon",
                    "txt",
                )
            },
        ),
        (
            _("Location information"),
            {
                "fields": (
                    "location",
                    "direction",
                    "road_name",
                    "lane_number",
                    "lane_type",
                    "location_specifier",
                )
            },
        ),
        (_("Physical properties"), {"fields": ("height", "mount_type")}),
        (_("Related models"), {"fields": ("plan", "mount_plan")}),
        (
            _("Validity"),
            {
                "fields": (
                    ("validity_period_start", "validity_period_end"),
                    "lifecycle",
                )
            },
        ),
        (
            _("Metadata"),
            {"fields": ("created_at", "updated_at", "created_by", "updated_by")},
        ),
    )
    list_display = (
        "id",
        "device_type",
        "txt",
        "lifecycle",
        "location",
    )
    list_filter = SoftDeleteAdminMixin.list_filter + [
        ResponsibleEntityPermissionFilter,
        ("responsible_entity", TreeModelFieldListFilter),
        ("lifecycle", EnumFieldListFilter),
        "owner",
    ]
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "source_name",
        "source_id",
    )
    raw_id_fields = ("plan", "mount_plan")
    ordering = ("-created_at",)
    inlines = (TrafficLightPlanFileInline,)


class TrafficLightRealFileInline(admin.TabularInline):
    formfield_overrides = {
        models.FileField: {"widget": AdminFileWidget},
    }
    model = TrafficLightRealFile


class TrafficLightRealOperationInline(TrafficControlOperationInlineBase):
    model = TrafficLightRealOperation


@admin.register(TrafficLightReal)
class TrafficLightRealAdmin(
    DeviceComparisonAdminMixin,
    ResponsibleEntityPermissionAdminMixin,
    EnumChoiceValueDisplayAdminMixin,
    SoftDeleteAdminMixin,
    UserStampedAdminMixin,
    UserStampedInlineAdminMixin,
    admin.OSMGeoAdmin,
    AuditLogHistoryAdmin,
):
    plan_model_field_name = "traffic_light_plan"
    default_lon = HELSINKI_LONGITUDE
    default_lat = HELSINKI_LATITUDE
    default_zoom = 12
    fieldsets = (
        (
            _("General information"),
            {
                "fields": (
                    "owner",
                    "responsible_entity",
                    "device_type",
                    "type",
                    "vehicle_recognition",
                    "push_button",
                    "sound_beacon",
                    "txt",
                )
            },
        ),
        (
            _("Location information"),
            {
                "fields": (
                    "location",
                    "direction",
                    "road_name",
                    "lane_number",
                    "lane_type",
                    "location_specifier",
                )
            },
        ),
        (_("Physical properties"), {"fields": ("height", "mount_type", "condition")}),
        (_("Related models"), {"fields": ("traffic_light_plan", "mount_real")}),
        (
            _("Installation information"),
            {"fields": ("installation_date", "installation_status")},
        ),
        (
            _("Validity"),
            {
                "fields": (
                    ("validity_period_start", "validity_period_end"),
                    "lifecycle",
                )
            },
        ),
        (
            _("Metadata"),
            {"fields": ("created_at", "updated_at", "created_by", "updated_by")},
        ),
    )
    list_display = (
        "id",
        "device_type",
        "txt",
        "lifecycle",
        "location",
        "installation_date",
    )
    list_filter = SoftDeleteAdminMixin.list_filter + [
        ResponsibleEntityPermissionFilter,
        ("responsible_entity", TreeModelFieldListFilter),
        ("lifecycle", EnumFieldListFilter),
        "owner",
    ]
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "source_name",
        "source_id",
    )
    raw_id_fields = ("traffic_light_plan", "mount_real")
    ordering = ("-created_at",)
    inlines = (TrafficLightRealFileInline, TrafficLightRealOperationInline)
