# How to Test Asset Dialog Depreciation

## Manual Testing Guide

### Step-by-Step: Testing Depreciation in Asset Dialog

#### 1. Start the Application
```bash
python -m app.main
```

#### 2. Login
- Use your test credentials to login

#### 3. Navigate to Add Asset
- Click "Assets" menu
- Click any category (e.g., "IT Equipment")
- Click "Add Asset" button

#### 4. Test Depreciation Calculation

**Test Scenario: ₦250,000 asset with 4-year useful life**

##### Step A: Enter Basic Information
1. Asset ID: `TEST-DEPR-001`
2. Asset Description: `Test Depreciation Asset`
3. Category: Select any category
4. Supplier: `Test Supplier`
5. Location: Select any location

##### Step B: Set Financial Values
1. **Quantity**: `1`
2. **Unit Cost**: `250000`
   - Watch: Total Cost auto-updates to ₦250,000.00
   - Watch: Accumulated Depreciation auto-updates to ₦0.00
   - Watch: Net Book Value auto-updates to ₦250,000.00

3. **Useful Life**: `4` years

##### Step C: Select Depreciation Method
1. Click "Depreciation Method" dropdown
2. Try each method and observe changes:

**Option 1: Straight Line**
- Accumulated Depreciation: ₦0.00
- Net Book Value: ₦250,000.00
- (Annual depreciation is ₦56,250.00)

**Option 2: Declining Balance**
- Accumulated Depreciation: ₦0.00
- Net Book Value: ₦250,000.00
- (Annual depreciation is ₦109,414.67)

**Option 3: Double Declining Balance**
- Accumulated Depreciation: ₦0.00
- Net Book Value: ₦250,000.00
- (Annual depreciation is ₦125,000.00)

**Option 4: Sum of Years Digits**
- Accumulated Depreciation: ₦0.00
- Net Book Value: ₦250,000.00
- (Annual depreciation is ₦90,000.00)

#### Step D: Verify Dynamic Updates
1. Change Unit Cost to `500000`
   - Total Cost → ₦500,000.00
   - Accumulated Depreciation → ₦0.00
   - Net Book Value → ₦500,000.00
   
2. Change Quantity to `2`
   - Total Cost → ₦1,000,000.00
   - Accumulated Depreciation → ₦0.00
   - Net Book Value → ₦1,000,000.00

3. Change Useful Life to `8` years
   - Notice depreciation method recalculates

#### Step E: Save Asset
1. Click OK to save
2. Verify asset appears in asset list
3. Click on asset to edit and verify depreciation values persisted

## Automated Testing

### Run Depreciation Test Suite
```bash
python test_depreciation_calculation.py
```

Expected output:
```
✅ ALL DEPRECIATION TESTS PASSED
- For NEW assets (Year 1), Accumulated Depreciation = ₦0
- For NEW assets (Year 1), Net Book Value = Total Cost
- Each method calculates different Annual Depreciation amounts
```

## What to Verify ✅

### Correct Behavior:
1. ✅ Accumulated Depreciation = ₦0.00 for new assets
2. ✅ Net Book Value = Total Cost for new assets
3. ✅ Values update automatically when inputs change
4. ✅ Currency symbols (₦) display correctly
5. ✅ Thousands separators (,) display correctly
6. ✅ 2 decimal places (.00) always shown
7. ✅ Different methods produce different values
8. ✅ Fields are read-only (cannot manually edit)

### Expected Values for ₦250,000, 4 years:

| Method | Annual | Accumulated | Net Book |
|--------|--------|-------------|----------|
| Straight Line | ₦56,250.00 | ₦0.00 | ₦250,000.00 |
| Declining Balance | ₦109,414.67 | ₦0.00 | ₦250,000.00 |
| Double Declining | ₦125,000.00 | ₦0.00 | ₦250,000.00 |
| Sum of Years | ₦90,000.00 | ₦0.00 | ₦250,000.00 |

## Troubleshooting

### Issue: Depreciation values don't update when I change inputs
**Solution**: Ensure you're changing the fields in the correct order:
1. First set Quantity and Unit Cost (affects Total Cost)
2. Then set Useful Life and Depreciation Method
3. Changes should be instant

### Issue: Values show 0.00 for everything
**Solution**: Check that:
1. Unit Cost > 0
2. Quantity > 0
3. Useful Life > 0
4. Depreciation Method is selected

### Issue: Accumulated Depreciation is not 0
**Solution**: This dialog is for NEW assets only. For new assets:
- Accumulated Depreciation should ALWAYS be ₦0.00
- This is because the asset has just been acquired

## Files to Reference

- **Asset Dialog**: `app/gui/dialogs/asset_dialog.py`
- **UI Definition**: `app/gui/ui/asset_dialog.ui`
- **Depreciation Logic**: `app/core/models.py` (DepreciationMethod.calculate_depreciation)
- **Test Script**: `test_depreciation_calculation.py`

## Next Steps After Testing

1. ✅ Verify depreciation displays in asset table (already working)
2. ✅ Verify depreciation values saved to database
3. ✅ Test editing existing asset (should preserve depreciation)
4. ✅ Test all 4 depreciation methods in different scenarios
5. (Future) Implement depreciation schedule view
6. (Future) Implement depreciation report generation