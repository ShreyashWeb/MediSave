import pytest
from backend.app.gemma_client import GemmaClient

def test_parse_valid_json():
    client = GemmaClient()
    sample_json = """
    {
      "items": [
        {
          "raw_text": "Dolo-650 Paracetamol Tablets IP 650 mg",
          "brand": "Dolo 650",
          "molecule": "Paracetamol",
          "strength": "650 mg",
          "form": "Tablet",
          "confidence": 0.95
        }
      ]
    }
    """
    items = client._parse_json_content(sample_json)
    assert len(items) == 1
    assert items[0].brand == "Dolo 650"
    assert items[0].confidence == 0.95

def test_parse_markdown_wrapped_json():
    client = GemmaClient()
    sample_wrapped = """```json
    {
      "items": [
        {
          "raw_text": "Augmentin 625 Duo",
          "brand": "Augmentin 625 Duo",
          "molecule": "Amoxicillin and Clavulanic Acid",
          "strength": "625 mg",
          "form": "Tablet",
          "confidence": 0.88
        }
      ]
    }
    ```"""
    items = client._parse_json_content(sample_wrapped)
    assert len(items) == 1
    assert items[0].brand == "Augmentin 625 Duo"

def test_parse_invalid_json():
    client = GemmaClient()
    items = client._parse_json_content("Not valid json at all")
    assert items == []

@pytest.mark.asyncio
async def test_dataset_enrichment_rule():
    client = GemmaClient()
    # Ensure that extracted item binds to real dataset without inventing facts
    items = client._parse_json_content("""
    {
      "items": [
        {
          "raw_text": "Dolo 650",
          "brand": "Dolo 650",
          "molecule": "Paracetamol",
          "strength": "650 mg",
          "form": "Tablet",
          "confidence": 0.9
        }
      ]
    }
    """)
    enriched = client._enrich_items_from_dataset(items)
    assert len(enriched) == 1
    assert enriched[0].matched_medicine is not None
    assert enriched[0].matched_medicine.brand_name == "Dolo 650"
    assert enriched[0].matched_medicine.generic_match.ja_price_inr == 10.50
