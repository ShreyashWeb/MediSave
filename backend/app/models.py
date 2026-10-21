from typing import List, Optional
from pydantic import BaseModel, Field

class Medicine(BaseModel):
    id: str
    brand: str
    brand_name: Optional[str] = None
    molecule: str
    strength: str
    form: str
    pack_size: str
    brand_mrp_inr: float
    ja_price_inr: float
    saving_percentage: int
    source: str = "SAMPLE_REPLACE_ME"

    def model_post_init(self, __context):
        if not self.brand_name:
            self.brand_name = self.brand

class SearchResultItem(BaseModel):
    medicine: Medicine
    score: float
    match_type: str  # "brand", "molecule", "fuzzy"

class SearchResponse(BaseModel):
    query: str
    total_matches: int
    matches: List[SearchResultItem]
    did_you_mean: Optional[str] = None
    disclaimer: str = (
        "Price and molecule information only, not medical advice. "
        "Confirm any change with your doctor or pharmacist."
    )

class ExtractedItem(BaseModel):
    raw_text: str
    brand: Optional[str] = None
    molecule: Optional[str] = None
    strength: Optional[str] = None

class ExtractionResponse(BaseModel):
    success: bool
    model_used: str
    items: List[ExtractedItem]
    warning: Optional[str] = None
    disclaimer: str = (
        "Price and molecule information only, not medical advice. "
        "Confirm any change with your doctor or pharmacist."
    )

class CompareItemRequest(BaseModel):
    medicine_id: str
    quantity: int = 1

class CompareRequest(BaseModel):
    items: List[CompareItemRequest]

class CompareResponse(BaseModel):
    total_brand_mrp: float
    total_ja_price: float
    total_saving: float
    overall_saving_percentage: int

class Kendra(BaseModel):
    id: str
    name: str
    address: str
    city: str
    state: str
    pincode: str
    lat: float
    lng: float
    phone: str
    timings: str
    distance_km: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    app_name: str
    total_medicines: int
    gemma_model: str
    gemma_base_url: str
    gemma_provider: str
