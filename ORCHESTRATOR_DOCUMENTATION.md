# Master Orchestrator Documentation
## Medical Residency Scheduler v2.0

---

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [How It Works](#how-it-works)
4. [Setup Instructions](#setup-instructions)
5. [Usage Guide](#usage-guide)
6. [Monitoring & Logging](#monitoring--logging)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## Overview

The **Master Orchestrator** is a single n8n workflow that automatically executes all 9 scheduling phases in the correct sequence, handling data flow between phases and providing comprehensive logging.

### Key Features
- ✅ **One-button execution** - Click "Run" to execute entire pipeline
- ✅ **Automatic data flow** - Phase outputs automatically passed as inputs
- ✅ **Sequential execution** - Phases run in proper dependency order
- ✅ **Comprehensive logging** - Detailed console output for each phase
- ✅ **Error handling** - Graceful failure with detailed error messages
- ✅ **Performance tracking** - Runtime monitoring and comparison
- ✅ **Modular design** - Each phase remains independent workflow

### What Gets Executed
```
Phase 0: Absence Loading (2 min)
  ↓
Phase 1: Smart Block Pairing (3 min)
  ↓
Phase 2: Resident Association (2 min)
  ↓
Phase 3: Faculty Assignment (2 min)
  ↓
Phase 4: Call Scheduling (2 min)
  ↓
Phase 5: ELIMINATED ⚠️
  ↓
Phase 6: Minimal Cleanup (5 sec)
  ↓
Phase 7: Validation & Reporting (2 min)
  ↓
Phase 8: Emergency Coverage (OPTIONAL - on-demand)
  ↓
Phase 9: Excel Export (2 min)

Total: ~15 minutes (71.7% faster than legacy 53 min)
```

---

## Architecture

### Workflow Structure

The orchestrator uses **Execute Workflow** nodes to call each phase as a subworkflow:

```
┌────────────────────────────────────────────────────────┐
│         MASTER ORCHESTRATOR WORKFLOW                   │
├────────────────────────────────────────────────────────┤
│                                                        │
│  [Manual Trigger]                                      │
│         ↓                                              │
│  [Initialize Orchestrator] ← Sets up execution config │
│         ↓                                              │
│  [Execute Phase 0] ← Calls phase0-absence-loader.json │
│         ↓                                              │
│  [Phase 0 Handler] ← Processes output, logs results   │
│         ↓                                              │
│  [Execute Phase 1] ← Calls phase1-smart-block-pairing  │
│         ↓                                              │
│  [Phase 1 Handler] ← Aggregates Phase 0 + 1 data      │
│         ↓                                              │
│  [Execute Phase 2] ← Calls phase2-resident-association │
│         ↓                                              │
│  ... (continues through all phases)                   │
│         ↓                                              │
│  [Final Completion Summary] ← Comprehensive results   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Node Types

1. **Execute Workflow Nodes** (9 total)
   - Execute each phase workflow
   - Wait for completion before proceeding
   - Pass data between phases

2. **Completion Handler Nodes** (9 total)
   - Process phase output
   - Aggregate data from upstream phases
   - Log results to console
   - Prepare input for next phase

3. **Special Nodes**
   - **Initialize Orchestrator**: Sets execution config and metadata
   - **Final Completion Summary**: Comprehensive execution report

---

## How It Works

### Data Flow Between Phases

Each completion handler aggregates data from all upstream phases:

```javascript
// Example: Phase 3 Completion Handler
const orchestrator = $('Phase 2 Completion Handler').first().json.orchestrator;
const phase0 = $('Phase 2 Completion Handler').first().json.phase0;
const phase1 = $('Phase 2 Completion Handler').first().json.phase1;
const phase2 = $('Phase 2 Completion Handler').first().json.phase2;
const phase3Result = $input.first().json;

return [{
  json: {
    orchestrator: orchestrator,  // Execution metadata
    phase0: phase0,              // Absence data
    phase1: phase1,              // Smart pairings
    phase2: phase2,              // Resident associations
    phase3: phase3Result,        // Faculty assignments (new)
    status: 'phase3_complete',
    nextPhase: 4
  }
}];
```

This ensures **all downstream phases have access to all upstream data**.

### Execution Flow

1. **User clicks "Execute Workflow"** on Master Orchestrator

2. **Initialize Orchestrator** sets up:
   - Unique execution ID
   - Start timestamp
   - Performance targets
   - Metadata

3. **For each phase:**
   - Execute Workflow node calls phase subworkflow
   - Waits for completion (synchronous)
   - Completion handler processes results
   - Aggregates with upstream data
   - Logs to console
   - Passes to next phase

4. **Final Completion Summary** generates:
   - Complete execution report
   - Performance metrics
   - ACGME compliance status
   - All phase results aggregated

---

## Setup Instructions

### Prerequisites

- ✅ n8n instance running (version 1.0+)
- ✅ Airtable account with credentials
- ✅ All 9 phase workflows imported
- ✅ Airtable credentials configured in n8n

### Step 1: Import All Workflows

Import these 10 JSON files into your n8n instance:

```
1. phase0-absence-loader.json
2. phase1-smart-block-pairing.json
3. phase2-smart-resident-association.json
4. phase3-enhanced-faculty-assignment.json
5. phase4-enhanced-call-scheduling.json
6. phase6-reinvented-minimal-cleanup.json
7. phase7-final-validation-reporting.json
8. phase8-emergency-coverage-engine.json
9. phase9-excel-export-engine.json
10. master-orchestrator.json ← THIS ONE
```

**How to import:**
1. Open n8n UI
2. Click "+ Add Workflow" or "New Workflow"
3. Click workflow name → "Import from File"
4. Select JSON file
5. Save workflow

**Repeat for all 10 files.**

### Step 2: Configure Airtable Credentials

Each phase workflow needs Airtable credentials:

1. Go to **Settings** → **Credentials** in n8n
2. Click **"+ Add Credential"**
3. Select **"Airtable Personal Access Token"**
4. Enter your Airtable API token
5. Save with name: **"Airtable Personal Access Token account 2"**
   (This matches the credential name in the workflows)

### Step 3: Update Execute Workflow Node References

**CRITICAL:** The Execute Workflow nodes need to reference the correct workflow IDs.

**Option A: Automatic (Recommended)**
1. Open `master-orchestrator.json` in n8n
2. Each "Execute Phase X" node should auto-detect available workflows
3. Click each Execute Workflow node
4. Select the corresponding phase workflow from dropdown:
   - "Execute Phase 0" → "Combined Medical Residency Scheduler - Phase 0"
   - "Execute Phase 1" → "Medical Residency Scheduler - Phase 1"
   - etc.

**Option B: Manual (If needed)**
1. Get workflow IDs:
   - Open each phase workflow
   - Note the workflow ID from URL: `/workflow/{WORKFLOW_ID}`
2. Edit each Execute Workflow node in orchestrator
3. Replace `workflowId` parameter with actual ID

### Step 4: Test Individual Phases

Before running orchestrator, test each phase individually:

```
✓ Phase 0: Should load absence data
✓ Phase 1: Should create block pairings
✓ Phase 2: Should assign residents
... etc.
```

### Step 5: Run the Orchestrator

1. Open **Master Orchestrator** workflow
2. Click **"Execute Workflow"** button
3. Monitor console output in Execution Log
4. Verify all phases complete successfully

---

## Usage Guide

### Running the Full Pipeline

**To execute all phases automatically:**

1. Open the **Master Orchestrator** workflow in n8n
2. Click the **"Execute Workflow"** button (top right)
3. Watch the execution progress in real-time
4. Monitor console logs for detailed output
5. Check final summary for results

**Expected execution time:** ~15 minutes

### Running Individual Phases

If you need to run a single phase:

1. Open the specific phase workflow (e.g., `phase0-absence-loader.json`)
2. Click "Execute Workflow"
3. Provide any required input data manually

**When to run individually:**
- Testing/debugging a specific phase
- Re-running failed phase
- Development/modification

### Viewing Results

**During Execution:**
- Click "Executions" in left sidebar
- Click running execution
- View real-time logs and output

**After Completion:**
- Check **Final Completion Summary** node output
- Contains all phase results aggregated
- Includes performance metrics and validation scores

---

## Monitoring & Logging

### Console Output

The orchestrator provides detailed console logging:

```
=== MASTER ORCHESTRATOR STARTING ===
Medical Residency Scheduler v2.0
Revolutionary 9-Phase Pipeline

Configuration:
  Execution ID: 2025-11-15T14:30:00.000Z
  Phases to execute: 0, 1, 2, 3, 4, 6, 7, 8, 9
  Phase 5 eliminated: true
  Target runtime: 15 minutes

=== PHASE 0 COMPLETE ===
Absences loaded: 15
Faculty absences: 10
Resident absences: 5

=== PHASE 1 COMPLETE ===
Smart pairings created: 120
Absence-aware: true

... (continues for all phases)

=== MASTER ORCHESTRATOR COMPLETE ===
================================================================================

EXECUTION SUMMARY:
  Execution ID: 2025-11-15T14:30:00.000Z
  Total runtime: 14 minutes
  Target runtime: 15 minutes
  Legacy runtime: 53 minutes
  Efficiency gain: 71.7%

PHASES EXECUTED:
  ✓ Phase 0: Absence Loading - 15 absences
  ✓ Phase 1: Smart Pairing - 120 pairings
  ✓ Phase 2: Resident Association - 100 assignments
  ✓ Phase 3: Faculty Assignment - 95 assignments
  ✓ Phase 4: Call Scheduling - 30 calls
  ✗ Phase 5: ELIMINATED (Revolutionary improvement!)
  ✓ Phase 6: Cleanup - 0 duplicates
  ✓ Phase 7: Validation - 98/100 score
  ⊙ Phase 8: Emergency Coverage - Skipped (on-demand only)
  ✓ Phase 9: Excel Export - 5 sheets

PERFORMANCE:
  Runtime: 14 min vs 53 min legacy
  Actual savings: 73.6%

ACGME COMPLIANCE:
  Validation score: 98/100
  Duty hours compliant: true
  Coverage gaps: 0

✅ ALL PHASES COMPLETE - SCHEDULING PIPELINE SUCCESS!
```

### Performance Metrics

Track these metrics across executions:

| Metric | Target | Typical | Alert If |
|--------|--------|---------|----------|
| Total Runtime | 15 min | 13-17 min | > 20 min |
| Phase 0 | 2 min | 1-3 min | > 5 min |
| Phase 6 | 5 sec | 3-10 sec | > 30 sec |
| Validation Score | 95+ | 95-100 | < 90 |
| Coverage Gaps | 0 | 0-2 | > 5 |

### Error Monitoring

**Common errors and resolutions:**

1. **"Workflow not found"**
   - Cause: Execute Workflow node references wrong workflow ID
   - Fix: Update workflow ID in Execute Workflow node settings

2. **"Airtable authentication failed"**
   - Cause: Invalid or expired Airtable credentials
   - Fix: Update Airtable credentials in n8n settings

3. **"Phase X timeout"**
   - Cause: Phase taking too long (>10 min)
   - Fix: Check Airtable data volume, network connectivity

4. **"Missing upstream data"**
   - Cause: Previous phase didn't output expected data structure
   - Fix: Check previous phase execution log, verify data structure

---

## Troubleshooting

### Issue: Orchestrator doesn't start

**Symptoms:** Clicking "Execute Workflow" does nothing

**Solutions:**
1. Check if workflow is saved (click Save button)
2. Verify Manual Trigger node is connected
3. Check browser console for errors
4. Try refreshing n8n UI

### Issue: Phase X fails during execution

**Symptoms:** Execution stops at specific phase with error

**Solutions:**
1. **View error details:**
   - Click failed node in execution view
   - Read error message
   - Check input/output data

2. **Test phase individually:**
   - Open failing phase workflow
   - Execute manually
   - Debug with test data

3. **Check Airtable data:**
   - Verify table IDs are correct
   - Check for missing records
   - Validate field names match schema

### Issue: Data not flowing between phases

**Symptoms:** Phase receives empty/null data from upstream

**Solutions:**
1. **Check completion handlers:**
   - Verify handler aggregates all upstream data
   - Check node references are correct (e.g., `$('Phase 0 Completion Handler')`)

2. **Verify Execute Workflow settings:**
   - Ensure "Wait for sub-workflow" is enabled
   - Check workflow ID is correct

3. **Test data structure:**
   - Run orchestrator up to failing phase
   - Examine output of previous completion handler
   - Verify expected data structure

### Issue: Performance degradation

**Symptoms:** Execution takes longer than expected (>20 min)

**Solutions:**
1. **Check Airtable rate limits:**
   - Airtable has 5 requests/sec limit
   - Add delays if hitting rate limits

2. **Optimize data volume:**
   - Filter unnecessary records in queries
   - Use pagination for large datasets

3. **Check network connectivity:**
   - Verify stable internet connection
   - Test Airtable API response times

4. **Review phase changes:**
   - Check if recent modifications added complexity
   - Profile slow operations

---

## Advanced Configuration

### Customizing Execution Order

To skip or reorder phases, modify the orchestrator workflow:

**Example: Skip Phase 9 (Excel Export)**

1. Open Master Orchestrator
2. Delete connection from "Phase 7 Handler" → "Execute Phase 9"
3. Connect "Phase 7 Handler" directly to "Final Completion Summary"
4. Update "Phase 7 Handler" code to remove phase9 references

**Example: Add conditional phase execution**

```javascript
// In Phase X Completion Handler
const shouldRunPhaseY = someCondition;

if (shouldRunPhaseY) {
  // Execute Phase Y
  return [{ json: data }];
} else {
  // Skip to Phase Z
  return [{ json: { ...data, phaseY: { skipped: true } } }];
}
```

### Adding Error Notifications

Add email/Slack notifications on failure:

1. Add new node after each Execute Workflow node
2. Use **IF** node to check for errors
3. Add **Send Email** or **Slack** node
4. Configure notification details

**Example IF condition:**
```javascript
{{ $json.error !== undefined }}
```

### Performance Optimization

**Enable parallel execution where possible:**

Currently phases run sequentially. Some phases could run in parallel:

- Phase 3 (Faculty) and Phase 4 (Call) could run parallel
- Phase 6 (Cleanup) could run parallel with Phase 7 (Validation)

**To implement:**
1. Use **Merge** node to combine parallel outputs
2. Ensure no data dependencies between parallel phases

### Custom Logging

Add custom logging to external system:

1. After each Completion Handler, add **HTTP Request** node
2. POST execution data to your logging service
3. Include execution ID, phase name, runtime, status

**Example payload:**
```json
{
  "executionId": "{{ $('Initialize Orchestrator').first().json.orchestrator.executionId }}",
  "phase": "Phase 3",
  "status": "complete",
  "runtime": "2 min",
  "timestamp": "{{ $now }}"
}
```

---

## Appendix: Node Reference

### Execute Workflow Nodes

| Node Name | Calls Workflow | Purpose |
|-----------|----------------|---------|
| Execute Phase 0 | phase0-absence-loader.json | Load absences |
| Execute Phase 1 | phase1-smart-block-pairing.json | Pair blocks |
| Execute Phase 2 | phase2-smart-resident-association.json | Assign residents |
| Execute Phase 3 | phase3-enhanced-faculty-assignment.json | Assign faculty |
| Execute Phase 4 | phase4-enhanced-call-scheduling.json | Schedule calls |
| Execute Phase 6 | phase6-reinvented-minimal-cleanup.json | Cleanup |
| Execute Phase 7 | phase7-final-validation-reporting.json | Validate |
| Execute Phase 9 | phase9-excel-export-engine.json | Export Excel |

### Completion Handler Nodes

| Node Name | Aggregates | Outputs |
|-----------|------------|---------|
| Phase 0 Handler | Phase 0 | orchestrator, phase0 |
| Phase 1 Handler | Phase 0-1 | orchestrator, phase0, phase1 |
| Phase 2 Handler | Phase 0-2 | orchestrator, phase0-2 |
| Phase 3 Handler | Phase 0-3 | orchestrator, phase0-3 |
| Phase 4 Handler | Phase 0-4 | orchestrator, phase0-4 |
| Phase 6 Handler | Phase 0-6 | orchestrator, phase0-6 |
| Phase 7 Handler | Phase 0-7 | orchestrator, phase0-7 |
| Final Summary | All phases | Complete execution report |

---

## Support & Contributions

### Getting Help

1. Check execution logs for error details
2. Review this documentation
3. Test individual phases
4. Check Airtable data and credentials

### Reporting Issues

When reporting issues, include:
- Execution ID
- Error messages
- Failed phase
- Input data structure
- n8n version

### Contributing Improvements

To modify the orchestrator:
1. Make changes in n8n UI
2. Export updated JSON
3. Test thoroughly
4. Document changes
5. Update this documentation

---

**Version:** 2.0.0  
**Last Updated:** 2025-11-15  
**Maintained By:** Medical Residency Scheduler Team
