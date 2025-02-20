from django.contrib.admin import SimpleListFilter
from django.contrib.gis import admin
from django.utils.translation import gettext_lazy as _

from traffic_control.models import OperationalArea, OperationType


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "traffic_sign",
        "additional_sign",
        "road_marking",
        "barrier",
        "signpost",
        "traffic_light",
        "mount",
    )


class TrafficControlOperationInlineBase(admin.TabularInline):
    extra = 0
    readonly_fields = ("created_by", "created_at", "updated_by", "updated_at")


class OperationalAreaListFilter(SimpleListFilter):
    title = _("Operational area")
    parameter_name = "operational_area"

    def lookups(self, request, model_admin):
        return OperationalArea.objects.values_list("id", "name")

    def queryset(self, request, queryset):
        if self.value():
            operational_area = OperationalArea.objects.get(id=self.value())
            return queryset.filter(location__contained=operational_area.location)
