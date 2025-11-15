# Pre-Testing Checklist for Expert Software Engineers
## Medical Residency Scheduler - n8n Workflows

**Version:** 1.0  
**Date:** 2025-11-15  
**Status:** Pre-Production Testing Phase

---

## 1. Code Quality & Security Audit

### JavaScript Code Review
- [ ] **Lint all JavaScript code** in workflow nodes
  - Check for syntax errors
  - Validate variable naming conventions
  - Check for unused variables
  - Verify no hardcoded values that should be configurable

- [ ] **Security scan**
  - [ ] No hardcoded credentials (✓ using n8n credential system)
  - [ ] No API keys in code
  - [ ] No PII logging to console
  - [ ] Input validation on all external data
  - [ ] SQL injection prevention (N/A - using Airtable API)
  - [ ] XSS prevention in data handling

- [ ] **Error handling review**
  - [ ] Try-catch blocks where needed
  - [ ] Graceful degradation on failures
  - [ ] Meaningful error messages
  - [ ] No sensitive data in error logs

### Code Pattern Validation
- [ ] **Consistency checks**
  - [ ] All phase outputs follow same data structure
  - [ ] Handler aggregation pattern consistent across all phases
  - [ ] Naming conventions consistent
  - [ ] Similar operations use similar code patterns

---

## 2. Environment Setup & Isolation

### Test Environment Configuration
- [ ] **Create separate Airtable base for testing**
  - [ ] Clone production schema
  - [ ] Populate with sanitized test data
  - [ ] No production data in test environment
  - [ ] Document test data scenarios

- [ ] **n8n environment setup**
  - [ ] Development instance separate from production
  - [ ] Test credentials different from production
  - [ ] Workflow versioning strategy defined
  - [ ] Execution history retention configured

- [ ] **Environment variables documented**
  - [ ] List all required credentials
  - [ ] Document Airtable base IDs
  - [ ] Document table IDs
  - [ ] API rate limits noted

### Data Isolation Strategy
- [ ] **Test data preparation**
  ```
  Test Scenarios:
  - Minimal dataset (1-2 residents, 1 faculty)
  - Typical dataset (~10 residents, 5 faculty)
  - Large dataset (50+ residents, 20+ faculty)
  - Edge cases (no absences, all absences, etc.)
  ```

- [ ] **Backup procedures**
  - [ ] Test Airtable base backup created
  - [ ] Workflow JSON files backed up
  - [ ] Restoration procedure documented
  - [ ] Rollback criteria defined

---

## 3. Dependency & Compatibility Verification

### Version Compatibility Matrix
- [ ] **n8n version requirements**
  ```
  Minimum: n8n v1.0.0
  Tested: n8n v1.119.2
  Execute Workflow node: v1.0+
  Code node: v2.0
  ```

- [ ] **Airtable API compatibility**
  - [ ] API version: v0 (current)
  - [ ] Personal Access Token auth supported
  - [ ] Rate limits: 5 req/sec documented
  - [ ] Table/field ID format validated

- [ ] **External dependencies**
  - [ ] Node.js version (for n8n self-hosted)
  - [ ] Browser compatibility (for n8n Cloud)
  - [ ] Network requirements (HTTPS to api.airtable.com)

### Table ID Validation
- [ ] **Verify all table IDs exist in your Airtable**
  ```bash
  # Run this check:
  grep -r "tbl[A-Za-z0-9]\{13,17\}" phase*.json | sort -u
  
  # Compare against your Airtable base
  Required tables:
  - tbl3TfpZSGYGxlCIG (Residency Block Schedule)
  - tblfqvE6iLYwRvJkM (Resident Details)
  - tbl2h0TDwPRMV5a1s (Faculty Schedules)
  - tbl1dDmLfKdf7P4l0 (Rotation Catalog)
  - tbl15U9cF0uig9IEo (Attending Call Shifts)
  - tbl17gcDUtXc14Rjv (Master Assignments)
  - tbloGnXnu0mC6y83L (Faculty Master Assignments)
  - tblTP62YOkF75o5aO (Half-Day Blocks)
  - tblLUzjfad4B1GQ1a (Rotation Templates)
  - tblmgzodmqTsJ5inf (Faculty Data)
  ```

---

## 4. Test Plan Development

### Unit Test Scenarios (Per Phase)
- [ ] **Phase 0: Absence Loading**
  ```
  Test cases:
  1. No absences in system
  2. Only faculty absences
  3. Only resident absences
  4. Mix of both
  5. Overlapping absences
  6. Future absences
  7. Past absences (should be filtered)
  ```

- [ ] **Phase 1: Smart Block Pairing**
  ```
  Test cases:
  1. All blocks have matching rotations
  2. Some blocks have no rotations
  3. Multiple rotations per block
  4. Absence-aware pairing active
  ```

- [ ] **Phase 2: Resident Association**
  ```
  Test cases:
  1. More residents than blocks
  2. More blocks than residents
  3. Exact match
  4. Residents on leave during block
  ```

- [ ] **Phase 3: Faculty Assignment**
  ```
  Test cases:
  1. Sufficient faculty available
  2. Faculty shortage
  3. Faculty on leave during assignment
  4. ACGME ratio violations
  5. Specialty requirements not met
  ```

- [ ] **Phase 4: Call Scheduling**
  ```
  Test cases:
  1. Equal distribution possible
  2. Unequal workload required
  3. Weekend coverage
  4. Holiday coverage
  ```

- [ ] **Phase 6: Cleanup**
  ```
  Test cases:
  1. No duplicates (clean run)
  2. Intentional duplicates
  3. Orphaned records
  4. Conflicting assignments
  ```

- [ ] **Phase 7: Validation**
  ```
  Test cases:
  1. Perfect schedule (100 score)
  2. Minor violations (90-95 score)
  3. Major violations (< 90 score)
  4. Coverage gaps present
  ```

- [ ] **Phase 9: Excel Export**
  ```
  Test cases:
  1. Multiple blocks
  2. Single block
  3. All fields populated
  4. Some fields empty
  ```

### Integration Test Scenarios
- [ ] **Full pipeline tests**
  ```
  Scenario 1: Happy path
  - Clean data, no absences
  - All phases succeed
  - Expected runtime: 13-17 min
  - Validation score: 95-100
  
  Scenario 2: Absence handling
  - Multiple faculty/resident absences
  - Substitutions applied
  - Phase 5 NOT needed
  - Validation score: 90-95
  
  Scenario 3: Edge cases
  - Maximum data volume
  - All residents on PGY-1 (high supervision needs)
  - Limited faculty availability
  - Validation score: 85-95
  
  Scenario 4: Error conditions
  - Missing Airtable tables
  - Invalid credentials
  - Network timeout
  - Graceful failure expected
  ```

### Performance Test Criteria
- [ ] **Runtime benchmarks**
  ```
  Phase 0: < 5 min
  Phase 1: < 5 min
  Phase 2: < 5 min
  Phase 3: < 5 min
  Phase 4: < 5 min
  Phase 6: < 1 min
  Phase 7: < 5 min
  Phase 9: < 5 min
  Total: < 20 min
  
  Alert if any phase > 10 min
  Alert if total > 25 min
  ```

- [ ] **Resource monitoring**
  - Memory usage (n8n instance)
  - API call count (Airtable rate limits)
  - Network bandwidth
  - Execution queue depth

---

## 5. Monitoring & Observability Setup

### Logging Strategy
- [ ] **Console logging levels**
  ```javascript
  DEBUG: Detailed execution steps
  INFO: Phase completion, counts
  WARN: Minor issues, fallbacks used
  ERROR: Failures, exceptions
  ```

- [ ] **Log aggregation**
  - [ ] Centralized logging if available
  - [ ] Log retention policy defined
  - [ ] Log search strategy documented

### Metrics to Track
- [ ] **Execution metrics**
  ```
  - Total executions per day/week
  - Success rate (%)
  - Average runtime
  - P50, P95, P99 runtime percentiles
  - Error rate by phase
  - Retry count
  ```

- [ ] **Business metrics**
  ```
  - Absences processed
  - Assignments created
  - ACGME compliance score
  - Coverage gaps count
  - Manual overrides needed (should be 0)
  ```

### Alerting Thresholds
- [ ] **Define alert conditions**
  ```
  CRITICAL:
  - Execution failure
  - ACGME score < 85
  - Coverage gaps > 5
  - Phase timeout (> 15 min)
  
  WARNING:
  - ACGME score < 95
  - Coverage gaps 1-5
  - Phase slow (> 7 min)
  - Airtable rate limit hit
  
  INFO:
  - Execution complete
  - New absence substitutions
  ```

---

## 6. Documentation & Runbook Completion

### Operational Documentation
- [ ] **Runbook created** (see below)
- [ ] **Incident response procedures**
  - [ ] Who to contact for issues
  - [ ] Escalation path
  - [ ] Common issues and fixes
- [ ] **Change management process**
  - [ ] How to update workflows
  - [ ] Testing requirements
  - [ ] Approval workflow

### API Documentation
- [ ] **Airtable schema documented**
  - [ ] All tables with field descriptions
  - [ ] Required vs optional fields
  - [ ] Data types and validations
  - [ ] Relationships between tables

- [ ] **Workflow interfaces documented**
  - [ ] Each phase input requirements
  - [ ] Each phase output structure
  - [ ] Data contracts between phases

### Training Materials
- [ ] **User guides**
  - [ ] How to trigger execution
  - [ ] How to interpret Excel output
  - [ ] What to do if schedule looks wrong

- [ ] **Admin guides**
  - [ ] How to import/update workflows
  - [ ] How to configure credentials
  - [ ] How to monitor execution

---

## 7. Disaster Recovery & Rollback Planning

### Backup Procedures
- [ ] **Pre-deployment backup checklist**
  ```
  1. Export all current workflows
  2. Backup Airtable data
  3. Document current n8n version
  4. Screenshot current credential setup
  5. Export execution history
  ```

- [ ] **Backup storage**
  - [ ] Workflows backed up to git (✓)
  - [ ] Airtable backup location defined
  - [ ] Backup retention policy (30 days)
  - [ ] Backup restoration tested

### Rollback Criteria
- [ ] **When to rollback**
  ```
  IMMEDIATE ROLLBACK:
  - Data corruption in Airtable
  - ACGME violations in > 20% of executions
  - Consistent execution failures (> 50%)
  - Security breach detected
  
  SCHEDULED ROLLBACK:
  - Performance degradation (> 30 min runtime)
  - Validation score < 90 consistently
  - User complaints about Excel format
  ```

- [ ] **Rollback procedure**
  ```
  1. Stop orchestrator executions
  2. Disable workflow triggers
  3. Restore previous workflow versions
  4. Verify Airtable data integrity
  5. Test legacy system
  6. Communicate to stakeholders
  7. Post-mortem analysis
  ```

---

## 8. Static Analysis & Validation Tools

### Automated Checks
- [ ] **JSON validation script**
  ```bash
  # Validate all workflow JSONs
  for file in phase*.json master-orchestrator.json; do
    echo "Validating $file..."
    jq empty "$file" || echo "ERROR: Invalid JSON in $file"
  done
  ```

- [ ] **Table ID validation script**
  ```bash
  # Check all table IDs are in schema
  grep -r "\"tbl[A-Za-z0-9]\+\"" *.json | \
    grep -o "tbl[A-Za-z0-9]\+" | \
    sort -u > used_table_ids.txt
  
  # Compare with schema
  jq -r '.tables[].id' docs/airtable_schema.json | \
    sort > schema_table_ids.txt
  
  # Find mismatches
  comm -23 used_table_ids.txt schema_table_ids.txt > missing_tables.txt
  ```

- [ ] **Credential reference check**
  ```bash
  # Ensure all workflows use same credential name
  grep -r "credentialType.*airtable" *.json | \
    grep -o '"name": "[^"]*"' | \
    sort -u
  # Should only show: "Airtable Personal Access Token account 2"
  ```

### Code Quality Checks
- [ ] **JavaScript linting** (if ESLint available)
  ```bash
  # Extract JS code from workflows and lint
  # (Would need custom script to extract from JSON)
  ```

- [ ] **Duplicate code detection**
  - [ ] Check for repeated logic across phases
  - [ ] Consider refactoring into reusable functions
  - [ ] Document intentional duplication

---

## 9. Security & Compliance

### Security Audit
- [ ] **Credential management**
  - [ ] All credentials use n8n credential system
  - [ ] No plaintext passwords in code
  - [ ] Credential rotation policy defined
  - [ ] Access control on credentials

- [ ] **Data handling**
  - [ ] PII identified (resident names, faculty names)
  - [ ] PII not logged unnecessarily
  - [ ] HIPAA compliance reviewed (if applicable)
  - [ ] Data retention policy defined

- [ ] **Network security**
  - [ ] All API calls use HTTPS
  - [ ] Certificate validation enabled
  - [ ] No hardcoded IPs/hostnames
  - [ ] Firewall rules documented

### Compliance Checks
- [ ] **ACGME compliance verification**
  - [ ] Duty hour calculations accurate
  - [ ] Supervision ratios enforced
  - [ ] PGY level restrictions applied
  - [ ] Specialty requirements met

- [ ] **Audit trail**
  - [ ] All executions logged
  - [ ] Changes trackable
  - [ ] Ability to reproduce schedules
  - [ ] Execution history retention

---

## 10. Performance & Load Testing

### Baseline Performance
- [ ] **Establish baseline metrics**
  ```
  Run orchestrator 5 times with typical data:
  - Record min, max, average runtime per phase
  - Note memory usage
  - Count API calls
  - Measure data volume
  ```

### Load Testing Scenarios
- [ ] **Test with production-scale data**
  ```
  Scenario 1: Small program
  - 10 residents
  - 5 faculty
  - 5 blocks
  Expected: < 10 min
  
  Scenario 2: Medium program
  - 30 residents
  - 15 faculty
  - 13 blocks
  Expected: < 15 min
  
  Scenario 3: Large program
  - 100 residents
  - 40 faculty
  - 13 blocks
  Expected: < 25 min
  ```

- [ ] **Concurrent execution test**
  - [ ] What happens if triggered multiple times?
  - [ ] Queue handling strategy
  - [ ] Resource contention

### API Rate Limit Testing
- [ ] **Airtable rate limit handling**
  ```
  - Document current approach (wait nodes)
  - Test with rate limit errors
  - Verify retry logic
  - Measure API call efficiency
  ```

---

## 11. User Acceptance Criteria

### Functional Requirements
- [ ] **Core functionality**
  - [ ] All phases execute without errors
  - [ ] Data flows correctly between phases
  - [ ] Excel output matches expected format
  - [ ] ACGME compliance maintained

- [ ] **Revolutionary improvements verified**
  - [ ] Phase 5 not needed (absence-aware from start)
  - [ ] Runtime < 20 min
  - [ ] No manual overrides required
  - [ ] Excel format unchanged (backward compatible)

### Non-Functional Requirements
- [ ] **Usability**
  - [ ] One-button execution works
  - [ ] Logs are readable
  - [ ] Errors are clear
  - [ ] Excel output is intuitive

- [ ] **Reliability**
  - [ ] Success rate > 95%
  - [ ] Graceful failure on errors
  - [ ] Data integrity maintained
  - [ ] Consistent results

- [ ] **Maintainability**
  - [ ] Code is documented
  - [ ] Workflows are self-explanatory
  - [ ] Updates can be made easily
  - [ ] Test suite exists

---

## 12. Pre-Testing Verification Commands

### Quick Validation Commands
```bash
# 1. Validate all JSON files
echo "=== JSON Validation ==="
for file in phase*.json master-orchestrator.json; do
  if jq empty "$file" 2>/dev/null; then
    echo "✓ $file"
  else
    echo "✗ $file - INVALID JSON"
  fi
done

# 2. Check file sizes (detect corruption)
echo -e "\n=== File Size Check ==="
ls -lh phase*.json master-orchestrator.json | awk '{print $9, $5}'

# 3. Count nodes in each workflow
echo -e "\n=== Node Count ==="
for file in phase*.json master-orchestrator.json; do
  count=$(jq '.nodes | length' "$file")
  echo "$file: $count nodes"
done

# 4. Extract all table IDs used
echo -e "\n=== Table IDs Used ==="
grep -rh "\"tbl[A-Za-z0-9]\{13,17\}\"" *.json | \
  grep -o "tbl[A-Za-z0-9]*" | \
  sort -u

# 5. Check credential names
echo -e "\n=== Credential Names ==="
grep -rh '"name".*Airtable' *.json | \
  grep -o '"name": "[^"]*"' | \
  sort -u

# 6. Verify no hardcoded secrets
echo -e "\n=== Secret Scan ==="
if grep -r "sk-\|token.*:" *.json | grep -v "credentialType"; then
  echo "⚠️  Possible hardcoded secrets found!"
else
  echo "✓ No hardcoded secrets detected"
fi
```

---

## Summary Checklist

### Critical Pre-Testing Items
- [ ] All JSON files validated ✓
- [ ] Table IDs verified against Airtable base
- [ ] Test environment isolated from production
- [ ] Test data prepared (3 scenarios minimum)
- [ ] Backup procedures documented and tested
- [ ] Rollback criteria defined
- [ ] Monitoring/alerting configured
- [ ] Test plan documented
- [ ] Security audit complete
- [ ] Performance baseline established

### Nice-to-Have Pre-Testing Items
- [ ] Automated test suite created
- [ ] Load testing completed
- [ ] User training materials ready
- [ ] Runbook finalized
- [ ] Code linting passed
- [ ] Duplicate code refactored

### Ready to Test When:
```
✅ Critical items: 100% complete
✅ Nice-to-have items: 70%+ complete
✅ Stakeholder approval obtained
✅ Test window scheduled
✅ Rollback plan approved
```

---

**Checklist Version:** 1.0  
**Last Updated:** 2025-11-15  
**Next Review:** Before first production deployment
