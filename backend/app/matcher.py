import re
from typing import List, Tuple, Optional
from rapidfuzz import fuzz
from .models import Medicine, SearchResultItem, SearchResponse
from .data_loader import data_loader

NOISE_PATTERNS = [
    r"\b(tab|capsule|cap|tablet|syrup|syr|syp|inj|injection|inhaler|gel|ointment|oint)\.?\b",
    r"\b(1-0-1|1-1-1|0-1-0|0-0-1|1-0-0|0-1-1|1-1-0|od|bd|bid|tds|tid|qid|hs|sos|bbf|ac|pc)\.?\b",
    r"\b(strip|strip of|tabs|caps|bottles?|pack|units?|rx)\.?\b",
    r"[#*@!&^%$~,.]"
]

def clean_query(query: str) -> str:
    """Clean clinical shorthand noise from query."""
    if not query:
        return ""
    q = query.lower()
    for pattern in NOISE_PATTERNS:
        q = re.sub(pattern, " ", q, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", q).strip()

class Matcher:
    def __init__(self):
        self.data_loader = data_loader

    def search(self, query: str, limit: int = 5, threshold: float = 40.0) -> SearchResponse:
        cleaned = clean_query(query)
        if not cleaned:
            return SearchResponse(query=query, total_matches=0, matches=[], did_you_mean=None)

        results = []
        best_candidate = None
        highest_score = 0.0

        for med in self.data_loader.medicines:
            brand = med.brand.lower()
            molecule = med.molecule.lower()

            # WRatio + token_set_ratio over brand and molecule
            brand_wratio = fuzz.WRatio(cleaned, brand)
            brand_tsr = fuzz.token_set_ratio(cleaned, brand)
            brand_score = max(brand_wratio, brand_tsr)

            mol_wratio = fuzz.WRatio(cleaned, molecule)
            mol_tsr = fuzz.token_set_ratio(cleaned, molecule)
            mol_score = max(mol_wratio, mol_tsr)

            # Combined searchable representation
            searchable = f"{brand} {molecule} {med.strength} {med.form}".lower()
            combo_score = fuzz.token_set_ratio(cleaned, searchable)

            # Substring exact boost
            if cleaned in brand or brand in cleaned:
                brand_score = max(brand_score, 92.0)
            if cleaned in molecule or molecule in cleaned:
                mol_score = max(mol_score, 88.0)

            # Strength matching bonus if query mentions a number
            strength_nums = re.findall(r"\d+", med.strength)
            query_nums = re.findall(r"\d+", cleaned)
            strength_bonus = 0.0
            if strength_nums and query_nums and any(qn in strength_nums for qn in query_nums):
                strength_bonus = 8.0

            score = min(100.0, max(brand_score * 1.05, mol_score, combo_score * 0.95) + strength_bonus)
            score = round(score, 1)

            match_type = "brand" if brand_score >= mol_score else "molecule"

            if score > highest_score:
                highest_score = score
                best_candidate = med.brand

            if score >= threshold:
                results.append((score, med, match_type))

        # Sort descending
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:limit]

        formatted = [
            SearchResultItem(
                medicine=item[1],
                score=item[0],
                match_type=item[2]
            )
            for item in top_results
        ]

        # "Did you mean...?" if highest score is under confident threshold (e.g. between 45 and 82)
        did_you_mean = None
        if top_results and top_results[0][0] < 82.0 and best_candidate:
            if best_candidate.lower() != cleaned:
                did_you_mean = best_candidate

        return SearchResponse(
            query=query,
            total_matches=len(formatted),
            matches=formatted,
            did_you_mean=did_you_mean
        )

matcher = Matcher()
