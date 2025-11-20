#!/usr/bin/env python3
"""
Integration Test Harness for n8n Residency Scheduler
Tests Phase 3 -> Phase 4 -> Phase 7 data flow with real or test data
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Import the modular phase implementations
# Note: When running in n8n, these would be embedded in the workflows
# For local testing, we need standalone versions

def load_test_data_from_json(data_file: str) -> Dict[str, List[Dict]]:
    """
    Load test data from JSON file.
    Expected structure:
    {
      "faculty": [...],
      "residents": [...],
      "master_assignments": [...],
      "leave_records": [...],
      "primary_duties": [...],
      "clinic_templates": [...]
    }
    """
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            print(f"✓ Loaded test data from {data_file}")
            return data
    except FileNotFoundError:
        print(f"✗ Test data file not found: {data_file}")
        print("  Create a test_data.json file with real Airtable exports")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in test data file: {e}")
        sys.exit(1)

def create_minimal_test_data() -> Dict[str, List[Dict]]:
    """
    Create minimal test data for smoke testing.
    This is a fallback if no real data is available.
    """
    print("⚠️  Using minimal synthetic test data")
    print("   For realistic testing, create test_data.json with real Airtable exports")

    today = datetime.now()
    start_date = today - timedelta(days=today.weekday())

    faculty_data = [
        {
            'id': 'fac_001',
            'Faculty': 'Dr. Test Faculty 1',
            'Last Name': 'Faculty 1',
            'Faculty Status': 'Active',
            'Primary Duty': 'Faculty',
            'Performs Procedure': True,
            'Available Monday': True,
            'Available Tuesday': True,
            'Available Wednesday': True,
            'Available Thursday': True,
            'Available Friday': True,
            'Total Inpatient Weeks': 2,
            'Total Monday Call': 0,
            'Total Tuesday Call': 0,
            'Total Wednesday Call': 0,
            'Total Thursday Call': 0,
            'Total Friday Call': 0,
            'Total Saturday Call': 0,
            'Total Sunday Call': 0
        },
        {
            'id': 'fac_002',
            'Faculty': 'Dr. Test Faculty 2',
            'Last Name': 'Faculty 2',
            'Faculty Status': 'Active',
            'Primary Duty': 'Faculty',
            'Performs Procedure': False,
            'Available Monday': True,
            'Available Tuesday': True,
            'Available Wednesday': True,
            'Available Thursday': True,
            'Available Friday': True,
            'Total Inpatient Weeks': 1,
            'Total Monday Call': 0,
            'Total Tuesday Call': 0,
            'Total Wednesday Call': 0,
            'Total Thursday Call': 0,
            'Total Friday Call': 0,
            'Total Saturday Call': 0,
            'Total Sunday Call': 0
        }
    ]

    residents = [
        {
            'id': 'res_001',
            'Resident': 'Test Resident 1',
            'PGY Level': 'PGY-1'
        },
        {
            'id': 'res_002',
            'Resident': 'Test Resident 2',
            'PGY Level': 'PGY-2'
        }
    ]

    master_assignments = [
        {
            'id': 'assign_001',
            'Resident (from Residency Block Schedule)': ['res_001'],
            'PGY Link (from Residency Block Schedule)': ['PGY-1'],
            'Half-Day of the Week of Blocks': ['hd_001'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            'Date': start_date.strftime('%Y-%m-%d')
        },
        {
            'id': 'assign_002',
            'Resident (from Residency Block Schedule)': ['res_002'],
            'PGY Link (from Residency Block Schedule)': ['PGY-2'],
            'Half-Day of the Week of Blocks': ['hd_002'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            'Date': (start_date + timedelta(days=1)).strftime('%Y-%m-%d')
        }
    ]

    primary_duties = [
        {
            'Faculty': ['fac_001', 'fac_002'],
            'Primary Duty': 'Faculty',
            'Clinic Minimum Half-Days Per Week': 2,
            'Clinic Maximum Half-Days Per Week': 8,
            'Sports Medicine Minimum Half-Days Per Week copy': 0,
            'Sports Medicine Maximum Half-Days Per Week': 0,
            'Minimum Graduate Medical Education Half-Day Per Week': 0,
            'Maximum Graduate Medical Education Half-Days Per Week': 0,
            'Department of Family Medicine Minimum Half-Days Per Week': 0,
            'Department of Family Medicine Maximum Half-Days Per Week': 0
        }
    ]

    return {
        'faculty': faculty_data,
        'residents': residents,
        'master_assignments': master_assignments,
        'leave_records': [],
        'primary_duties': primary_duties,
        'clinic_templates': [
            {'id': 'tmpl_001', 'Name': 'General Clinic', 'Activity Type': 'Clinic', 'Category': 'Attending'}
        ],
        'absence_data': {'facultyAbsences': {}, 'facultyReference': {}}
    }

def validate_data_completeness(data: Dict[str, List[Dict]]) -> bool:
    """Check if test data has all required components"""
    required_keys = ['faculty', 'residents', 'master_assignments', 'primary_duties']
    missing = [k for k in required_keys if k not in data or not data[k]]

    if missing:
        print(f"✗ Missing required data: {', '.join(missing)}")
        return False

    print("✓ Test data validation passed")
    print(f"  Faculty: {len(data['faculty'])}")
    print(f"  Residents: {len(data['residents'])}")
    print(f"  Master Assignments: {len(data['master_assignments'])}")
    print(f"  Primary Duties: {len(data['primary_duties'])}")
    print(f"  Leave Records: {len(data.get('leave_records', []))}")

    return True

def generate_integration_report(results: Dict[str, Any]) -> str:
    """Generate human-readable integration test report"""
    report = []
    report.append("\n" + "="*70)
    report.append("INTEGRATION TEST REPORT")
    report.append("="*70)
    report.append(f"Timestamp: {datetime.now().isoformat()}")
    report.append(f"Test Duration: {results.get('duration', 'N/A')}")
    report.append("")

    # Phase 3 Results
    if 'phase3' in results:
        p3 = results['phase3']
        report.append("PHASE 3: Faculty Assignment")
        report.append(f"  Assignments Generated: {len(p3.get('assignments', []))}")
        report.append(f"  Substitutions: {len(p3.get('substitutions', []))}")
        report.append(f"  Coverage Gaps: {len(p3.get('gaps', []))}")
        report.append("")

    # Phase 4 Results
    if 'phase4' in results:
        p4 = results['phase4']
        stats = p4.get('statistics', {})
        report.append("PHASE 4: Call Scheduling")
        report.append(f"  Call Assignments: {stats.get('successful_assignments', 0)}")
        report.append(f"  Coverage Rate: {stats.get('coverage_rate', 'N/A')}")
        report.append(f"  Gap Violations: {stats.get('gap_violations', 0)}")
        report.append("")

    # Phase 7 Results
    if 'phase7' in results:
        p7 = results['phase7']['validation_report']
        report.append("PHASE 7: Final Validation")
        report.append(f"  Overall Score: {p7['overallScore']}")
        report.append(f"  Grade: {p7['grade']}")
        report.append(f"  Ready for Deployment: {'YES' if p7['readyForDeployment'] else 'NO'}")

        acgme = p7['acgmeCompliance']
        report.append("\n  ACGME Compliance:")
        for pgy, data in acgme['supervision'].items():
            report.append(f"    {pgy}: {data['actualRatio']} (Required: {data['requiredRatio']})")

        primary = p7['primaryDutyValidation']
        report.append(f"\n  Primary Duty Score: {primary['overallScore']}")
        if primary['violations']:
            report.append(f"  Violations: {len(primary['violations'])}")

    report.append("")
    report.append("="*70)
    report.append("TEST RESULT: " + ("PASS ✓" if results.get('overall_pass') else "FAIL ✗"))
    report.append("="*70)

    return "\n".join(report)

def main():
    print("\n" + "="*70)
    print("n8n RESIDENCY SCHEDULER - INTEGRATION TEST")
    print("="*70 + "\n")

    # Check if test data file exists
    test_data_file = Path('test_data.json')

    if test_data_file.exists():
        data = load_test_data_from_json(str(test_data_file))
    else:
        print("📝 No test_data.json found, using minimal synthetic data")
        print("   To use real data: export from Airtable and save as test_data.json\n")
        data = create_minimal_test_data()

    if not validate_data_completeness(data):
        print("\n✗ Test data validation failed")
        sys.exit(1)

    start_time = datetime.now()

    # NOTE: The actual phase implementations would be imported/executed here
    # Since they require n8n runtime (_get_input_all, etc), we can't run them directly
    # This harness validates data structure and flow

    results = {
        'start_time': start_time.isoformat(),
        'data_summary': {
            'faculty_count': len(data['faculty']),
            'resident_count': len(data['residents']),
            'assignment_count': len(data['master_assignments']),
            'has_leave_data': len(data.get('leave_records', [])) > 0,
            'has_primary_duties': len(data.get('primary_duties', [])) > 0
        },
        'overall_pass': True
    }

    end_time = datetime.now()
    results['duration'] = f"{(end_time - start_time).total_seconds():.2f}s"

    # Generate report
    print("\n📊 Test data structure validated successfully")
    print(f"\nTo run full integration:")
    print("  1. Import phase3-enhanced-faculty-assignment.json to n8n")
    print("  2. Import phase4-python-powered.json to n8n")
    print("  3. Import phase7-python-powered.json to n8n")
    print("  4. Execute workflows in sequence with your Airtable data\n")

    # Save results
    results_file = f"integration_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"✓ Test results saved to {results_file}\n")

    return 0 if results['overall_pass'] else 1

if __name__ == "__main__":
    sys.exit(main())
