import math
import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import config
from .models import (
    SearchResponse, ExtractionResponse, CompareRequest, CompareResponse,
    HealthResponse, Kendra
)
from .matcher import matcher
from .compare import compare_medicines
from .gemma_client import gemma_client
from .data_loader import data_loader

app = FastAPI(
    title="MediSave API",
    description="The Prescription You Cannot Read — Generic Medicine Discovery & Cost Visibility Platform",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in config.ALLOWED_ORIGINS else config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points in km."""
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

@app.get("/api/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        app_name="MediSave",
        total_medicines=len(data_loader.medicines),
        gemma_model=config.GEMMA_MODEL,
        gemma_base_url=config.GEMMA_BASE_URL,
        gemma_provider=config.GEMMA_PROVIDER
    )

@app.get("/api/search", response_model=SearchResponse)
def search_medicines(
    q: str = Query(..., min_length=1, description="Brand name, molecule, or prescription text"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Fuzzy search over medicine brand names, molecules, and therapeutic classes.
    100% offline-compatible; does not require an LLM.
    """
    return matcher.search(query=q, limit=limit)

@app.post("/api/extract-from-image", response_model=ExtractionResponse)
async def extract_from_image(file: UploadFile = File(...)):
    """
    Upload a photo of a medicine strip, box, or printed prescription.
    Processed purely in-memory via Gemma 4. Never stored to disk.
    """
    if file.content_type not in ["image/jpeg", "image/png", "image/webp", "image/bmp"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Please upload JPEG, PNG, or WebP."
        )

    # Check file size limit
    max_bytes = config.MAX_IMAGE_SIZE_MB * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Image too large. Maximum allowed size is {config.MAX_IMAGE_SIZE_MB}MB."
        )

    return await gemma_client.extract_from_image(content, file.filename or "upload.jpg")

@app.post("/api/compare", response_model=CompareResponse)
def compare(request: CompareRequest):
    """
    Calculate fair unit-price comparison and total savings across single or multiple medicines.
    """
    return compare_medicines(request)

@app.get("/api/kendras")
def get_kendras(
    lat: Optional[float] = Query(None, description="User latitude"),
    lng: Optional[float] = Query(None, description="User longitude"),
    radius_km: float = Query(50.0, description="Search radius in kilometers"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Locate nearby Pradhan Mantri Bhartiya Janaushadhi Kendras.
    Calculates Haversine distance when GPS coordinates are supplied.
    """
    kendras = data_loader.kendras
    if lat is not None and lng is not None:
        results = []
        for k in kendras:
            d = haversine_distance(lat, lng, k.lat, k.lng)
            k_dict = k.model_dump()
            k_dict["distance_km"] = d
            results.append(k_dict)
        results.sort(key=lambda x: x["distance_km"])
        return results[:limit]
    return [k.model_dump() for k in kendras[:limit]]

# Mount frontend directory for direct unified serving
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
