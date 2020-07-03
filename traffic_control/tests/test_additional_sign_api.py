from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_gis.fields import GeoJsonDict

from traffic_control.models import (
    AdditionalSignContentPlan,
    AdditionalSignContentReal,
    AdditionalSignPlan,
    AdditionalSignReal,
)

from .factories import (
    get_additional_sign_content_plan,
    get_additional_sign_content_real,
    get_additional_sign_plan,
    get_additional_sign_real,
    get_api_client,
    get_traffic_control_device_type,
    get_traffic_sign_plan,
    get_traffic_sign_real,
    get_user,
)

# AdditionalSignPlan tests
# ===============================================


@pytest.mark.parametrize("geo_format", ("", "geojson"))
@pytest.mark.django_db
def test__additional_sign_plan__list(geo_format):
    client = get_api_client()
    for owner in ["foo", "bar", "baz"]:
        asp = get_additional_sign_plan(owner=owner)
        get_additional_sign_content_plan(parent=asp)

    response = client.get(
        reverse("v1:additionalsignplan-list"), data={"geo_format": geo_format}
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["count"] == 3
    for result in response_data["results"]:
        obj = AdditionalSignPlan.objects.get(pk=result["id"])
        assert result["content"][0]["id"] == str(obj.content.first().pk)

        if geo_format == "geojson":
            assert result["location"] == GeoJsonDict(obj.location.json)
            assert result["affect_area"] == GeoJsonDict(obj.affect_area.json)
        else:
            assert result["location"] == obj.location.ewkt
            assert result["affect_area"] == obj.affect_area.ewkt


@pytest.mark.parametrize("geo_format", ("", "geojson"))
@pytest.mark.django_db
def test__additional_sign_plan__detail(geo_format):
    client = get_api_client()
    asp = get_additional_sign_plan()
    ascp = get_additional_sign_content_plan(parent=asp)

    response = client.get(
        reverse("v1:additionalsignplan-detail", kwargs={"pk": asp.pk}),
        data={"geo_format": geo_format},
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["id"] == str(asp.pk)
    assert response_data["parent"] == str(asp.parent.pk)
    assert response_data["content"][0]["id"] == str(ascp.pk)

    if geo_format == "geojson":
        assert response_data["location"] == GeoJsonDict(asp.location.json)
        assert response_data["affect_area"] == GeoJsonDict(asp.affect_area.json)
    else:
        assert response_data["location"] == asp.location.ewkt
        assert response_data["affect_area"] == asp.affect_area.ewkt


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_plan__create(admin_user):
    client = get_api_client(user=get_user(admin=admin_user))
    traffic_sign_plan = get_traffic_sign_plan()
    data = {
        "parent": traffic_sign_plan.pk,
        "location": str(traffic_sign_plan.location),
        "decision_date": "2020-01-02",
        "owner": "City of Helsinki",
    }

    response = client.post(reverse("v1:additionalsignplan-list"), data=data)
    response_data = response.json()

    if admin_user:
        assert response.status_code == status.HTTP_201_CREATED
        assert AdditionalSignPlan.objects.count() == 1
        assert response_data["id"] == str(AdditionalSignPlan.objects.first().pk)
        assert response_data["decision_date"] == data["decision_date"]
        assert response_data["owner"] == data["owner"]
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert AdditionalSignPlan.objects.count() == 0


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_plan__update(admin_user):
    client = get_api_client(user=get_user(admin=admin_user))
    dt = get_traffic_control_device_type(code="A1234")
    asp = get_additional_sign_plan()
    traffic_sign_plan = get_traffic_sign_plan(device_type=dt)
    data = {
        "parent": traffic_sign_plan.pk,
        "location": str(traffic_sign_plan.location),
        "decision_date": "2020-01-02",
        "owner": "City of Helsinki",
    }

    response = client.put(
        reverse("v1:additionalsignplan-detail", kwargs={"pk": asp.pk}), data=data
    )
    response_data = response.json()

    if admin_user:
        assert response.status_code == status.HTTP_200_OK
        assert response_data["id"] == str(asp.pk)
        assert response_data["decision_date"] == data["decision_date"]
        assert response_data["owner"] == data["owner"]
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        asp.refresh_from_db()
        assert (
            asp.decision_date
            != datetime.strptime(data["decision_date"], "%Y-%m-%d").date()
        )
        assert asp.owner != data["owner"]


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_plan__delete(admin_user):
    user = get_user(admin=admin_user)
    client = get_api_client(user=user)
    asp = get_additional_sign_plan()

    response = client.delete(
        reverse("v1:additionalsignplan-detail", kwargs={"pk": asp.pk})
    )

    if admin_user:
        assert response.status_code == status.HTTP_204_NO_CONTENT
        asp.refresh_from_db()
        assert not asp.is_active
        assert asp.deleted_by == user
        assert asp.deleted_at
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        asp.refresh_from_db()
        assert asp.is_active
        assert not asp.deleted_by
        assert not asp.deleted_at


@pytest.mark.django_db
def test__additional_sign_plan__soft_deleted_get_404_response():
    user = get_user()
    client = get_api_client()
    asp = get_additional_sign_plan()
    asp.soft_delete(user)

    response = client.get(
        reverse("v1:additionalsignplan-detail", kwargs={"pk": asp.pk})
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# AdditionalSignReal tests
# ===============================================


@pytest.mark.parametrize("geo_format", ("", "geojson"))
@pytest.mark.django_db
def test__additional_sign_real__list(geo_format):
    client = get_api_client()
    for owner in ["foo", "bar", "baz"]:
        asr = get_additional_sign_real(owner=owner)
        get_additional_sign_content_real(parent=asr)

    response = client.get(
        reverse("v1:additionalsignreal-list"), data={"geo_format": geo_format}
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["count"] == 3
    for result in response_data["results"]:
        obj = AdditionalSignReal.objects.get(pk=result["id"])
        assert result["content"][0]["id"] == str(obj.content.first().pk)

        if geo_format == "geojson":
            assert result["location"] == GeoJsonDict(obj.location.json)
            assert result["affect_area"] == GeoJsonDict(obj.affect_area.json)
        else:
            assert result["location"] == obj.location.ewkt
            assert result["affect_area"] == obj.affect_area.ewkt


@pytest.mark.parametrize("geo_format", ("", "geojson"))
@pytest.mark.django_db
def test__additional_sign_real__detail(geo_format):
    client = get_api_client()
    asr = get_additional_sign_real()
    ascr = get_additional_sign_content_real(parent=asr)

    response = client.get(
        reverse("v1:additionalsignreal-detail", kwargs={"pk": asr.pk}),
        data={"geo_format": geo_format},
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["id"] == str(asr.pk)
    assert response_data["parent"] == str(asr.parent.pk)
    assert response_data["content"][0]["id"] == str(ascr.pk)

    if geo_format == "geojson":
        assert response_data["location"] == GeoJsonDict(asr.location.json)
        assert response_data["affect_area"] == GeoJsonDict(asr.affect_area.json)
    else:
        assert response_data["location"] == asr.location.ewkt
        assert response_data["affect_area"] == asr.affect_area.ewkt


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_real__create(admin_user):
    client = get_api_client(user=get_user(admin=admin_user))
    traffic_sign_real = get_traffic_sign_real()
    data = {
        "parent": traffic_sign_real.pk,
        "location": str(traffic_sign_real.location),
        "owner": "City of Helsinki",
    }

    response = client.post(reverse("v1:additionalsignreal-list"), data=data)
    response_data = response.json()

    if admin_user:
        assert response.status_code == status.HTTP_201_CREATED
        assert AdditionalSignReal.objects.count() == 1
        assert response_data["id"] == str(AdditionalSignReal.objects.first().pk)
        assert response_data["owner"] == data["owner"]
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert AdditionalSignReal.objects.count() == 0


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_real__update(admin_user):
    client = get_api_client(user=get_user(admin=admin_user))
    dt = get_traffic_control_device_type(code="A1234")
    asr = get_additional_sign_real()
    traffic_sign_real = get_traffic_sign_real(device_type=dt)
    data = {
        "parent": traffic_sign_real.pk,
        "location": str(traffic_sign_real.location),
        "owner": "City of Helsinki",
    }

    response = client.put(
        reverse("v1:additionalsignreal-detail", kwargs={"pk": asr.pk}), data=data
    )
    response_data = response.json()

    if admin_user:
        assert response.status_code == status.HTTP_200_OK
        assert response_data["id"] == str(asr.pk)
        assert response_data["owner"] == data["owner"]
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        asr.refresh_from_db()
        assert asr.owner != data["owner"]


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_real__delete(admin_user):
    user = get_user(admin=admin_user)
    client = get_api_client(user=user)
    asr = get_additional_sign_real()

    response = client.delete(
        reverse("v1:additionalsignreal-detail", kwargs={"pk": asr.pk})
    )

    if admin_user:
        assert response.status_code == status.HTTP_204_NO_CONTENT
        asr.refresh_from_db()
        assert not asr.is_active
        assert asr.deleted_by == user
        assert asr.deleted_at
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        asr.refresh_from_db()
        assert asr.is_active
        assert not asr.deleted_by
        assert not asr.deleted_at


@pytest.mark.django_db
def test__additional_sign_real__soft_deleted_get_404_response():
    user = get_user()
    client = get_api_client()
    asr = get_additional_sign_real()
    asr.soft_delete(user)

    response = client.get(
        reverse("v1:additionalsignreal-detail", kwargs={"pk": asr.pk})
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# AdditionalSignContentPlan tests
# ===============================================


@pytest.mark.django_db
def test__additional_sign_content_plan__list():
    client = get_api_client()
    dt = get_traffic_control_device_type(code="H17.1")
    for i in range(3):
        get_additional_sign_content_plan(order=i, device_type=dt)

    response = client.get(reverse("v1:additionalsigncontentplan-list"))
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["count"] == 3
    for i in range(3):
        result = response_data["results"][i]
        assert result["order"] == i
        assert result["device_type"] == str(dt.pk)


@pytest.mark.django_db
def test__additional_sign_content_plan__detail():
    client = get_api_client()
    dt = get_traffic_control_device_type(code="H17.1")
    ascp = get_additional_sign_content_plan(device_type=dt)

    response = client.get(
        reverse("v1:additionalsigncontentplan-detail", kwargs={"pk": ascp.pk})
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["id"] == str(ascp.pk)
    assert response_data["parent"] == str(ascp.parent.pk)
    assert response_data["order"] == 1
    assert response_data["text"] == "Content"
    assert response_data["device_type"] == str(dt.pk)
    assert response_data["created_by"] == str(ascp.created_by.pk)
    assert response_data["updated_by"] == str(ascp.updated_by.pk)


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_content_plan__create(admin_user):
    client = get_api_client(user=get_user(admin=admin_user))
    asp = get_additional_sign_plan()
    dt = get_traffic_control_device_type(code="H17.1")
    data = {
        "parent": str(asp.pk),
        "order": 1,
        "text": "Content",
        "device_type": str(dt.pk),
    }

    response = client.post(reverse("v1:additionalsigncontentplan-list"), data=data)
    response_data = response.json()

    if admin_user:
        assert response.status_code == status.HTTP_201_CREATED
        assert AdditionalSignContentPlan.objects.count() == 1
        assert response_data["id"] == str(AdditionalSignContentPlan.objects.first().pk)
        assert response_data["parent"] == data["parent"]
        assert response_data["order"] == data["order"]
        assert response_data["text"] == data["text"]
        assert response_data["device_type"] == data["device_type"]
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert AdditionalSignContentPlan.objects.count() == 0


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_content_plan__update(admin_user):
    client = get_api_client(user=get_user(admin=admin_user))
    ascp = get_additional_sign_content_plan()
    dt = get_traffic_control_device_type(code="H17.1")
    data = {
        "parent": get_additional_sign_plan(owner="New owner").pk,
        "text": "Updated content",
        "order": 100,
        "device_type": str(dt.pk),
    }

    response = client.put(
        reverse("v1:additionalsigncontentplan-detail", kwargs={"pk": ascp.pk}),
        data=data,
    )
    response_data = response.json()

    if admin_user:
        assert response.status_code == status.HTTP_200_OK
        assert response_data["id"] == str(ascp.pk)
        assert response_data["parent"] == str(data["parent"])
        assert response_data["text"] == data["text"]
        assert response_data["order"] == data["order"]
        assert response_data["device_type"] == str(data["device_type"])
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        ascp.refresh_from_db()
        assert ascp.parent.pk != data["parent"]
        assert ascp.text != data["text"]
        assert ascp.order != data["order"]
        assert ascp.device_type.pk != data["device_type"]


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_content_plan__delete(admin_user):
    user = get_user(admin=admin_user)
    client = get_api_client(user=user)
    ascp = get_additional_sign_content_plan()

    response = client.delete(
        reverse("v1:additionalsigncontentplan-detail", kwargs={"pk": ascp.pk})
    )

    if admin_user:
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not AdditionalSignContentPlan.objects.filter(pk=ascp.pk).exists()
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert AdditionalSignContentPlan.objects.filter(pk=ascp.pk).exists()


# AdditionalSignContentReal tests
# ===============================================


@pytest.mark.django_db
def test__additional_sign_content_real__list():
    client = get_api_client()
    dt = get_traffic_control_device_type(code="H17.1")
    for i in range(3):
        get_additional_sign_content_real(order=i, device_type=dt)

    response = client.get(reverse("v1:additionalsigncontentreal-list"))
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["count"] == 3
    for i in range(3):
        result = response_data["results"][i]
        assert result["order"] == i
        assert result["device_type"] == str(dt.pk)


@pytest.mark.django_db
def test__additional_sign_content_real__detail():
    client = get_api_client()
    dt = get_traffic_control_device_type(code="H17.1")
    ascr = get_additional_sign_content_real(device_type=dt)

    response = client.get(
        reverse("v1:additionalsigncontentreal-detail", kwargs={"pk": ascr.pk})
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["id"] == str(ascr.pk)
    assert response_data["parent"] == str(ascr.parent.pk)
    assert response_data["order"] == 1
    assert response_data["text"] == "Content"
    assert response_data["device_type"] == str(dt.pk)
    assert response_data["created_by"] == str(ascr.created_by.pk)
    assert response_data["updated_by"] == str(ascr.updated_by.pk)


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_content_real__create(admin_user):
    client = get_api_client(user=get_user(admin=admin_user))
    asr = get_additional_sign_real()
    dt = get_traffic_control_device_type(code="H17.1")
    data = {
        "parent": str(asr.pk),
        "order": 1,
        "text": "Content",
        "device_type": str(dt.pk),
    }

    response = client.post(reverse("v1:additionalsigncontentreal-list"), data=data)
    response_data = response.json()

    if admin_user:
        assert response.status_code == status.HTTP_201_CREATED
        assert AdditionalSignContentReal.objects.count() == 1
        assert response_data["id"] == str(AdditionalSignContentReal.objects.first().pk)
        assert response_data["parent"] == data["parent"]
        assert response_data["order"] == data["order"]
        assert response_data["text"] == data["text"]
        assert response_data["device_type"] == data["device_type"]
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert AdditionalSignContentReal.objects.count() == 0


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_content_real__update(admin_user):
    client = get_api_client(user=get_user(admin=admin_user))
    ascr = get_additional_sign_content_real()
    dt = get_traffic_control_device_type(code="H17.1")
    data = {
        "parent": get_additional_sign_real(owner="New owner").pk,
        "text": "Updated content",
        "order": 100,
        "device_type": str(dt.pk),
    }

    response = client.put(
        reverse("v1:additionalsigncontentreal-detail", kwargs={"pk": ascr.pk}),
        data=data,
    )
    response_data = response.json()

    if admin_user:
        assert response.status_code == status.HTTP_200_OK
        assert response_data["id"] == str(ascr.pk)
        assert response_data["parent"] == str(data["parent"])
        assert response_data["text"] == data["text"]
        assert response_data["order"] == data["order"]
        assert response_data["device_type"] == str(data["device_type"])
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        ascr.refresh_from_db()
        assert ascr.parent.pk != data["parent"]
        assert ascr.text != data["text"]
        assert ascr.order != data["order"]
        assert ascr.device_type.pk != data["device_type"]


@pytest.mark.parametrize("admin_user", (False, True))
@pytest.mark.django_db
def test__additional_sign_content_real__delete(admin_user):
    user = get_user(admin=admin_user)
    client = get_api_client(user=user)
    ascr = get_additional_sign_content_real()

    response = client.delete(
        reverse("v1:additionalsigncontentreal-detail", kwargs={"pk": ascr.pk})
    )

    if admin_user:
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not AdditionalSignContentReal.objects.filter(pk=ascr.pk).exists()
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert AdditionalSignContentReal.objects.filter(pk=ascr.pk).exists()
