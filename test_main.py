from typing import List

import pytest

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


@pytest.mark.parametrize(
    "country, expected_cities",
    [
        ("England", ["London"]),
        ("Portugal", ["Lisbon", "Porto"]),
        ("Spain", ["Seville"]),
    ],
)
def test_cities(country: str, expected_cities: List[str]) -> None:
    """Return only the requested country's available cities."""
    response = client.get(f"/countries/{country}")
    assert response.status_code == 200
    assert sorted(response.json()) == expected_cities


def test_cities_unknown_country() -> None:
    """Return 404 when the requested country has no data."""
    response = client.get("/countries/Unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}


def test_monthly_average() -> None:
    """Keep the existing monthly weather route accessible."""
    response = client.get("/countries/England/London/January")
    assert response.status_code == 200
    assert response.json() == {"high": 45, "low": 36}