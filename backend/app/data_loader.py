import csv
import os
from typing import List, Dict, Optional
from .models import Medicine

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV_PATH = os.path.join(BASE_DIR, "data", "medicines.csv")

class DataLoader:
    def __init__(self):
        self.medicines: List[Medicine] = []
        self.medicines_by_id: Dict[str, Medicine] = {}
        self.load_all()

    def load_all(self):
        if not os.path.exists(CSV_PATH):
            return

        with open(CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                brand_mrp = float(row.get("brand_mrp_inr", 0))
                ja_price = float(row.get("ja_price_inr", 0))
                saving_pct = 0
                if brand_mrp > ja_price and brand_mrp > 0:
                    saving_pct = round(((brand_mrp - ja_price) / brand_mrp) * 100)

                med = Medicine(
                    id=row.get("id", "").strip(),
                    brand=row.get("brand", "").strip(),
                    brand_name=row.get("brand", "").strip(),
                    molecule=row.get("molecule", "").strip(),
                    strength=row.get("strength", "").strip(),
                    form=row.get("form", "").strip(),
                    pack_size=row.get("pack_size", "").strip(),
                    brand_mrp_inr=brand_mrp,
                    ja_price_inr=ja_price,
                    saving_percentage=saving_pct,
                    source=row.get("source", "SAMPLE_REPLACE_ME").strip()
                )
                self.medicines.append(med)
                self.medicines_by_id[med.id] = med

    def get_medicine(self, med_id: str) -> Optional[Medicine]:
        return self.medicines_by_id.get(med_id)

data_loader = DataLoader()
