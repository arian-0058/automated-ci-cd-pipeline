import pytest
import sys
import os

# اضافه کردن پوشه src به ماژول‌های پایتون
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from app import app  # noqa: E402


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """بررسی اینکه اندپوینت سلامت کد ۲۰۰ و فرمت استاندارد برمی‌گرداند"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "UP", "service": "python-backend"}


def test_homepage_render(client):
    """بررسی اینکه قالب صفحه با موفقیت بارگذاری شده و تایتل ماه هفتم در آن وجود دارد"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Month 07: CI/CD Pipeline" in response.data