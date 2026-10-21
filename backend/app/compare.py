from typing import List
from .models import CompareRequest, CompareResponse
from .data_loader import data_loader

def compare_medicines(req: CompareRequest) -> CompareResponse:
    total_brand = 0.0
    total_ja = 0.0

    for item in req.items:
        med = data_loader.get_medicine(item.medicine_id)
        if not med:
            continue
        qty = max(1, item.quantity)
        total_brand += med.brand_mrp_inr * qty
        total_ja += med.ja_price_inr * qty

    total_saving = max(0.0, round(total_brand - total_ja, 2))
    overall_pct = round((total_saving / total_brand) * 100) if total_brand > 0 else 0

    return CompareResponse(
        total_brand_mrp=round(total_brand, 2),
        total_ja_price=round(total_ja, 2),
        total_saving=total_saving,
        overall_saving_percentage=overall_pct
    )
