# Scheduling Conflicts Table Setup Guide

## Overview

This document provides step-by-step instructions for creating the **"Scheduling Conflicts"** table in your Airtable base for continuous conflict monitoring and auto-resolution.

---

## Table Purpose

The Scheduling Conflicts table tracks all scheduling issues that arise throughout the academic year, attempts automatic resolution, and logs results for audit trail and continuous improvement.

---

## Setup Method Options

### Option 1: Manual Setup (Recommended for Control)
Follow the step-by-step guide below to create the table manually in Airtable.

### Option 2: Automated Setup (n8n Workflow)
Use the provided n8n workflow `setup-conflicts-table.json` to create the table automatically via Airtable API.

---

## Option 1: Manual Setup Instructions

### Step 1: Create the Table

1. Open your Airtable base: `appDgFtrU7njCKDW5`
2. Click **"+"** to add a new table
3. Name it: **`Scheduling Conflicts`**
4. Delete the default fields (we'll add custom ones)

### Step 2: Add Basic Fields (These can be imported via CSV)

Create these fields in order:

| Field Name | Field Type | Configuration |
|------------|------------|---------------|
| Conflict Type | Single select | Options: `Faculty Double-Booked`, `Coverage Gap`, `ACGME Supervision Violation`, `Primary Duty Violation`, `Call Gap Violation`, `Unqualified Assignment`, `Emergency Leave Conflict`, `Deployment Conflict` |
| Severity | Single select | Options: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| Affected Date Start | Date | Date only (no time) |
| Affected Date End | Date | Date only (no time) |
| Conflict Description | Long text | Allow rich text formatting |
| Detection Phase | Single select | Options: `Phase 7 (Validation)`, `Phase 8 (Emergency)`, `Continuous Monitor`, `Manual Entry` |
| Auto-Resolution Attempted | Checkbox | Default: unchecked |
| Auto-Resolution Method | Single select | Options: `Faculty Swap`, `Call Redistribution`, `Emergency Coverage`, `Schedule Adjustment`, `Not Attempted`, `No Solution Found` |
| Resolution Status | Single select | Options: `Unresolved`, `Auto-Resolved`, `Manual-Resolved`, `Escalated`, `Acknowledged`, `Ignored (Low Priority)` |
| Resolution Confidence | Number | Precision: 0, Format: Percent |
| Resolution Notes | Long text | Allow rich text formatting |
| Resolved By | Single select | Options: `System`, `Scheduler`, `Program Director`, `Admin`, `Unresolved` |
| Resolved At | Date | Include time |
| Requires Human Review | Checkbox | Default: unchecked |
| Escalation Reason | Long text | Plain text |
| Impact Score | Number | Precision: 0, Format: Integer |

### Step 3: Add Auto-Generated Fields

| Field Name | Field Type | Configuration |
|------------|------------|---------------|
| Conflict ID | Autonumber | Starting number: 1 |
| Date Detected | Created time | Use GMT |
| Last Updated | Last modified time | Use GMT |

### Step 4: Add Link Fields (Must be done AFTER related tables exist)

| Field Name | Field Type | Configuration |
|------------|------------|---------------|
| Affected Person | Link to another record | Link to: `Faculty` table<br>Allow linking to multiple records |
| Affected Assignments | Link to another record | Link to: `Master Assignments` table<br>Allow linking to multiple records |
| Applied Solution | Link to another record | Link to: `Master Assignments` table<br>Allow linking to multiple records |

**Note:** If you need to link to Residents as well, add another field:
- **Affected Resident**: Link to `Residents` table

### Step 5: Add Lookup Fields (Depend on Link fields)

| Field Name | Field Type | Configuration |
|------------|------------|---------------|
| Affected Person Name | Lookup | From: `Affected Person` → `Faculty` (or `Last Name`) |
| Assignment Count | Count | Count of: `Affected Assignments` |

### Step 6: Add Formula Fields

#### Affected Date Range (Days)
```
DATETIME_DIFF({Affected Date End}, {Affected Date Start}, 'days') + 1
```

#### Resolution Time (Hours)
```
IF(
  {Resolved At},
  DATETIME_DIFF({Resolved At}, {Date Detected}, 'hours'),
  BLANK()
)
```

#### Blocking Deployment
```
AND(
  {Severity} = "CRITICAL",
  {Resolution Status} = "Unresolved"
)
```

### Step 7: Add JSON/Long Text Field for Complex Data

| Field Name | Field Type | Configuration |
|------------|------------|---------------|
| Replacement Options | Long text | Used to store JSON array of auto-resolution options |

---

## Field Descriptions

### Critical Fields

**Conflict Type**
- What kind of problem was detected
- Used to determine which auto-resolution strategy to use

**Severity**
- `CRITICAL`: Blocks deployment, requires immediate attention
- `HIGH`: Should be resolved soon, affects quality
- `MEDIUM`: Should be addressed, not urgent
- `LOW`: Informational, can be deferred

**Affected Date Start/End**
- Date range when the conflict affects the schedule
- Used to calculate impact score

**Resolution Status**
- `Unresolved`: Not fixed yet
- `Auto-Resolved`: System fixed it automatically
- `Manual-Resolved`: Human intervention required and completed
- `Escalated`: Sent to leadership for decision
- `Acknowledged`: Noted but accepted as-is
- `Ignored (Low Priority)`: Not worth fixing

**Auto-Resolution Attempted**
- `TRUE`: Phase 8 tried to fix this automatically
- `FALSE`: Human-detected or system chose not to attempt

**Resolution Confidence**
- 0-100% how confident the system is in the auto-fix
- Only relevant if Auto-Resolved
- Low confidence (<80%) may trigger human review

**Blocking Deployment**
- Formula field that returns TRUE if:
  - Severity = CRITICAL AND
  - Resolution Status = Unresolved
- Used by Phase 9 to prevent exporting bad schedules

---

## Views to Create

### 1. Dashboard (Default View)
- **Filter:** `{Resolution Status} != "Ignored (Low Priority)"`
- **Sort:**
  1. `{Severity}` descending
  2. `{Date Detected}` ascending
- **Group by:** `{Severity}`
- **Color:** Severity (Red = Critical, Orange = High, etc.)

### 2. Critical Blockers
- **Filter:** `{Blocking Deployment} = TRUE()`
- **Sort:** `{Date Detected}` ascending
- **Hide fields:** Less important fields for focus
- **Color:** All red

### 3. Auto-Resolution Success
- **Filter:** `{Auto-Resolution Attempted} = TRUE()`
- **Group by:** `{Auto-Resolution Method}`
- **Show:** Summary of success rates

### 4. Pending Review
- **Filter:** `{Requires Human Review} = TRUE() AND {Resolution Status} = "Escalated"`
- **Sort:** `{Date Detected}` ascending

### 5. Historical Log
- **Filter:** None (show all)
- **Sort:** `{Date Detected}` descending
- **Group by:** Week of `{Date Detected}`

---

## CSV Template for Initial Import

Save this as `scheduling-conflicts-template.csv`:

```csv
Conflict Type,Severity,Affected Date Start,Affected Date End,Conflict Description,Detection Phase,Auto-Resolution Attempted,Auto-Resolution Method,Resolution Status,Resolution Confidence,Resolution Notes,Resolved By,Escalation Reason,Impact Score,Requires Human Review
Faculty Double-Booked,CRITICAL,2025-11-25,2025-11-25,Dr. Smith assigned to Main Clinic and Satellite Clinic at same time,Continuous Monitor,TRUE,Faculty Swap,Auto-Resolved,95,Reassigned Satellite Clinic to Dr. Wilson,System,,0,FALSE
Coverage Gap,CRITICAL,2025-12-01,2025-12-01,Resident Martinez (PGY-1) has no faculty supervisor for General Clinic,Phase 7 (Validation),TRUE,No Solution Found,Unresolved,0,No qualified faculty available,Unresolved,All faculty fully assigned - need to add coverage,10,TRUE
```

**To import:**
1. Create the basic fields first (Step 2 above)
2. In Airtable, click table menu → Import → CSV
3. Upload the template
4. This will create sample records to verify structure
5. Delete sample records once verified

---

## Option 2: Automated Setup (n8n Workflow)

An n8n workflow is provided: `setup-conflicts-table.json`

### How It Works

The workflow uses Airtable's Meta API to:
1. Create the "Scheduling Conflicts" table
2. Add all field types (text, select, checkbox, etc.)
3. Configure formulas
4. Set up single-select options

### Limitations

**Cannot create via API:**
- Link fields (must add manually)
- Lookup fields (must add manually)
- Count fields (must add manually)

**After running the workflow, manually add:**
1. Affected Person (Link to Faculty)
2. Affected Assignments (Link to Master Assignments)
3. Applied Solution (Link to Master Assignments)
4. Affected Person Name (Lookup)
5. Assignment Count (Count)

### Usage

1. Import `setup-conflicts-table.json` to n8n
2. Update the base ID if different
3. Run the workflow once
4. Manually add link/lookup fields
5. Create views

---

## Integration with Phase 8

Once the table is created, Phase 8 will automatically:

1. **Detect conflicts** during validation
2. **Attempt auto-resolution** using built-in strategies
3. **Write results** to this table via Airtable API
4. **Update status** when conflicts are resolved

### Expected Data Flow

```
Phase 8 Runs
    ↓
Scans all assignments for conflicts
    ↓
Finds: Dr. Smith double-booked on 11/25
    ↓
Attempts: Faculty Swap strategy
    ↓
Success: Reassigns to Dr. Wilson
    ↓
Creates record in Scheduling Conflicts:
  - Conflict Type: Faculty Double-Booked
  - Severity: CRITICAL
  - Status: Auto-Resolved
  - Confidence: 95%
  - Method: Faculty Swap
```

---

## Maintenance

### Daily Tasks
- Review "Critical Blockers" view
- Resolve escalated conflicts
- Acknowledge low-priority conflicts

### Weekly Tasks
- Review "Auto-Resolution Success" rates
- Tune confidence thresholds if needed
- Archive resolved conflicts older than 90 days

### Monthly Tasks
- Analyze conflict trends
- Update resolution strategies
- Review and improve detection rules

---

## Metrics to Track

Create a summary view or dashboard to track:

1. **Detection Rate**: Conflicts per week
2. **Auto-Resolution Rate**: % auto-resolved
3. **Average Resolution Time**: Hours to resolve
4. **Escalation Rate**: % requiring human review
5. **Deployment Blocks**: Times Phase 9 was stopped

---

## Troubleshooting

### "Blocking Deployment" not working
- Check formula syntax in field
- Verify Severity values match exactly (case-sensitive)
- Ensure Resolution Status options match

### Link fields not populating
- Verify target table exists
- Check that Phase 8 is using correct record IDs
- Ensure API permissions allow writing to linked records

### Auto-resolution not logging
- Check Phase 8 has Airtable credentials
- Verify table name matches exactly: "Scheduling Conflicts"
- Check n8n execution logs for errors

---

## Next Steps After Table Creation

1. ✅ Create table using this guide
2. Test with manual entries
3. Run Phase 8 in test mode
4. Verify records are created correctly
5. Tune auto-resolution strategies
6. Deploy to production
7. Monitor for first week
8. Adjust thresholds as needed

---

## Support

If you encounter issues:
1. Check field names match exactly (case-sensitive)
2. Verify formula syntax
3. Test with manual record creation first
4. Review Phase 8 execution logs in n8n

---

## Appendix: Complete Field Reference

| Field Name | Type | Required | Notes |
|------------|------|----------|-------|
| Conflict ID | Autonumber | Auto | Primary key |
| Date Detected | Created time | Auto | When detected |
| Last Updated | Last modified time | Auto | Last change |
| Conflict Type | Single select | Yes | Category |
| Severity | Single select | Yes | Priority level |
| Affected Date Start | Date | Yes | First date affected |
| Affected Date End | Date | Yes | Last date affected |
| Affected Date Range (Days) | Formula | Auto | Calculated duration |
| Affected Person | Link | No | Link to Faculty/Residents |
| Affected Person Name | Lookup | Auto | From linked record |
| Affected Assignments | Link | No | Link to assignments |
| Assignment Count | Count | Auto | Count of links |
| Conflict Description | Long text | Yes | Human-readable summary |
| Detection Phase | Single select | Yes | Which phase found it |
| Auto-Resolution Attempted | Checkbox | Yes | Did system try to fix |
| Auto-Resolution Method | Single select | If attempted | How it tried |
| Resolution Status | Single select | Yes | Current state |
| Resolution Confidence | Number | If auto-resolved | 0-100% |
| Resolution Notes | Long text | No | What was done |
| Resolved By | Single select | If resolved | Who/what fixed it |
| Resolved At | Date/time | If resolved | When fixed |
| Resolution Time (Hours) | Formula | Auto | Time to resolve |
| Requires Human Review | Checkbox | No | Escalate flag |
| Escalation Reason | Long text | If escalated | Why needs human |
| Impact Score | Number | Yes | Severity metric |
| Blocking Deployment | Formula | Auto | Critical + unresolved |
| Replacement Options | Long text | No | JSON data |
| Applied Solution | Link | If resolved | Link to new assignments |

---

**Table is ready for Phase 8 integration once created!**
