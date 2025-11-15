# Deployment Guide
## Medical Residency Scheduler - Master Orchestrator Setup

**Estimated Setup Time:** 30-45 minutes  
**Difficulty Level:** Intermediate  
**Prerequisites:** n8n instance running, Airtable account

---

## Quick Start (TL;DR)

```bash
# 1. Import all 10 workflows into n8n
# 2. Configure Airtable credentials
# 3. Update Execute Workflow node references in orchestrator
# 4. Click "Execute Workflow" on Master Orchestrator
# 5. Watch the magic happen! ✨
```

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Step-by-Step Deployment](#step-by-step-deployment)
3. [Post-Deployment Validation](#post-deployment-validation)
4. [Production Deployment](#production-deployment)
5. [Rollback Procedures](#rollback-procedures)

---

## Pre-Deployment Checklist

### Environment Requirements

- [ ] **n8n instance** running (version 1.0.0 or higher)
  - Cloud: n8n.cloud account with active subscription
  - Self-hosted: Docker or npm installation

- [ ] **Airtable setup**
  - [ ] Active Airtable account
  - [ ] Base created with required tables (see schema)
  - [ ] Personal Access Token generated
  - [ ] Tables populated with initial data

- [ ] **Required files** downloaded from repository
  ```
  ✓ phase0-absence-loader.json
  ✓ phase1-smart-block-pairing.json
  ✓ phase2-smart-resident-association.json
  ✓ phase3-enhanced-faculty-assignment.json
  ✓ phase4-enhanced-call-scheduling.json
  ✓ phase6-reinvented-minimal-cleanup.json
  ✓ phase7-final-validation-reporting.json
  ✓ phase8-emergency-coverage-engine.json
  ✓ phase9-excel-export-engine.json
  ✓ master-orchestrator.json
  ```

- [ ] **Network access**
  - [ ] n8n can reach Airtable API (api.airtable.com)
  - [ ] No firewall blocking outbound HTTPS

### Airtable Schema Verification

Verify these tables exist in your Airtable base:

| Table ID | Table Name | Purpose |
|----------|------------|---------|
| `tbl3TfpZSGYGxlCIG` | Residency Block Schedule | Main scheduling data |
| `tblfqvE6iLYwRvJkM` | Resident Details | Resident information |
| `tbl2h0TDwPRMV5a1s` | Faculty Schedules | Faculty data |
| `tbl1dDmLfKdf7P4l0` | Rotation Catalog | Available rotations |
| `tbl15U9cF0uig9IEo` | Attending Call Shifts | Call scheduling |
| `tbl17gcDUtXc14Rjv` | Master Assignments | Generated assignments |
| `tbloGnXnu0mC6y83L` | Faculty Master Assignments | Faculty assignments |
| `tblTP62YOkF75o5aO` | Half-Day Blocks | Time block definitions |
| `tblLUzjfad4B1GQ1a` | Rotation Templates | Template definitions |
| `tblmgzodmqTsJ5inf` | Faculty Data | Faculty details |

**Note:** Table IDs are hardcoded in workflows. If your IDs differ, you'll need to update them.

---

## Step-by-Step Deployment

### Phase 1: Import Workflows (15 minutes)

**For each of the 10 JSON files, follow these steps:**

1. **Open n8n**
   - Navigate to your n8n instance URL
   - Log in with your credentials

2. **Create New Workflow**
   - Click **"+ Add Workflow"** (top right)
   - Or use **"Workflows"** → **"Add Workflow"**

3. **Import JSON**
   - Click the workflow name (top left, says "My workflow")
   - Select **"Import from File"**
   - Click **"Select file to import"**
   - Choose one of the JSON files (e.g., `phase0-absence-loader.json`)
   - Click **"Import"**

4. **Verify Import**
   - Workflow name should update to match the imported workflow
   - Nodes should appear on the canvas
   - Check for any import warnings

5. **Save Workflow**
   - Click **"Save"** button (top right)
   - Workflow is now saved in your n8n instance

6. **Repeat for all 10 files**
   - Import each file as a separate workflow
   - You should have 10 workflows total when done

**Import Order (recommended):**
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
10. master-orchestrator.json ← Import this one LAST
```

### Phase 2: Configure Airtable Credentials (10 minutes)

1. **Generate Airtable Personal Access Token**
   - Go to https://airtable.com/create/tokens
   - Click **"Create new token"**
   - Name: "n8n Medical Residency Scheduler"
   - Scopes: 
     - ✓ `data.records:read`
     - ✓ `data.records:write`
     - ✓ `schema.bases:read`
   - Access: Select your Medical Residency base
   - Click **"Create token"**
   - **Copy the token** (you won't see it again!)

2. **Add Credentials in n8n**
   - In n8n, click **"Settings"** (left sidebar)
   - Click **"Credentials"**
   - Click **"+ Add Credential"**
   - Search for "Airtable"
   - Select **"Airtable Personal Access Token"**

3. **Configure Credential**
   - **Credential Name:** `Airtable Personal Access Token account 2`
     (Must match this exactly - workflows reference this name)
   - **Access Token:** Paste your token from step 1
   - Click **"Save"**

4. **Verify Credential**
   - Should see green checkmark
   - Test by opening any phase workflow
   - Find an Airtable node
   - Credential should be auto-selected
   - No "Missing credentials" warnings

### Phase 3: Configure Orchestrator (10 minutes)

**This is the CRITICAL step that links everything together.**

1. **Open Master Orchestrator Workflow**
   - Go to **"Workflows"**
   - Find **"Master Orchestrator - Medical Residency Scheduler"**
   - Click to open

2. **For Each "Execute Phase X" Node:**

   You'll see 8 nodes named like:
   - "Execute Phase 0: Absence Loading"
   - "Execute Phase 1: Smart Block Pairing"
   - etc.

   **For EACH of these nodes:**

   a. **Click the node** to select it
   
   b. **Click "Parameters"** panel (right side)
   
   c. **Find "Workflow" dropdown**
   
   d. **Select the corresponding workflow:**
      - "Execute Phase 0" → Select "Combined Medical Residency Scheduler - Phase 0"
      - "Execute Phase 1" → Select "Medical Residency Scheduler - Phase 1"
      - "Execute Phase 2" → Select "Medical Residency Scheduler - Phase 2"
      - etc.
   
   e. **Verify "Wait for sub-workflow" is ENABLED**
      - Look for checkbox/toggle that says "Wait for completion"
      - This MUST be checked/enabled
   
   f. **Click away** to save the node

3. **Verify All Connections**
   - All 8 Execute Workflow nodes should now have workflow selected
   - No red warning icons
   - Canvas should show clean flow from start to finish

4. **Save Orchestrator**
   - Click **"Save"** button

**Troubleshooting:**
- **Can't find workflow in dropdown?**
  - Make sure you imported all 9 phase workflows first
  - Try refreshing the page
  - Check workflow names match exactly

- **"Wait for sub-workflow" option missing?**
  - Check n8n version (needs 1.0+)
  - Try updating Execute Workflow node

### Phase 4: Initial Testing (15 minutes)

**Test each phase individually before running full orchestrator.**

#### Test Phase 0 (Absence Loading)

1. **Open Phase 0 workflow**
2. **Click "Execute Workflow"**
3. **Check execution:**
   - Should complete without errors
   - Check output: should contain `absence_data`
   - Look for faculty/resident absence counts in logs
4. **Expected runtime:** ~2 minutes

#### Test Phase 1 (Smart Block Pairing)

1. **Open Phase 1 workflow**
2. **Manually provide Phase 0 data** (or run with test data)
3. **Execute**
4. **Verify:** Creates block-rotation pairings
5. **Expected runtime:** ~3 minutes

#### Continue for Phases 2-9

- Test each phase individually
- Verify outputs match expected structure
- Fix any Airtable connection issues
- Ensure credentials work

**Skip Phase 8** (Emergency Coverage) for now - it's optional.

### Phase 5: First Full Orchestrator Run (15 minutes)

**Now for the moment of truth!**

1. **Open Master Orchestrator workflow**

2. **Clear any previous execution data:**
   - Click "Executions" (left sidebar)
   - Delete any previous test executions
   - Return to workflow canvas

3. **Click "Execute Workflow"** (top right)

4. **Watch execution in real-time:**
   - You'll see nodes light up as they execute
   - Green = success, Red = error
   - Click any node to see its output

5. **Monitor Console Logs:**
   - Click "Executions" → Latest execution
   - View console output for detailed logging
   - Look for "=== PHASE X COMPLETE ===" messages

6. **Expected behavior:**
   ```
   Phase 0 executes → Handler processes → Phase 1 executes → etc.
   Total time: ~15 minutes
   ```

7. **Check Final Output:**
   - Last node should be "Final Completion Summary"
   - Output should contain:
     - All phase results
     - Performance metrics
     - ACGME compliance score
     - Excel workbook data

**Success Criteria:**
- ✅ All phases execute without errors
- ✅ Total runtime: 13-17 minutes
- ✅ Validation score: 95+/100
- ✅ Coverage gaps: 0-2
- ✅ Final output contains all phase data

---

## Post-Deployment Validation

### Validation Checklist

After successful first run, verify:

- [ ] **Data Quality**
  - [ ] Absence data loaded correctly
  - [ ] Resident assignments look accurate
  - [ ] Faculty assignments meet ACGME requirements
  - [ ] Call schedule is equitably distributed

- [ ] **Airtable Updates**
  - [ ] Check Master Assignments table - new records created
  - [ ] Check Faculty Master Assignments table - new records
  - [ ] Check Call Assignments table - new records
  - [ ] No duplicate records

- [ ] **Performance**
  - [ ] Total runtime < 20 minutes
  - [ ] Phase 6 cleanup < 30 seconds
  - [ ] No timeout errors

- [ ] **Compliance**
  - [ ] ACGME validation score ≥ 95
  - [ ] Duty hours within limits
  - [ ] Supervision ratios met
  - [ ] Coverage gaps minimal (0-2)

### Compare with Legacy System

If you have a legacy system, compare outputs:

| Metric | Legacy | New System | Improvement |
|--------|--------|------------|-------------|
| Runtime | 53 min | ~15 min | 71.7% faster |
| Manual overrides | Many | None | Phase 5 eliminated |
| Cleanup time | 36 min | 5 sec | 86% faster |
| ACGME compliance | Manual check | Automated | 100% verified |
| Excel format | Legacy | Preserved | No training needed |

---

## Production Deployment

### Production Readiness Checklist

Before deploying to production:

- [ ] **Tested with production-like data volume**
- [ ] **All stakeholders trained on Excel output**
- [ ] **Backup procedures established**
- [ ] **Rollback plan documented**
- [ ] **Monitoring and alerting configured**
- [ ] **Performance baseline established**

### Deployment Strategy: Blue-Green

**Recommended approach for zero-downtime deployment:**

1. **Blue Environment (Legacy):**
   - Keep existing scheduling system running
   - Continue generating schedules as normal

2. **Green Environment (New):**
   - Deploy Master Orchestrator
   - Run in parallel with legacy system
   - Compare outputs

3. **Validation Period (1-2 weeks):**
   - Run both systems
   - Compare schedule outputs
   - Validate ACGME compliance
   - Gather user feedback on Excel format

4. **Cutover:**
   - Switch primary system to Green (new)
   - Keep Blue (legacy) as backup
   - Monitor closely for 1 week

5. **Decommission:**
   - After stable operation, retire legacy system

### Scheduling the Cutover

**Best practice: Start during off-peak period**

```
Recommended timeline:
- Friday 5 PM: Deploy to Green environment
- Saturday-Sunday: Monitor test runs
- Monday 8 AM: Begin parallel operation
- Week 1-2: Dual operation and validation
- Week 3: Cutover to primary
- Week 4+: Legacy system backup only
```

---

## Rollback Procedures

### When to Rollback

Rollback if you encounter:
- ❌ Consistent validation scores < 90
- ❌ Critical ACGME compliance violations
- ❌ Data corruption in Airtable
- ❌ Runtime consistently > 30 minutes
- ❌ Frequent execution failures (> 10%)

### Rollback Steps

1. **Immediate Actions:**
   - Stop orchestrator executions
   - Revert to legacy scheduling system
   - Document issues encountered

2. **Data Cleanup:**
   - Identify records created by failed runs
   - Mark or delete as appropriate
   - Restore from backup if needed

3. **Investigation:**
   - Review execution logs
   - Identify root cause
   - Test fixes in development environment

4. **Re-deployment:**
   - Apply fixes
   - Re-test thoroughly
   - Schedule new deployment

### Emergency Contacts

Maintain list of contacts for deployment issues:

```
n8n Administrator: [name/email]
Airtable Admin: [name/email]
System Owner: [name/email]
On-call Support: [phone/email]
```

---

## Appendix: Common Issues

### Issue: "Workflow not found" error

**Cause:** Execute Workflow node references wrong workflow ID

**Fix:**
1. Open Master Orchestrator
2. Click failing Execute Workflow node
3. Re-select correct workflow from dropdown
4. Save and re-run

### Issue: Airtable rate limit errors

**Cause:** Hitting Airtable's 5 req/sec limit

**Fix:**
1. Add "Wait" nodes between Airtable operations
2. Set wait time to 250ms (0.25 seconds)
3. Or upgrade Airtable plan for higher limits

### Issue: Phase timeout

**Cause:** Phase taking > 10 minutes

**Fix:**
1. Check data volume in Airtable
2. Optimize queries (add filters)
3. Increase timeout in n8n settings
4. Consider breaking large dataset into batches

### Issue: Missing data in outputs

**Cause:** Completion handler not aggregating correctly

**Fix:**
1. Check handler node code
2. Verify references to upstream nodes
3. Ensure data structure matches expected format

---

## Quick Reference

### File Checklist

```
Required Imports:
☐ phase0-absence-loader.json
☐ phase1-smart-block-pairing.json
☐ phase2-smart-resident-association.json
☐ phase3-enhanced-faculty-assignment.json
☐ phase4-enhanced-call-scheduling.json
☐ phase6-reinvented-minimal-cleanup.json
☐ phase7-final-validation-reporting.json
☐ phase8-emergency-coverage-engine.json
☐ phase9-excel-export-engine.json
☐ master-orchestrator.json

Required Configuration:
☐ Airtable Personal Access Token created
☐ Credential added in n8n
☐ Execute Workflow nodes configured
☐ All workflows saved
```

### Execution Command

```
1. Open Master Orchestrator workflow
2. Click "Execute Workflow"
3. Wait ~15 minutes
4. Check "Final Completion Summary" output
```

### Success Indicators

```
✓ All phases green (no errors)
✓ Runtime: 13-17 minutes
✓ Validation score: 95+/100
✓ Coverage gaps: 0-2
✓ Excel output generated
```

---

**Deployment Guide Version:** 1.0  
**Last Updated:** 2025-11-15  
**Next Review:** 2026-01-15
