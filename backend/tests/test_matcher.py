import pytest
from backend.app.matcher import matcher, clean_query

def test_clean_query():
    assert clean_query("Tab. Dolo 650 1-0-1") == "dolo 650"
    assert clean_query("Cap Omez 20mg bbf") == "omez 20mg"
    assert clean_query("Syr. Ascoril 100ml tds") == "ascoril 100ml"

def test_exact_brand_search():
    res = matcher.search("Dolo 650")
    assert res.total_matches > 0
    top = res.matches[0]
    assert top.medicine.brand_name == "Dolo 650"
    assert "Paracetamol" in top.medicine.molecule
    assert top.medicine.generic_match is not None
    assert top.medicine.generic_match.ja_price_inr == 10.50

def test_molecule_search():
    res = matcher.search("Metformin")
    assert res.total_matches > 0
    top = res.matches[0]
    assert "Metformin" in top.medicine.molecule

def test_typo_tolerance():
    # 'paracetmol' with missing 'a'
    res = matcher.search("paracetmol 650")
    assert res.total_matches > 0
    assert any("Paracetamol" in m.medicine.molecule for m in res.matches[:3])

def test_prescription_noise_search():
    res = matcher.search("Tab Augmentin 625 Duo 1-0-1")
    assert res.total_matches > 0
    top = res.matches[0]
    assert "Augmentin 625 Duo" in top.medicine.brand_name
    assert "Amoxicillin" in top.medicine.molecule

def test_empty_query():
    res = matcher.search("")
    assert res.total_matches == 0
    assert len(res.matches) == 0
