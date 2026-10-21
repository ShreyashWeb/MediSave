import pytest
from backend.app.compare import compare_medicines
from backend.app.models import CompareRequest, CompareItemRequest

def test_compare_single_item():
    req = CompareRequest(items=[CompareItemRequest(medicine_id="B001", quantity_units=15)])
    res = compare_medicines(req)
    assert len(res.items) == 1
    item = res.items[0]
    assert item.brand_name == "Dolo 650"
    assert item.brand_total_cost > item.generic_total_cost
    assert item.total_saving_inr > 0
    assert res.total_saving_inr == item.total_saving_inr
    assert res.overall_saving_percentage > 0

def test_compare_multi_item_basket():
    req = CompareRequest(items=[
        CompareItemRequest(medicine_id="B001", quantity_units=10),  # Dolo 650
        CompareItemRequest(medicine_id="B006", quantity_units=10),  # Augmentin 625 Duo
        CompareItemRequest(medicine_id="B009", quantity_units=15)   # Pan 40
    ])
    res = compare_medicines(req)
    assert len(res.items) == 3
    assert res.total_brand_cost > res.total_generic_cost
    assert res.total_saving_inr > 100.0  # Significant savings in INR
    assert res.overall_saving_percentage > 50
    assert "not medical advice" in res.disclaimer.lower()
