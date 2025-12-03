# -*- coding: utf-8 -*-
"""
Test script to examine and test the Excel file import
"""
import sys
import os
from pathlib import Path

# Set stdout encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Import dependencies
try:
    import pandas as pd
    print("[OK] pandas available")
except ImportError:
    print("[!] pandas not available - attempting to install")
    os.system("pip install pandas openpyxl -q")
    import pandas as pd

def main():
    file_path = Path("tests/RHV TEST.xlsx")
    
    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        return
    
    print("\n" + "="*80)
    print("EXAMINING EXCEL FILE: RHV TEST.xlsx")
    print("="*80 + "\n")
    
    try:
        # Read raw data first to see structure
        print("[1] Reading raw file structure...")
        df_raw = pd.read_excel(file_path, header=None, nrows=3)
        print(f"\nRaw first 3 rows (no header processing):")
        print(df_raw.to_string())
        
        # Now read with proper header
        print("\n[2] Reading with first row as header...")
        df = pd.read_excel(file_path, header=0)
        
        print(f"\nColumns found: {len(df.columns)}")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        print(f"\nData shape: {df.shape[0]} rows x {df.shape[1]} columns")
        
        # Show first row of data
        print(f"\nFirst data row values:")
        if len(df) > 0:
            for col in df.columns:
                val = df[col].iloc[0]
                print(f"  {col}: {val}")
        
        # Test column matching
        print("\n" + "="*80)
        print("COLUMN MAPPING TEST")
        print("="*80 + "\n")
        
        mappings = {
            'asset_id': ['asset id', 'asset_id', 'assetid', 'id'],
            'name': ['description', 'asset description', 'name'],
            'category': ['category', 'asset category'],
            'sub_category': ['sub category', 'subcategory'],
            'acquisition_date': ['acquisition', 'acquistion', 'date'],
            'supplier': ['supplier', 'vendor'],
            'quantity': ['quantity', 'qty'],
            'unit_cost': ['unit cost'],
            'total_cost': ['total cost'],
            'useful_life': ['useful life', 'usefull life'],
            'depreciation_method': ['depreciation method'],
            'depreciation_percentage': ['depreciation %', 'depreciation percentage'],
            'net_book_value': ['netbook value', 'net book value'],
            'department': ['department', 'location'],
            'custodian': ['custodian', 'user'],
            'serial_number': ['serial', 'serial number'],
            'model_number': ['model', 'model number'],
            'status': ['status'],
        }
        
        def find_col(variants, cols):
            variants_lower = [v.lower() for v in variants]
            for c in cols:
                if c and c.lower() in variants_lower:
                    return c
                if c and any(v in c.lower() for v in variants_lower):
                    return c
            return None
        
        matched = {}
        for field, variants in mappings.items():
            col = find_col(variants, df.columns)
            if col:
                matched[field] = col
                print(f"  [MATCH] {field:25s} -> {col}")
            else:
                print(f"  [MISS]  {field:25s}")
        
        print(f"\nMatched: {len(matched)}/{len(mappings)}")
        
        # Show unmatched Excel columns
        matched_cols = set(matched.values())
        unmatched = set(df.columns) - matched_cols
        if unmatched:
            print(f"\nUnmatched Excel columns:")
            for col in unmatched:
                print(f"  - {col}")
        
        print("\n" + "="*80)
        print("READY FOR IMPORT")
        print("="*80 + "\n")
        print("Use Settings > Import tab to import this file")
        print(f"File: {file_path}")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
