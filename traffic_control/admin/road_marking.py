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
from traffic_control.models import RoadMarkingPlan, RoadMarkingPlanFile, RoadMarkingReal, RoadMarkingRealFile

__all__ = (
    "RoadMarkingPlanAdmin",
    "RoadMarkingPlanFileInline",
    "RoadMarkingRealAdmin",
    "RoadMarkingRealFileInline",
)

from traffic_control.models.road_marking import RoadMarkingRealOperation


class RoadMarkingPlanFileInline(admin.TabularInline):
    formfield_overrides = {
        models.FileField: {"widget": AdminFileWidget},
    }
    model = RoadMarkingPlanFile


@admin.register(RoadMarkingPlan)
class RoadMarkingPlanAdmin(
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
                    "type_specifier",
                    "value",
                    "symbol",
                    "amount",
                    "additional_info",
                    "source_id",
                    "source_name",
                )
            },
        ),
        (
            _("Location information"),
            {
                "fields": (
                    "location",
                    "road_name",
                    "lane_number",
                    "lane_type",
                    "location_specifier",
                )
            },
        ),
        (
            _("Physical properties"),
            {
                "fields": (
                    "arrow_direction",
                    "line_direction",
                    "size",
                    "length",
                    "width",
                    "is_raised",
                    "is_grinded",
                    "material",
                    "color",
                )
            },
        ),
        (_("Related models"), {"fields": ("plan", "traffic_sign_plan")}),
        (
            _("Validity"),
            {
                "fields": (
                    ("validity_period_start", "validity_period_end"),
                    ("seasonal_validity_period_start", "seasonal_validity_period_end"),
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
    raw_id_fields = ("plan", "traffic_sign_plan")
    ordering = ("-created_at",)
    inlines = (RoadMarkingPlanFileInline,)


class RoadMarkingRealFileInline(admin.TabularInline):
    formfield_overrides = {
        models.FileField: {"widget": AdminFileWidget},
    }
    model = RoadMarkingRealFile


class RoadMarkingRealOperationInline(TrafficControlOperationInlineBase):
    model = RoadMarkingRealOperation


@admin.register(RoadMarkingReal)
class RoadMarkingRealAdmin(
    DeviceComparisonAdminMixin,
    ResponsibleEntityPermissionAdminMixin,
    EnumChoiceValueDisplayAdminMixin,
    SoftDeleteAdminMixin,
    UserStampedAdminMixin,
    UserStampedInlineAdminMixin,
    admin.OSMGeoAdmin,
    AuditLogHistoryAdmin,
):
    plan_model_field_name = "road_marking_plan"
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
                    "type_specifier",
                    "value",
                    "symbol",
                    "amount",
                    "additional_info",
                    "missing_traffic_sign_real_txt",
                    "source_id",
                    "source_name",
                )
            },
        ),
        (
            _("Location information"),
            {
                "fields": (
                    "location",
                    "road_name",
                    "lane_number",
                    "lane_type",
                    "location_specifier",
                )
            },
        ),
        (
            _("Physical properties"),
            {
                "fields": (
                    "arrow_direction",
                    "line_direction",
                    "size",
                    "length",
                    "width",
                    "is_raised",
                    "is_grinded",
                    "material",
                    "color",
                    "condition",
                )
            },
        ),
        (_("Related models"), {"fields": ("road_marking_plan", "traffic_sign_real")}),
        (
            _("Installation information"),
            {"fields": ("installation_date", "installation_status")},
        ),
        (
            _("Validity"),
            {
                "fields": (
                    ("validity_period_start", "validity_period_end"),
                    ("seasonal_validity_period_start", "seasonal_validity_period_end"),
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
    raw_id_fields = ("road_marking_plan", "traffic_sign_real")
    ordering = ("-created_at",)
    inlines = (RoadMarkingRealFileInline, RoadMarkingRealOperationInline)
