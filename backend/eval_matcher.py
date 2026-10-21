#!/usr/bin/env python3
"""
MediSave Matcher Accuracy Evaluation
Tests 30 deliberately messy, misspelled, and OCR-distorted prescription inputs
against the dataset to report Top-1 and Top-3 accuracy for the README.
"""

import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.matcher import matcher

BENCHMARK_CASES = [
    # (Input Query, Expected Target Keyword in brand or molecule)
    ("Tab. Dolo-650 1-0-1", "Dolo 650"),
    ("dolo 650mg", "Dolo 650"),
    ("paracetmol 650", "Paracetamol"),
    ("calpol 500 tab", "Calpol 500"),
    ("Crocin 650 mg", "Crocin 650"),
    ("Augmentin Duo 625 1bd", "Augmentin 625 Duo"),
    ("amox clav 625", "Amoxicillin"),
    ("Clavam 625mg tab", "Clavam 625"),
    ("Pan 40 bbf", "Pan 40"),
    ("pantocid 40 mg", "Pantocid 40"),
    ("pan-d cap od", "Pan-D"),
    ("Atorva 10 tab hs", "Atorva 10"),
    ("atorvastatin 20mg", "Atorvastatin"),
    ("lipitor 10", "Lipitor 10"),
    ("glycomet 500 sr", "Glycomet 500"),
    ("metformin 500", "Metformin"),
    ("glycomet gp1", "Glycomet-GP 1"),
    ("Telma 40 mg od", "Telma 40"),
    ("telmisartan 40", "Telmisartan"),
    ("amlokind 5", "Amlokind 5"),
    ("norvasc 5mg", "Norvasc 5"),
    ("azee 500 od x 3d", "Azee 500"),
    ("azithral 500", "Azithral 500"),
    ("montair lc at night", "Montair-LC"),
    ("cetzine 10mg", "Cetzine 10"),
    ("omez 20 bbf", "Omez 20"),
    ("losar 50", "Losar 50"),
    ("combiflam sos", "Combiflam"),
    ("shelcal 500 daily", "Shelcal 500"),
    ("asthalin inhaler 2 puffs", "Asthalin Inhaler"),
]

def run_evaluation():
    print("=" * 80)
    print(" MediSave Matcher Benchmark: 30 Real-World Messy Prescription Inputs")
    print("=" * 80)
    print(f"{'#':<3} | {'Input Query':<28} | {'Expected':<18} | {'Top-1 Result':<20} | {'Score':<5} | {'Status'}")
    print("-" * 80)

    top1_correct = 0
    top3_correct = 0
    total = len(BENCHMARK_CASES)

    for i, (query, expected) in enumerate(BENCHMARK_CASES, 1):
        res = matcher.search(query, limit=3)
        top1_match = res.matches[0] if res.matches else None

        # Check Top 1
        is_top1 = False
        if top1_match:
            med_text = f"{top1_match.medicine.brand_name} {top1_match.medicine.molecule}".lower()
            if expected.lower() in med_text:
                is_top1 = True
                top1_correct += 1

        # Check Top 3
        is_top3 = False
        for m in res.matches[:3]:
            med_text = f"{m.medicine.brand_name} {m.medicine.molecule}".lower()
            if expected.lower() in med_text:
                is_top3 = True
                break
        if is_top3:
            top3_correct += 1

        top1_name = top1_match.medicine.brand_name if top1_match else "None"
        score = top1_match.score if top1_match else 0.0
        status = "TOP-1 PASS" if is_top1 else ("TOP-3 PASS" if is_top3 else "FAIL")

        print(f"{i:<3} | {query:<28} | {expected:<18} | {top1_name:<20} | {score:<5.1f} | {status}")

    top1_pct = (top1_correct / total) * 100
    top3_pct = (top3_correct / total) * 100

    print("=" * 80)
    print(f"BENCHMARK SUMMARY:")
    print(f"Total Test Cases : {total}")
    print(f"Top-1 Accuracy   : {top1_correct}/{total} ({top1_pct:.1f}%)")
    print(f"Top-3 Accuracy   : {top3_correct}/{total} ({top3_pct:.1f}%)")
    print("=" * 80)

if __name__ == "__main__":
    run_evaluation()
