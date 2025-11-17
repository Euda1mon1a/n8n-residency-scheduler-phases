#!/usr/bin/env python3
"""
Phase 3 Edge Case Testing
Tests boundary conditions, error handling, and special scenarios
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List
import sys

# Import the test module to reuse classes
sys.path.insert(0, '/home/user/n8n-residency-scheduler-phases')
from test_phase3_mock import (
    FacultyAbsenceProcessor, ACGMEComplianceEngine,
    ACGME_RATIOS, SPECIALTY_REQUIREMENTS
)

def test_all_faculty_absent():
    """Test scenario where all faculty are absent"""
    print("\n" + "="*60)
    print("TEST 1: All Faculty Absent Scenario")
    print("="*60)

    today = datetime.now()

    faculty_data = [
        {'id': 'rec_f1', 'Faculty': 'Faculty1', 'Last Name': 'F1',
         'Performs Procedure': True, 'Faculty Status': 'Active'}
    ]

    faculty_leave = [
        {
            'Faculty': ['rec_f1'],
            'Leave Start': today.isoformat(),
            'Leave End': (today + timedelta(days=10)).isoformat(),
            'Leave Type': 'TDY',
            'Comments': 'Away',
            'Leave Approved Residency': True,
            'Leave Approved Army': True
        }
    ]

    master_assignments = [
        {
            'id': 'rec_ma_001',
            'Half-Day of the Week of Blocks': ['rec_hd_001'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            'PGY Link (from Residency Block Schedule)': ['PGY-1']
        }
    ]

    processor = FacultyAbsenceProcessor()
    absence_calendar = processor.process_leave_records(faculty_leave)

    engine = ACGMEComplianceEngine(faculty_data, absence_calendar, ACGME_RATIOS, SPECIALTY_REQUIREMENTS)
    result = engine.process_all_assignments(master_assignments)

    # Validate
    has_coverage_gap = result['statistics']['coverage_gaps'] > 0
    print(f"✓ Coverage gaps detected: {has_coverage_gap}")
    print(f"  Gap reason: {result['coverage_gaps'][0]['reason'] if result['coverage_gaps'] else 'N/A'}")

    return has_coverage_gap

def test_specialty_requirement_enforcement():
    """Test that specialty requirements are strictly enforced"""
    print("\n" + "="*60)
    print("TEST 2: Specialty Requirement Enforcement")
    print("="*60)

    faculty_data = [
        {'id': 'rec4F7XQKFyDjXn5n', 'Faculty': 'Tagawa', 'Last Name': 'Tagawa',
         'Performs Procedure': True, 'Specialties': ['Sports Medicine'], 'Faculty Status': 'Active'},
        {'id': 'rec_other', 'Faculty': 'OtherDoc', 'Last Name': 'Other',
         'Performs Procedure': True, 'Specialties': ['General'], 'Faculty Status': 'Active'}
    ]

    master_assignments = [
        {
            'id': 'rec_ma_sports',
            'Half-Day of the Week of Blocks': ['rec_hd_sports'],
            'Activity (from Rotation Templates)': ['Sports Medicine'],
            'PGY Link (from Residency Block Schedule)': ['PGY-2']
        }
    ]

    engine = ACGMEComplianceEngine(faculty_data, {}, ACGME_RATIOS, SPECIALTY_REQUIREMENTS)
    result = engine.process_all_assignments(master_assignments)

    # Validate - should only assign Dr. Tagawa
    if result['assignments']:
        assigned_faculty = result['assignments'][0]['faculty_id']
        correct_faculty = assigned_faculty == 'rec4F7XQKFyDjXn5n'
        print(f"✓ Correct faculty assigned (Dr. Tagawa): {correct_faculty}")
        print(f"  Assigned: {result['assignments'][0]['faculty_name']}")
        return correct_faculty
    else:
        print("✗ No assignment made")
        return False

def test_procedure_credential_enforcement():
    """Test that procedure credentials are required for procedure activities"""
    print("\n" + "="*60)
    print("TEST 3: Procedure Credential Enforcement")
    print("="*60)

    faculty_data = [
        {'id': 'rec_no_proc', 'Faculty': 'NoProc', 'Last Name': 'NoProc',
         'Performs Procedure': False, 'Faculty Status': 'Active'},
        {'id': 'rec_with_proc', 'Faculty': 'WithProc', 'Last Name': 'WithProc',
         'Performs Procedure': True, 'Faculty Status': 'Active'}
    ]

    master_assignments = [
        {
            'id': 'rec_ma_vasectomy',
            'Half-Day of the Week of Blocks': ['rec_hd_vas'],
            'Activity (from Rotation Templates)': ['Vasectomy Clinic'],
            'PGY Link (from Residency Block Schedule)': ['PGY-2']
        }
    ]

    engine = ACGMEComplianceEngine(faculty_data, {}, ACGME_RATIOS, SPECIALTY_REQUIREMENTS)
    result = engine.process_all_assignments(master_assignments)

    # Validate - should assign faculty with procedure credentials
    if result['assignments']:
        assigned_faculty = result['assignments'][0]['faculty_id']
        has_credentials = assigned_faculty == 'rec_with_proc'
        print(f"✓ Faculty with credentials assigned: {has_credentials}")
        print(f"  Assigned: {result['assignments'][0]['faculty_name']}")
        return has_credentials
    else:
        print("✗ No assignment made")
        return False

def test_pgy1_direct_supervision_required():
    """Test that PGY-1 always gets direct supervision"""
    print("\n" + "="*60)
    print("TEST 4: PGY-1 Direct Supervision Required")
    print("="*60)

    faculty_data = [
        {'id': 'rec_f1', 'Faculty': 'Faculty1', 'Last Name': 'F1',
         'Performs Procedure': True, 'Faculty Status': 'Active'}
    ]

    master_assignments = [
        {
            'id': 'rec_ma_pgy1',
            'Half-Day of the Week of Blocks': ['rec_hd_pgy1'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            'PGY Link (from Residency Block Schedule)': ['PGY-1']
        },
        {
            'id': 'rec_ma_pgy2',
            'Half-Day of the Week of Blocks': ['rec_hd_pgy2'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            'PGY Link (from Residency Block Schedule)': ['PGY-2']
        }
    ]

    engine = ACGMEComplianceEngine(faculty_data, {}, ACGME_RATIOS, SPECIALTY_REQUIREMENTS)
    result = engine.process_all_assignments(master_assignments)

    # Validate
    pgy1_assignment = next((a for a in result['assignments'] if a['pgy_level'] == 'PGY-1'), None)
    pgy2_assignment = next((a for a in result['assignments'] if a['pgy_level'] == 'PGY-2'), None)

    pgy1_direct = pgy1_assignment and pgy1_assignment['supervision_type'] == 'direct'
    pgy2_indirect = pgy2_assignment and pgy2_assignment['supervision_type'] == 'indirect'

    print(f"✓ PGY-1 has direct supervision: {pgy1_direct}")
    print(f"✓ PGY-2 has indirect supervision: {pgy2_indirect}")

    return pgy1_direct and pgy2_indirect

def test_workload_balancing():
    """Test that workload is balanced across faculty"""
    print("\n" + "="*60)
    print("TEST 5: Workload Balancing")
    print("="*60)

    faculty_data = [
        {'id': f'rec_f{i}', 'Faculty': f'Faculty{i}', 'Last Name': f'F{i}',
         'Performs Procedure': True, 'Faculty Status': 'Active'}
        for i in range(3)
    ]

    # Create 9 assignments (should distribute 3 each if balanced)
    master_assignments = [
        {
            'id': f'rec_ma_{i}',
            'Half-Day of the Week of Blocks': [f'rec_hd_{i}'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            'PGY Link (from Residency Block Schedule)': ['PGY-2']
        }
        for i in range(9)
    ]

    engine = ACGMEComplianceEngine(faculty_data, {}, ACGME_RATIOS, SPECIALTY_REQUIREMENTS)
    result = engine.process_all_assignments(master_assignments)

    # Check distribution
    utilization = {u['faculty_name']: u['assignment_count'] for u in result['faculty_utilization']}
    max_assignments = max(utilization.values())
    min_assignments = min(utilization.values())
    variance = max_assignments - min_assignments

    balanced = variance <= 1  # Should be nearly equal (difference of at most 1)

    print(f"✓ Workload balanced (variance ≤ 1): {balanced}")
    print(f"  Distribution: {utilization}")
    print(f"  Variance: {variance}")

    return balanced

def test_empty_input():
    """Test handling of empty input"""
    print("\n" + "="*60)
    print("TEST 6: Empty Input Handling")
    print("="*60)

    faculty_data = [
        {'id': 'rec_f1', 'Faculty': 'Faculty1', 'Last Name': 'F1',
         'Performs Procedure': True, 'Faculty Status': 'Active'}
    ]

    master_assignments = []

    engine = ACGMEComplianceEngine(faculty_data, {}, ACGME_RATIOS, SPECIALTY_REQUIREMENTS)
    result = engine.process_all_assignments(master_assignments)

    handles_empty = (result['statistics']['total_processed'] == 0 and
                     result['statistics']['successful_assignments'] == 0)

    print(f"✓ Handles empty input gracefully: {handles_empty}")
    print(f"  Total processed: {result['statistics']['total_processed']}")

    return handles_empty

def test_missing_data_fields():
    """Test handling of missing or incomplete data"""
    print("\n" + "="*60)
    print("TEST 7: Missing Data Fields Handling")
    print("="*60)

    faculty_data = [
        {'id': 'rec_f1', 'Faculty': 'Faculty1', 'Last Name': 'F1',
         'Performs Procedure': True, 'Faculty Status': 'Active'}
    ]

    # Assignment with missing activity
    master_assignments = [
        {
            'id': 'rec_ma_incomplete',
            'Half-Day of the Week of Blocks': ['rec_hd_001'],
            # Missing 'Activity (from Rotation Templates)'
            'PGY Link (from Residency Block Schedule)': ['PGY-1']
        },
        {
            'id': 'rec_ma_no_halfday',
            # Missing 'Half-Day of the Week of Blocks'
            'Activity (from Rotation Templates)': ['General Clinic'],
            'PGY Link (from Residency Block Schedule)': ['PGY-1']
        },
        {
            'id': 'rec_ma_complete',
            'Half-Day of the Week of Blocks': ['rec_hd_002'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            'PGY Link (from Residency Block Schedule)': ['PGY-1']
        }
    ]

    engine = ACGMEComplianceEngine(faculty_data, {}, ACGME_RATIOS, SPECIALTY_REQUIREMENTS)
    result = engine.process_all_assignments(master_assignments)

    # Should process only the complete one
    handles_missing = (result['statistics']['successful_assignments'] == 1 and
                      result['statistics']['total_processed'] == 3)

    print(f"✓ Handles missing fields gracefully: {handles_missing}")
    print(f"  Total processed: {result['statistics']['total_processed']}")
    print(f"  Successful: {result['statistics']['successful_assignments']}")

    return handles_missing

def test_acgme_compliance_tracking():
    """Test that ACGME compliance is properly tracked"""
    print("\n" + "="*60)
    print("TEST 8: ACGME Compliance Tracking")
    print("="*60)

    faculty_data = [
        {'id': 'rec_f1', 'Faculty': 'Faculty1', 'Last Name': 'F1',
         'Performs Procedure': True, 'Faculty Status': 'Active'}
    ]

    master_assignments = [
        {
            'id': 'rec_ma_001',
            'Half-Day of the Week of Blocks': ['rec_hd_001'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            'PGY Link (from Residency Block Schedule)': ['PGY-1']
        }
    ]

    engine = ACGMEComplianceEngine(faculty_data, {}, ACGME_RATIOS, SPECIALTY_REQUIREMENTS)
    result = engine.process_all_assignments(master_assignments)

    # Check that ACGME compliance is tracked
    assignment = result['assignments'][0]
    has_compliance_field = 'acgme_compliant' in assignment
    has_compliance_message = 'compliance_message' in assignment
    is_compliant = assignment.get('acgme_compliant', False)

    tracking_works = has_compliance_field and has_compliance_message and is_compliant

    print(f"✓ ACGME compliance tracked: {tracking_works}")
    print(f"  Compliant: {is_compliant}")
    print(f"  Message: {assignment.get('compliance_message', 'N/A')}")

    return tracking_works

def main():
    """Run all edge case tests"""
    print("="*60)
    print("PHASE 3 EDGE CASE TESTING")
    print("Testing Boundary Conditions & Error Handling")
    print("="*60)

    tests = [
        ("All Faculty Absent", test_all_faculty_absent),
        ("Specialty Requirement Enforcement", test_specialty_requirement_enforcement),
        ("Procedure Credential Enforcement", test_procedure_credential_enforcement),
        ("PGY-1 Direct Supervision", test_pgy1_direct_supervision_required),
        ("Workload Balancing", test_workload_balancing),
        ("Empty Input Handling", test_empty_input),
        ("Missing Data Fields", test_missing_data_fields),
        ("ACGME Compliance Tracking", test_acgme_compliance_tracking)
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} FAILED with exception: {e}")
            results[test_name] = False

    # Summary
    print("\n" + "="*60)
    print("EDGE CASE TEST SUMMARY")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print(f"\n{passed}/{total} tests passed ({(passed/total*100):.1f}%)")

    if passed == total:
        print("\n🎉 ALL EDGE CASE TESTS PASSED!")
        print("✅ Phase 3 is robust and handles edge cases properly")
        print("✅ Ready for production deployment")
        return 0
    else:
        print("\n⚠️  Some edge case tests failed")
        print("Please review and fix issues before deployment")
        return 1

if __name__ == "__main__":
    exit(main())
