import pytest

from src.database.schemas.order import ProductOrderType


@pytest.fixture()
def test_productOrderType():
    yield ProductOrderType(
        Category="Test Category",
        Variety="Test Variety",
        Packaging="Test Packaging",
        Volume="Test Volume",
        Price_per_unit="Test Price_per_unit",
    )


def test_ProductOrderType_converts_to_dictionary(test_productOrderType):
    assert test_productOrderType.dict() == {
        "Category": "Test Category",
        "Variety": "Test Variety",
        "Packaging": "Test Packaging",
        "Volume": "Test Volume",
        "Price_per_unit": "Test Price_per_unit",
    }
