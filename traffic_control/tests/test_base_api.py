from django.conf import settings
from django.contrib.gis.geos import LineString, MultiPolygon, Point, Polygon
from rest_framework.test import APITestCase

from traffic_control.enums import Lifecycle
from traffic_control.models import MountType, Owner, TrafficControlDeviceType
from users.models import User

test_point = Point(10.0, 10.0, 0.0, srid=settings.SRID)
test_point_2 = Point(0.0, 0.0, 0.0, srid=settings.SRID)
test_point_3 = Point(100.0, 100.0, 0.0, srid=settings.SRID)
test_point_4 = Point(-44.3, 60.1, 0.0, srid=4326)
test_line = LineString((0.0, 0.0, 0.0), (50.0, 0.0, 0.0), srid=settings.SRID)
test_line_2 = LineString((20.0, 20.0, 0.0), (30.0, 30.0, 0.0), srid=settings.SRID)
test_line_3 = LineString((40.0, 40.0, 0.0), (60.0, 60.0, 0.0), srid=settings.SRID)
test_line_4 = LineString((500.0, 500.0, 0.0), (500.0, 550.0, 0.0), srid=settings.SRID)
test_polygon = Polygon(
    (
        (0.0, 0.0, 0.0),
        (0.0, 50.0, 0.0),
        (50.0, 50.0, 0.0),
        (50.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    ),
    srid=settings.SRID,
)
test_polygon_2 = Polygon(
    (
        (1000.0, 1000.0, 0.0),
        (1000.0, 1050.0, 0.0),
        (1050.0, 1050.0, 0.0),
        (1050.0, 1000.0, 0.0),
        (1000.0, 1000.0, 0.0),
    ),
    srid=settings.SRID,
)
test_polygon_3 = Polygon(
    (
        (100.0, 100.0, 0.0),
        (100.0, 150.0, 0.0),
        (150.0, 150.0, 0.0),
        (150.0, 100.0, 0.0),
        (100.0, 100.0, 0.0),
    ),
    srid=settings.SRID,
)
test_multi_polygon = MultiPolygon(test_polygon, test_polygon_2, srid=settings.SRID)

point_location_test_data = [
    (test_point, test_polygon, 1),
    (test_point_2, test_polygon, 1),
    (test_point_3, test_polygon, 0),
    (test_point_4, test_polygon, 0),
    (test_point, test_polygon_2, 0),
    (test_point_2, test_polygon_2, 0),
    (test_point_3, test_polygon_2, 0),
]

point_location_error_test_data = [
    (test_point, "invalid_test_string", "Virheellinen geometria-arvo."),
    (test_point, 123123, "Virheellinen geometria-arvo."),
]

line_location_test_data = [
    (test_line, test_polygon, 1),
    (test_line_2, test_polygon, 1),
    (test_line_3, test_polygon, 1),
    (test_line_4, test_polygon, 0),
    (test_line, test_polygon_2, 0),
    (test_line_2, test_polygon_2, 0),
    (test_line_3, test_polygon_2, 0),
    (test_line_4, test_polygon_2, 0),
]

line_location_error_test_data = [
    (test_line, "invalid_test_string", "Virheellinen geometria-arvo."),
    (test_line, 123123, "Virheellinen geometria-arvo."),
]


class TrafficControlAPIBaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="testpw", email="testuser@example.com")
        self.client.login(username="testuser", password="testpw")
        self.test_lifecycle = Lifecycle.ACTIVE
        self.test_lifecycle_2 = Lifecycle.INACTIVE
        self.test_device_type = TrafficControlDeviceType.objects.create(code="A11", description="Speed limit")
        self.test_device_type_2 = TrafficControlDeviceType.objects.create(code="A12", description="Weight limit")
        self.test_mount_type = MountType.objects.create(code="PORTAL", description="Portal")
        self.test_mount_type_2 = MountType.objects.create(code="WALL", description="Wall")
        self.test_point = test_point
        self.test_point_2 = test_point_2
        self.test_owner = Owner.objects.create(name_fi="Helsingin kaupunki", name_en="City of Helsinki")
