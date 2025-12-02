# Field Mapping Standardization Issue and Solution

## Problem Summary

While all phases use the constant name `FIELD_IDS`, they map to different value types:

- **Phase 0**: Maps to field **names** (e.g., `FL_FACULTY: 'Faculty'`)
- **Phase 1**: Mixed approach with actual field **IDs** (e.g., `HD_HDOWOB_ID: 'fldHDoWoBID'`)
- **Phase 2**: Maps to actual field **IDs** (e.g., `MA_HALF_DAY_OF_WEEK_BLOCKS: 'fldHalfDayOfWeekBlocks'`)

This inconsistency is confusing for humans reading the code because:
1. The constant name `FIELD_IDS` suggests values are Airtable field IDs
2. Phase 0 actually stores field names, not IDs
3. Developers must remember which phase uses which convention

## Current State

### Phase 0 (Inconsistent)
```javascript
const FIELD_IDS = {
  FL_FACULTY: 'Faculty',           // Field NAME, not ID
  FL_LEAVE_START: 'Leave Start',   // Field NAME, not ID
  RR_RESIDENT: 'fldq0D4a6GevQSbhz',  // Field ID (only one!)
  ...
}
```

### Phase 1 (Mixed)
```javascript
const FIELD_IDS = {
  HD_HDOWOB_ID: 'fldHDoWoBID',                    // Field ID ✓
  RT_ROTATION_SLOT_ID: 'Rotation Slot ID',        // Field NAME (with comment "// Field ID needed")
  MA_HALF_DAY_OF_WEEK_BLOCKS: 'fldHalfDayOfWeekBlocks', // Field ID ✓
  ...
}
```

### Phase 2 (Consistent - Gold Standard)
```javascript
const FIELD_IDS = {
  MA_HALF_DAY_OF_WEEK_BLOCKS: 'fldHalfDayOfWeekBlocks', // Field ID ✓
  MA_ROTATION_TEMPLATES: 'fldRotationTemplates',        // Field ID ✓
  RBS_RESIDENT: 'fldq0D4a6GevQSbhz',                   // Field ID ✓
  ...
}
```

## Solution

### Option 1: Use Actual Field IDs (Recommended)
Update Phase 0 and Phase 1 to consistently use actual Airtable field IDs like Phase 2.

**Pros:**
- Resilient to field name changes in Airtable
- Matches the constant name `FIELD_IDS`
- Consistent with Phase 2 (the gold standard)
- More professional and maintainable

**Cons:**
- Requires obtaining actual field IDs from Airtable

### Option 2: Rename Constants to Match Content
If actual field IDs are not available, rename constants to accurately reflect their content:
- Phase 0: `FIELD_NAMES` or `FIELD_MAP`
- Phase 1: Update mixed entries to be consistent
- Phase 2: Keep as `FIELD_IDS`

## Implementation Plan

We'll implement Option 1 (use actual field IDs everywhere):

1. **Phase 0**: Update all field name values to use actual Airtable field IDs
2. **Phase 1**: Update remaining field name values to use actual Airtable field IDs
3. **Verification**: Ensure all three phases use the same convention
4. **Testing**: Validate that fallback patterns still work (e.g., `data[FIELD_IDS.FL_FACULTY] || data['Faculty']`)

## Expected Outcome

After standardization, all phases will have consistent field mappings:

```javascript
// All phases will follow this pattern
const FIELD_IDS = {
  TABLE_FIELD_NAME: 'fldActualAirtableID',  // Consistent across all phases
  ...
}

// Usage pattern (consistent across all phases)
const value = data[FIELD_IDS.TABLE_FIELD_NAME] || data['Field Name Fallback'];
```

This makes the codebase more maintainable and less confusing for humans working with the code.
