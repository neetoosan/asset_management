"""
Test script to examine and test the Excel file import
"""
import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Now import dependencies
try:
    import pandas as pd
    print("✓ pandas available")
except ImportError:
    print("✗ pandas not available - attempting to install")
    os.system("pip install pandas openpyxl -q")
    import pandas as pd

def examine_excel_file(file_path):
    """Examine the structure of the Excel file"""
    print(f"\n{'='*80}")
    print(f"EXAMINING: {file_path}")
    print(f"{'='*80}\n")
    
    try:
        # Read Excel file - treat first row as data initially to inspect
        df_raw = pd.read_excel(file_path, header=None)
        
        # Check if first row looks like headers (all non-numeric strings)
        first_row = df_raw.iloc[0]
        is_header = all(isinstance(v, str) for v in first_row if pd.notna(v))
        
        # Re-read with appropriate header setting
        if is_header:
            df = pd.read_excel(file_path, header=0)
        else:
            df = pd.read_excel(file_path, header=None)
            # If no header, create generic column names
            df.columns = [f'Column_{i}' for i in range(len(df.columns))]
        
        print(f"📊 Sheet Columns ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        print(f"\n📈 Data Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        print(f"\n📋 Data Types:")
        for col in df.columns:
            print(f"  - {col}: {df[col].dtype}")
        
        print(f"\n🔍 First 3 Rows:")
        print(df.head(3).to_string())
        
        print(f"\n📍 Sample Values:")
        for col in df.columns:
            first_val = df[col].iloc[0] if len(df) > 0 else None
            print(f"  - {col}: {first_val}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_column_mapping(df):
    """Test how the import mappings would match the Excel columns"""
    print(f"\n{'='*80}")
    print("COLUMN MAPPING TEST")
    print(f"{'='*80}\n")
    
    # Define mappings from setting_screen.py
    mappings = {
        'asset_id': ['asset id', 'asset_id', 'assetid', 'id', 'asset no', 'asset number'],
        'name': ['description', 'asset description', 'name', 'asset name', 'item'],
        'serial_number': ['serial', 'serial number', 'serial_number', 'serial no', 's/n'],
        'model_number': ['model', 'model number', 'model_number', 'model no'],
        'department': ['department', 'dept', 'location', 'department/location', 'dept/location'],
        'category': ['category', 'asset category', 'type', 'class'],
        'sub_category': ['sub category', 'sub_category', 'subcategory', 'sub-category'],
        'total_cost': ['total cost', 'total_cost', 'value', 'cost', 'price', 'amount'],
        'acquisition_date': ['acquisition', 'acquisition date', 'date registered', 'acquisition_date', 'purchase date', 'date'],
        'supplier': ['supplier', 'vendor', 'supplier/vendor'],
        'status': ['status', 'asset status', 'condition'],
        'quantity': ['quantity', 'qty', 'units'],
        'unit_cost': ['unit cost', 'unit_cost', 'unit price', 'price per unit'],
        'custodian': ['custodian', 'user', 'assigned to', 'custodian/user'],
        'useful_life': ['useful life', 'useful_life', 'years', 'lifespan', 'useful life (years)'],
        'depreciation_method': ['depreciation method', 'depreciation_method', 'method', 'depreciation'],
        'depreciation_percentage': ['depreciation %', 'depreciation_percentage', 'dep %', 'depreciation percentage'],
        'depreciation_value': ['depreciation', 'depreciation value', 'depreciation_value'],
        'scrap_value': ['scrap value', 'scrap_value', 'salvage value'],
        'net_book_value': ['net book value', 'nbv', 'book value']
    }
    
    def find_column(variants, columns):
        """Find column by matching variants (case-insensitive)"""
        variants = [v.lower() for v in variants]
        for c in columns:
            if c:
                col_lower = c.lower().strip()
                # Exact match
                if col_lower in variants:
                    return c
                # Partial match
                if any(v in col_lower for v in variants):
                    return c
        return None
    
    excel_columns = df.columns.tolist()
    matched = {}
    unmatched_excel = set(excel_columns)
    
    print("🔗 Column Matches:\n")
    for field, variants in mappings.items():
        matched_col = find_column(variants, excel_columns)
        if matched_col:
            matched[field] = matched_col
            unmatched_excel.discard(matched_col)
            print(f"  ✓ {field:25s} → {matched_col}")
        else:
            print(f"  ✗ {field:25s} → NOT FOUND (looking for: {', '.join(variants[:2])}...)")
    
    print(f"\n📋 Unmatched Excel Columns:")
    if unmatched_excel:
        for col in unmatched_excel:
            print(f"  ⚠ {col}")
    else:
        print(f"  ✓ All Excel columns matched to asset fields!")
    
    print(f"\n📊 Mapping Summary:")
    print(f"  - Mapped: {len(matched)}/{len(excel_columns)} fields")
    print(f"  - Unmatched: {len(unmatched_excel)}")
    
    return matched

def test_data_conversion(df, mappings):
    """Test data type conversions"""
    print(f"\n{'='*80}")
    print("DATA CONVERSION TEST")
    print(f"{'='*80}\n")
    
    # Test a sample row
    if len(df) > 0:
        sample_row = df.iloc[0]
        print("🔄 Testing first row conversions:\n")
        
        for field, excel_col in mappings.items():
            if excel_col and excel_col in df.columns:
                val = sample_row[excel_col]
                
                try:
                    # Test conversions based on field type
                    if field in ['total_cost', 'unit_cost', 'depreciation_value', 'scrap_value', 'net_book_value']:
                        if pd.isna(val):
                            converted = None
                        else:
                            clean_val = str(val).replace(',', '').replace('$', '').replace('₦', '').replace('NGN', '').strip()
                            converted = float(clean_val) if clean_val else None
                        print(f"  {field:25s} ({type(val).__name__:10s}) → float → {converted}")
                    
                    elif field == 'quantity':
                        if pd.isna(val):
                            converted = None
                        else:
                            converted = int(float(str(val).replace(',', '')))
                        print(f"  {field:25s} ({type(val).__name__:10s}) → int   → {converted}")
                    
                    elif field == 'useful_life':
                        if pd.isna(val):
                            converted = None
                        else:
                            converted = int(float(str(val)))
                        print(f"  {field:25s} ({type(val).__name__:10s}) → int   → {converted}")
                    
                    elif field == 'depreciation_percentage':
                        if pd.isna(val):
                            converted = None
                        else:
                            clean_val = str(val).replace('%', '').strip()
                            converted = float(clean_val)
                        print(f"  {field:25s} ({type(val).__name__:10s}) → float → {converted}")
                    
                    elif field == 'acquisition_date':
                        if pd.isna(val):
                            converted = None
                        else:
                            converted = pd.to_datetime(val, errors='coerce')
                        print(f"  {field:25s} ({type(val).__name__:10s}) → date  → {converted}")
                    
                    else:
                        converted = str(val) if not pd.isna(val) else None
                        print(f"  {field:25s} ({type(val).__name__:10s}) → str   → {converted}")
                
                except Exception as e:
                    print(f"  {field:25s} ({type(val).__name__:10s}) → ❌ ERROR: {e}")

def main():
    file_path = Path("tests/RHV TEST.xlsx")
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    print("\n🔍 Initial file inspection...")
    try:
        # First, check the raw structure
        df_raw = pd.read_excel(file_path, header=None, nrows=2)
        print(f"Raw first 2 rows (without header parsing):\n{df_raw}\n")
    except Exception as e:
        print(f"Could not inspect raw data: {e}\n")
    
    # Examine file
    df = examine_excel_file(file_path)
    
    if df is not None:
        # Test mappings
        mappings = test_column_mapping(df)
        
        # Test conversions
        test_data_conversion(df, mappings)
        
        print(f"\n{'='*80}")
        print("✅ IMPORT TEST COMPLETE")
        print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
