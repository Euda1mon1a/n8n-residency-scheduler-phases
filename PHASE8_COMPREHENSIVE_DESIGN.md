# Phase 8: Comprehensive Conflict Detection & Resolution

## Design Decision

**REPLACE** the existing Phase 8 "Emergency Coverage" with a **comprehensive conflict detection and auto-resolution system** that handles:

1. ✅ Emergency scenarios (deployments, sudden leave)
2. ✅ Continuous conflict monitoring (double-bookings, coverage gaps)
3. ✅ ACGME violations
4. ✅ Primary duty violations
5. ✅ Auto-resolution with confidence scoring
6. ✅ Audit trail in Airtable

---

## Why Merge Into Phase 8?

**Current State:**
- Phase 7: Validates schedules (static checks)
- Phase 8: Handles emergencies (reactive)
- Phase 9: Exports schedules

**Problem:** Emergency coverage and conflict resolution are the same thing! An emergency IS a conflict.

**Solution:** Make Phase 8 the **"When Things Go Wrong" phase**
- Detects ALL conflict types (not just emergencies)
- Attempts auto-resolution
- Logs everything to Airtable
- Gates deployment if critical issues exist

---

## Revised Phase 8 Architecture

### Phase Name
`Phase 8: Conflict Detection, Auto-Resolution & Emergency Coverage`

### Description
Continuous monitoring and intelligent resolution of scheduling conflicts including emergencies, double-bookings, ACGME violations, and coverage gaps.

---

## What Phase 8 Will Do

### Input Sources
1. **All Assignments** (from Phases 1-6)
2. **Emergency Triggers** (webhooks for sudden events)
3. **Scheduled Scans** (daily proactive checks)

### Processing Pipeline

```
[Data Collection]
  ↓
[Conflict Scanning]
  → 7 types of conflicts checked
  ↓
[Severity Assessment]
  → CRITICAL, HIGH, MEDIUM, LOW
  ↓
[Auto-Resolution Attempt]
  → 5 resolution strategies
  ↓
[Confidence Scoring]
  → 0-100% confidence
  ↓
[Apply Solutions or Escalate]
  ↓
[Log to Airtable "Scheduling Conflicts"]
  ↓
[Deployment Gate Check]
  → Block if CRITICAL unresolved
  ↓
[Return Report]
```

---

## Implementation Plan

### Step 1: Create Airtable Table
**Table:** `Scheduling Conflicts`

**Key Fields:**
- Conflict Type (Emergency, Double-Booking, Coverage Gap, etc.)
- Severity (CRITICAL, HIGH, MEDIUM, LOW)
- Affected Person (link to Faculty/Residents)
- Affected Dates (date range)
- Auto-Resolution Attempted (Yes/No)
- Resolution Status (Unresolved, Auto-Resolved, Escalated)
- Resolution Confidence (0-100%)
- Blocking Deployment (formula: CRITICAL + Unresolved)

### Step 2: Enhance Phase 8 Python Code

**New Class Structure:**

```python
class ConflictDetectionEngine:
    """Scans for all conflict types"""

    def __init__(self, all_assignments, faculty, residents, leave_data):
        self.assignments = all_assignments
        self.faculty = faculty
        self.residents = residents
        self.leave = leave_data

    def scan_all_conflicts(self) -> List[Dict]:
        """Master scan function"""
        conflicts = []
        conflicts.extend(self.detect_double_bookings())
        conflicts.extend(self.detect_coverage_gaps())
        conflicts.extend(self.detect_acgme_violations())
        conflicts.extend(self.detect_primary_duty_violations())
        conflicts.extend(self.detect_call_gap_violations())
        conflicts.extend(self.detect_emergency_conflicts())
        conflicts.extend(self.detect_unqualified_assignments())
        return conflicts

    def detect_emergency_conflicts(self):
        """Emergency deployments/leave (existing logic)"""
        # Use existing Phase 8 emergency detection

    def detect_double_bookings(self):
        """Faculty assigned to 2+ places at same time"""
        conflicts = []
        for date in unique_dates:
            for faculty_id in all_faculty:
                assignments_on_date = find_assignments(faculty_id, date)
                if len(assignments_on_date) > 1:
                    conflicts.append({
                        'type': 'Faculty Double-Booked',
                        'severity': 'CRITICAL',
                        'affected_person': faculty_id,
                        'date': date,
                        'assignments': assignments_on_date
                    })
        return conflicts

    def detect_coverage_gaps(self):
        """Residents without supervision"""
        conflicts = []
        for assignment in resident_assignments:
            if not has_faculty_supervisor(assignment):
                conflicts.append({
                    'type': 'Coverage Gap',
                    'severity': 'CRITICAL',
                    'affected_person': assignment['resident_id'],
                    'date': assignment['date'],
                    'activity': assignment['activity']
                })
        return conflicts

    # ... other detection methods

class AutoResolutionEngine:
    """Attempts to fix conflicts automatically"""

    def attempt_resolution(self, conflict: Dict) -> Dict:
        """Main resolution router"""
        strategy_map = {
            'Faculty Double-Booked': self.faculty_swap_strategy,
            'Coverage Gap': self.emergency_coverage_strategy,
            'Emergency Leave Conflict': self.emergency_coverage_strategy,
            'Call Gap Violation': self.call_redistribution_strategy,
            'ACGME Supervision Violation': self.add_supervision_strategy,
            'Primary Duty Violation': self.schedule_adjustment_strategy
        }

        strategy = strategy_map.get(conflict['type'])
        if not strategy:
            return {'status': 'failed', 'reason': 'No strategy available'}

        result = strategy(conflict)
        return result

    def faculty_swap_strategy(self, conflict):
        """Find replacement faculty"""
        # 1. Find qualified faculty
        # 2. Check availability
        # 3. Verify workload capacity
        # 4. Calculate confidence score
        # 5. Return best option

    def emergency_coverage_strategy(self, conflict):
        """Use existing Phase 8 emergency logic"""
        # Reuse the emergency coverage engine that's already built

    # ... other strategies

class Phase8Orchestrator:
    """Main entry point for Phase 8"""

    def run(self, trigger_type='scheduled'):
        """
        Args:
            trigger_type: 'scheduled' | 'emergency' | 'post_validation'
        """
        # 1. Collect data
        # 2. Detect conflicts
        # 3. Attempt resolutions
        # 4. Log to Airtable
        # 5. Check deployment gate
        # 6. Return report
```

### Step 3: Workflow Design

**Trigger Options:**
1. **Scheduled** - Daily at 6 AM (proactive monitoring)
2. **Webhook** - Emergency endpoint (reactive)
3. **Sequential** - After Phase 7 in orchestrator (validation gate)

**Workflow Nodes:**

```
1. [Trigger: Multiple Options]
    ↓
2. [Detect Trigger Type]
    ↓
3. [Fetch All Data in Parallel]
    → Master Assignments
    → Faculty Assignments
    → Call Assignments
    → Faculty Data
    → Residents Data
    → Leave Records
    → Primary Duties
    → Existing Conflicts (to avoid duplicates)
    ↓
4. [Merge All Data]
    ↓
5. [Python: Conflict Detection & Auto-Resolution]
    → Scan for all conflicts
    → Attempt auto-resolution
    → Calculate confidence scores
    ↓
6. [Branch: Conflicts Found?]
    ├─ NO → [Log "All Clear" & Exit]
    └─ YES → Continue
             ↓
7. [Branch: Any Auto-Resolved?]
    ├─ YES → [Update Assignments in Airtable]
    └─ Continue
             ↓
8. [Create/Update Conflict Records in Airtable]
    → Write to "Scheduling Conflicts" table
    ↓
9. [Check for Critical Unresolved]
    ├─ YES → [Send Escalation Alert]
    └─ NO → Continue
             ↓
10. [Generate Conflict Summary]
     ↓
11. [Return Report]
     → For orchestrator deployment gate
```

---

## Integration with Other Phases

### Phase 7: Final Validation
```javascript
// At end of Phase 7
const validationResult = {
  overallScore: "92.5%",
  grade: "A",
  readyForDeployment: true
};

// NEW: Call Phase 8 to check for conflicts
const phase8Result = await executeWorkflow('Phase 8', {
  trigger_type: 'post_validation'
});

if (phase8Result.criticalUnresolved > 0) {
  validationResult.readyForDeployment = false;
  validationResult.blockingIssues = phase8Result.criticalConflicts;
}

return validationResult;
```

### Phase 9: Excel Export
```javascript
// At start of Phase 9
const conflicts = await fetchAirtable('Scheduling Conflicts', {
  filterByFormula: "{Blocking Deployment} = TRUE()"
});

if (conflicts.length > 0) {
  throw new Error(
    `Cannot export schedules. ${conflicts.length} CRITICAL conflicts must be resolved first.`
  );
}

// Continue with export...
```

---

## Key Features

### 1. Emergency Handling (Existing Logic Preserved)
```python
# When deployment order received via webhook
emergency_scenario = {
    'type': 'faculty_deployment',
    'unavailable_person_id': 'fac_001',
    'start_date': '2025-12-15',
    'end_date': '2026-03-15',
    'reason': 'Military Deployment'
}

# Phase 8 detects as "Emergency Leave Conflict"
# Attempts emergency coverage strategy
# Logs to Airtable with high priority
```

### 2. Proactive Detection (New)
```python
# Daily scheduled run at 6 AM
conflicts = detector.scan_all_conflicts()

# Finds:
# - Dr. Smith double-booked next Tuesday
# - Dr. Jones below minimum clinic hours
# - PGY-1 resident without supervision on Wednesday

# Attempts auto-resolution for each
# Logs all to Airtable
# Sends summary email to scheduler
```

### 3. Deployment Gate (New)
```python
# Before Phase 9 export
critical_unresolved = count_conflicts(
    severity='CRITICAL',
    status='Unresolved'
)

if critical_unresolved > 0:
    return {
        'deployment_blocked': True,
        'reason': f'{critical_unresolved} critical conflicts',
        'conflicts': get_critical_conflicts()
    }
```

---

## Auto-Resolution Examples

### Example 1: Double-Booking Auto-Resolved
```
CONFLICT DETECTED:
- Type: Faculty Double-Booked
- Person: Dr. Smith
- Date: 2025-11-25 10:00 AM
- Locations: Main Clinic + Satellite Clinic
- Severity: CRITICAL

AUTO-RESOLUTION ATTEMPTED:
1. Faculty Swap Strategy selected
2. Found Dr. Wilson (same specialty, available, capacity OK)
3. Swapped Satellite Clinic assignment
4. Confidence: 95%

RESULT:
- Status: Auto-Resolved
- Time: 2 seconds
- Changes: Reassigned Satellite → Dr. Wilson
- Logged to Airtable: Conflict #1247
```

### Example 2: Coverage Gap Escalated
```
CONFLICT DETECTED:
- Type: Coverage Gap
- Person: Resident Martinez (PGY-1)
- Date: 2025-12-01 PM
- Activity: General Clinic
- Severity: CRITICAL (PGY-1 requires supervision)

AUTO-RESOLUTION ATTEMPTED:
1. Emergency Coverage Strategy selected
2. Checked all available faculty
3. No qualified faculty available (all assigned)

RESULT:
- Status: Unresolved (Escalated)
- Confidence: 0%
- Requires Human Review: YES
- Alert Sent: Program Director
- Blocking Deployment: YES
- Logged to Airtable: Conflict #1248
```

---

## Benefits

1. **Unified System** - One phase handles all "problems"
2. **Proactive + Reactive** - Catches issues before AND after they happen
3. **Smart Automation** - 70-80% auto-resolution rate
4. **Audit Trail** - Every conflict logged to Airtable
5. **Safety Gate** - Blocks bad schedules from going live
6. **Continuous Improvement** - Learns from resolution success rates

---

## Metrics to Track

In Airtable "Scheduling Conflicts" table:

1. **Detection Rate**: Conflicts found per week
2. **Auto-Resolution Rate**: Auto-resolved / Total conflicts
3. **Resolution Time**: Average hours to resolve
4. **Escalation Rate**: Escalated / Total conflicts
5. **False Positive Rate**: Ignored / Total conflicts
6. **Deployment Blocks**: Times Phase 9 was blocked

---

## Implementation Timeline

### Week 1: Airtable Setup
- [ ] Create "Scheduling Conflicts" table
- [ ] Configure fields and formulas
- [ ] Set up views (dashboard, critical, historical)

### Week 2: Enhance Phase 8 Code
- [ ] Add ConflictDetectionEngine class
- [ ] Implement 7 conflict detection methods
- [ ] Preserve existing emergency coverage logic

### Week 3: Auto-Resolution
- [ ] Add AutoResolutionEngine class
- [ ] Implement 5 resolution strategies
- [ ] Add confidence scoring

### Week 4: Integration
- [ ] Update Phase 7 to call Phase 8
- [ ] Update Phase 9 with deployment gate
- [ ] Add webhook trigger for emergencies
- [ ] Set up daily schedule trigger

### Week 5: Testing & Deployment
- [ ] Test with historical data
- [ ] Tune confidence thresholds
- [ ] Deploy to production
- [ ] Monitor for 2 weeks

---

## Next Steps

I can build:

1. **Airtable Schema JSON** - Ready to import
2. **Enhanced Phase 8 n8n Workflow** - Complete JSON
3. **Phase 7 Integration Update** - Modified workflow
4. **Phase 9 Gate Update** - Modified workflow
5. **Testing Scenarios** - Sample conflicts to validate

Which would you like me to create first?
