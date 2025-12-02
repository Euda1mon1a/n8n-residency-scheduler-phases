# Phase 2 Workflow Update: Field IDs Implementation

## Summary
Updated the Phase 2 Smart Resident Association workflow to use Airtable field IDs instead of field names throughout all operations. This ensures reliability and prevents issues when field names are changed in Airtable.

## Key Changes Made

### 1. Airtable Node Updates

#### Fetch Phase 1 Master Assignments
- **Before:** `{Half-Day of the Week of Blocks}`, `{Rotation Templates}`, `{Processing Phase}`
- **After:** `{fldHalfDayOfWeekBlocks}`, `{fldRotationTemplates}`, `{fldProcessingPhase}`

#### Fetch Residency Block Schedule
- **Before:** `{Resident}`
- **After:** `{fldq0D4a6GevQSbhz}` (Resident field ID)

#### Fetch Half-Day Blocks Reference
- **Before:** `{Date of Day of the Week of Block}`
- **After:** `{fldDateOfDayOfWeekBlock}`

### 2. JavaScript Code Updates

#### Phase 2: Smart Association Engine
Added comprehensive field ID mapping at the top of the code:

```javascript
const FIELD_IDS = {
  // Master Assignments table
  MA_HALF_DAY_OF_WEEK_BLOCKS: 'fldHalfDayOfWeekBlocks',
  MA_ROTATION_TEMPLATES: 'fldRotationTemplates',
  MA_PROCESSING_PHASE: 'fldProcessingPhase',
  MA_RESIDENT_FROM_RBS: 'fldResidentFromRBS',
  MA_PGY_LINK_FROM_RBS: 'fldPGYLinkFromRBS',
  // ... and more
  
  // Residency Block Schedule table
  RBS_RESIDENT: 'fldq0D4a6GevQSbhz',
  RBS_PGY_YEAR: 'fld1gvZ5vL0gkrJ4W',
  // ... and more
  
  // Half-Day Blocks Reference table
  HD_DATE_OF_DAY_OF_WEEK_BLOCK: 'fldDateOfDayOfWeekBlock',
  HD_TIME_OF_DAY: 'fldTimeOfDay',
  // ... and more
};
```

Updated all field references to use these constants while maintaining fallbacks to field names for backward compatibility.

#### Format Resident Associations for Airtable
Updated to use field IDs when creating the update payload:

```javascript
const FIELD_IDS = {
  RESIDENT_FROM_RBS: 'fldResidentFromRBS',
  PGY_LINK_FROM_RBS: 'fldPGYLinkFromRBS',
  RESIDENT_AVAILABLE: 'fldResidentAvailable',
  PROCESSING_PHASE: 'fldProcessingPhase',
  ASSIGNMENT_TYPE: 'fldAssignmentType',
  RESIDENT_SUBSTITUTION_APPLIED: 'fldResidentSubstitutionApplied',
  FINAL_ACTIVITY_NAME: 'fldFinalActivityName',
  ASSIGNMENT_SCORE: 'fldAssignmentScore',
  ASSIGNMENT_DATE: 'fldAssignmentDate'
};
```

All field assignments now use these IDs:
```javascript
fields: {
  [FIELD_IDS.RESIDENT_FROM_RBS]: [association.Resident_ID],
  [FIELD_IDS.PGY_LINK_FROM_RBS]: [association.PGY_Level],
  // ... etc
}
```

### 3. HTTP Request Node Update

#### Update Master Assignments with Residents
Simplified the JSON body to use the already-formatted fields object:

```json
{
  "fields": {{ JSON.stringify($json.fields) }}
}
```

This ensures all field IDs from the formatting step are properly sent to Airtable.

## Field ID Reference

### Master Assignments Table (tbl17gcDUtXc14Rjv)
| Field Name | Field ID |
|------------|----------|
| Half-Day of the Week of Blocks | fldHalfDayOfWeekBlocks |
| Rotation Templates | fldRotationTemplates |
| Processing Phase | fldProcessingPhase |
| Resident (from Residency Block Schedule) | fldResidentFromRBS |
| PGY Link (from Residency Block Schedule) | fldPGYLinkFromRBS |
| Resident Available | fldResidentAvailable |
| Assignment Type | fldAssignmentType |
| Resident Substitution Applied | fldResidentSubstitutionApplied |
| Final Activity Name | fldFinalActivityName |
| Assignment Score | fldAssignmentScore |
| Assignment Date | fldAssignmentDate |

### Residency Block Schedule Table (tbl3TfpZSGYGxlCIG)
| Field Name | Field ID |
|------------|----------|
| Name | fld9jU1b60KFqZSWx |
| Resident | fldq0D4a6GevQSbhz |
| Block | fldSm2tVzmgKpwAMH |
| Rotation | fldxZH0CjlYJ8V4eW |
| PGY Year | fld1gvZ5vL0gkrJ4W |

### Half-Day of the Week of Blocks Table (tblTP62YOkF75o5aO)
| Field Name | Field ID |
|------------|----------|
| Date of Day of the Week of Block | fldDateOfDayOfWeekBlock |
| Time of Day | fldTimeOfDay |
| Day of the Week of Block | fldDayOfTheWeekOfBlock |
| Block | fldBlock |
| Week of the Block | fldWeekOfTheBlock |

## Benefits

1. **Reliability**: Field ID-based operations are immune to field name changes in Airtable
2. **Consistency**: Uses the same approach as recommended in `.codex/config.yml` (`field_ref_mode: id`)
3. **Maintainability**: All field IDs are defined as constants at the top of each code block
4. **Backward Compatibility**: Code includes fallbacks to field names where appropriate
5. **Documentation**: Added comprehensive field ID mappings to workflow metadata

## Testing Recommendations

1. Verify all Airtable nodes can successfully query data using the new field IDs
2. Test the smart association engine with sample data
3. Confirm that HTTP PATCH requests successfully update Master Assignment records
4. Validate that all field references resolve correctly in both the filtering and data access operations
5. Check that metadata logging still works with human-readable names

## Notes

- Human-readable field names are retained in metadata fields (prefixed with `_metadata`) for logging and debugging purposes
- The workflow maintains backward compatibility by checking both field IDs and field names where data might come from external sources
- All filterByFormula expressions in Airtable nodes now use field IDs wrapped in curly braces: `{fldFieldID}`

## File Location
The updated workflow has been saved to: `/mnt/user-data/outputs/phase2-smart-resident-association-with-ids.json`
