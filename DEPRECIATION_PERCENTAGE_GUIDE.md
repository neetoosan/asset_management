# Depreciation Percentage and Year-End Accounting Feature

## Overview

The Asset Management System now supports **annual depreciation percentage** instead of depreciation methods. Each asset can have a custom depreciation percentage that is applied annually on December 31st.

---

## Key Features

### 1. Depreciation Percentage Field
- **Field Name**: "Annual Depreciation %"
- **Range**: 0% to 100%
- **Step**: 0.5% (for precise control)
- **Validation**: Must be greater than 0% to save an asset
- **Default**: 0% (must be entered manually)

### 2. Year-End Accounting (December 31)
- Depreciation accumulates **once per year on December 31st**
- Example: If an asset is added on **November 18, 2025** with 10% annual depreciation:
  - **2025**: No depreciation (added mid-year)
  - **Dec 31, 2025**: First depreciation applies (10% of total cost)
  - **Dec 31, 2026**: Second depreciation applies (10% of remaining book value)
  - And so on...

### 3. Annual Depreciation Calculation
```
Annual Depreciation Amount = Total Cost × (Depreciation Percentage / 100)

Example:
- Asset Cost: ₦1,000,000
- Depreciation %: 5%
- Annual Depreciation = ₦1,000,000 × (5/100) = ₦50,000 per year
```

### 4. Accumulated Depreciation Logic
- **For New Assets**: Accumulated depreciation = 0 until Dec 31 of first year
- **Each Year**: On Dec 31, accumulated depreciation increases by the annual amount
- **Net Book Value**: Total Cost - Accumulated Depreciation

---

## Database Changes

### New Column
A new column `depreciation_percentage` (REAL, default 0.0) was added to the `assets` table.

**Migration Script**: `migrations/add_depreciation_percentage.py`

Run the migration:
```bash
python migrations/add_depreciation_percentage.py up
```

---

## Using the Feature

### Adding a New Asset

1. Open the "Add Asset" dialog
2. Fill in all required fields
3. **Important**: Set the "Annual Depreciation %" field
   - Use the spinner buttons or click and type the value
   - Example: Enter `5.00` for 5% annual depreciation
4. The "Annual Depreciation (₦)" field will auto-calculate based on total cost and percentage
5. Click "OK" to save

### Editing an Existing Asset

1. Open an asset for editing
2. The "Annual Depreciation %" field will show the currently saved percentage
3. Modify the percentage if needed
4. The annual depreciation amount updates automatically
5. Click "OK" to save changes

### Example Scenarios

#### Scenario 1: Hospital Equipment (Quick Depreciation)
- Asset: CT Scan Machine
- Cost: ₦50,000,000
- Depreciation %: 15% (deprecates quickly due to technology obsolescence)
- Annual Depreciation: ₦7,500,000

#### Scenario 2: Building (Slow Depreciation)
- Asset: Office Building
- Cost: ₦200,000,000
- Depreciation %: 2% (slower depreciation for real estate)
- Annual Depreciation: ₦4,000,000

#### Scenario 3: Furniture
- Asset: Office Chairs (50 units)
- Cost: ₦250,000
- Depreciation %: 5%
- Annual Depreciation: ₦12,500

---

## Technical Implementation

### Asset Dialog Changes

**File**: `app/gui/dialogs/asset_dialog.py`

Key methods:
- `setup_calculations()`: Initializes the depreciation percentage spinbox with proper ranges and increments
- `calculate_depreciation()`: Calculates annual depreciation based on percentage (not method-based)
- `load_asset_data()`: Loads existing depreciation percentage when editing
- `validate()`: Ensures percentage is greater than 0%
- `get_data()`: Includes depreciation_percentage in saved asset data

**Removed**: Depreciation method calculations are no longer used for computing depreciation

**File**: `app/gui/ui/asset_dialog.ui`
- Added QDoubleSpinBox for "Annual Depreciation %"
- Range: 0.00 to 100.00
- Suffix: " %" for clarity
- Step: 0.50

### Model Changes

**File**: `app/core/models.py`

Added column to Asset model:
```python
depreciation_percentage = Column(Float, default=0.0)  # Annual depreciation percentage (0-100)
```

### Database Migration

**File**: `migrations/add_depreciation_percentage.py`

Adds the depreciation_percentage column to the assets table:
- Data type: REAL (float)
- Default value: 0.0
- Compatible with both SQLite and PostgreSQL

---

## Year-End Accounting Process (Future Implementation)

The system is designed for automatic year-end processing. In future versions, a background job or scheduled task will:

1. **Every December 31st**:
   - Find all active assets
   - Calculate 1 year of depreciation based on the percentage
   - Update accumulated_depreciation
   - Update net_book_value

2. **Calculation**:
   ```
   annual_depreciation = total_cost × (depreciation_percentage / 100)
   accumulated_depreciation += annual_depreciation
   net_book_value = total_cost - accumulated_depreciation
   ```

3. **Audit Trail**:
   - All depreciation updates recorded in audit log
   - Batch year-end adjustment documented

---

## Validation Rules

✅ **Required**:
- Depreciation percentage must be > 0%

✅ **Range**:
- Minimum: 0.01%
- Maximum: 100%

✅ **Precision**:
- 2 decimal places
- Increments by 0.5%

---

## Reports and Views

Assets now display:
- **Annual Depreciation Amount** (₦): Auto-calculated based on percentage
- **Accumulated Depreciation**: Updated on Dec 31 each year
- **Net Book Value**: Current value after accumulated depreciation
- **Depreciation %**: The configured annual rate

---

## FAQ

**Q: What if I don't enter a depreciation percentage?**
A: The system requires it - validation will show an error: "Annual Depreciation percentage must be greater than 0%"

**Q: Can I change the percentage after asset creation?**
A: Yes! Edit the asset and modify the percentage. The annual depreciation amount updates automatically.

**Q: How is depreciation applied to mid-year purchases?**
A: Mid-year purchases accumulate depreciation starting December 31 of the same year. They count as "Year 1" if purchased before Dec 31.

**Q: What depreciation percentage should I use for different assets?**
A: This depends on your company's accounting policy. Common ranges:
- Buildings: 2-5%
- Machinery: 5-10%
- Equipment: 10-20%
- Computer/IT: 20-33%
- Furniture: 5-10%

**Q: Can I use different percentages for the same asset class?**
A: Yes! Each asset has its own percentage, allowing for individual valuation considerations.

---

## Support & Updates

For questions or issues with the depreciation feature, contact the development team.

This feature is production-ready as of Build [VERSION].
