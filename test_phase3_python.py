"""
Test harness for Phase 3 Enhanced Faculty Assignment (Python/Pyodide version)

This script validates the Python conversion by:
1. Creating realistic mock data
2. Running the Phase 3 engine
3. Validating outputs
4. Generating a test report
"""

from datetime import datetime, timedelta, date
from typing import Dict, List, Any, Optional
import json

print("="*80)
print("PHASE 3 PYTHON VALIDATION TEST")
print("="*80)

# =============================================================================
# MOCK N8N ENVIRONMENT
# =============================================================================

class MockN8nEnvironment:
    """Simulate n8n's input/output environment for testing."""

    def __init__(self):
        self.input_items = []
        self.output = None

    def set_input_all(self, items):
        """Set the mock input data."""
        self.input_items = items

    def get_input_all(self):
        """Mock n8n's _get_input_all() function."""
        return self.input_items

    def set_output(self, output):
        """Capture the output."""
        self.output = output

# Create mock environment
mock_env = MockN8nEnvironment()

# Mock the n8n function globally
def _get_input_all():
    return mock_env.get_input_all()

# =============================================================================
# GENERATE REALISTIC MOCK DATA
# =============================================================================

print("\n[1/5] Generating mock data...")

# Generate faculty data (10 faculty members)
mock_faculty_data = []
faculty_names = [
    ("Smith", "John"),
    ("Johnson", "Sarah"),
    ("Williams", "Michael"),
    ("Brown", "Emily"),
    ("Jones", "David"),
    ("Garcia", "Maria"),
    ("Miller", "Robert"),
    ("Davis", "Jennifer"),
    ("Rodriguez", "Carlos"),
    ("Martinez", "Lisa")
]

for i, (last_name, first_name) in enumerate(faculty_names):
    faculty_id = f"rec_faculty_{i+1:03d}"
    mock_faculty_data.append({
        'id': faculty_id,
        'Faculty': f"Dr. {first_name} {last_name}",
        'Last Name': last_name,
        'Primary Duty': 'Clinical Faculty' if i < 7 else 'Academic Faculty',
        'Performs Procedure': i < 5,  # First 5 can do procedures
        'Specialties': ['Family Medicine', 'Sports Medicine'] if i == 0 else ['Family Medicine'],
        'Available Monday': True,
        'Available Tuesday': i % 2 == 0,  # Half available on Tuesday
        'Available Wednesday': True,
        'Available Thursday': i % 3 != 0,  # Most available on Thursday
        'Available Friday': True,
        'Total Inpatient Weeks': 2 if i < 5 else 0,
        'Faculty Status': 'Active'
    })

# Generate Phase 0 absence data (3 faculty members with absences)
current_date = datetime.now()
mock_phase0_absence_data = {
    'facultyAbsences': {
        'rec_faculty_001': {
            (current_date + timedelta(days=5)).strftime('%Y-%m-%d'): {
                'leaveType': 'Conference',
                'timeOfDay': 'All Day',
                'replacementActivity': 'Conference Attendance (Virtual Supervision Available)',
                'comments': 'ACGME Conference - Virtual backup arranged'
            },
            (current_date + timedelta(days=6)).strftime('%Y-%m-%d'): {
                'leaveType': 'Conference',
                'timeOfDay': 'All Day',
                'replacementActivity': 'Conference Attendance (Virtual Supervision Available)',
                'comments': 'ACGME Conference - Virtual backup arranged'
            }
        },
        'rec_faculty_003': {
            (current_date + timedelta(days=3)).strftime('%Y-%m-%d'): {
                'leaveType': 'Personal Leave',
                'timeOfDay': 'PM',
                'replacementActivity': 'Personal Leave - Coverage Required',
                'comments': 'Afternoon only'
            }
        },
        'rec_faculty_005': {
            (current_date + timedelta(days=7)).strftime('%Y-%m-%d'): {
                'leaveType': 'Medical Leave',
                'timeOfDay': 'All Day',
                'replacementActivity': 'Medical Leave - Full Coverage Required',
                'comments': 'Urgent medical appointment'
            }
        }
    },
    'facultyReference': {
        faculty['id']: faculty['Faculty'] for faculty in mock_faculty_data
    }
}

# Generate clinic templates
mock_clinic_templates = [
    {
        'id': 'rec_template_001',
        'Name': 'Resident Supervision',
        'Category': 'Attending',
        'Activity Type': 'General Clinic',
        'Requires Specialty Credentials': False
    },
    {
        'id': 'rec_template_002',
        'Name': 'Procedure Template',
        'Category': 'Attending',
        'Activity Type': 'Procedure',
        'Requires Specialty Credentials': True
    },
    {
        'id': 'rec_template_003',
        'Name': 'Sports Medicine Clinic',
        'Category': 'Attending',
        'Activity Type': 'Sports Medicine',
        'Requires Specialty Credentials': True
    },
    {
        'id': 'rec_template_004',
        'Name': 'Inpatient Teaching',
        'Category': 'Attending',
        'Activity Type': 'Inpatient',
        'Requires Specialty Credentials': False
    }
]

# Generate master assignments (20 assignments across different days and activities)
mock_master_assignments = []
activities = [
    'Family Medicine Clinic',
    'Continuity Clinic',
    'Procedure Clinic',
    'Sports Medicine',
    'Family Medicine Inpatient',
    'General Clinic'
]
pgy_levels = ['PGY-1', 'PGY-2', 'PGY-3']

for i in range(20):
    day_offset = i % 10  # Spread across 10 days
    assignment_date = current_date + timedelta(days=day_offset)

    mock_master_assignments.append({
        'id': f'rec_assignment_{i+1:03d}',
        'Half-Day of the Week of Blocks': [f'rec_halfday_{i+1:03d}'],
        'Resident (from Residency Block Schedule)': [f'rec_resident_{(i % 5) + 1:03d}'],
        'PGY Link (from Residency Block Schedule)': [pgy_levels[i % 3]],
        'Activity (from Rotation Templates)': [activities[i % len(activities)]],
        'Date': assignment_date.strftime('%Y-%m-%d'),
        'Time of Day': 'AM' if i % 2 == 0 else 'PM'
    })

# Generate Phase 1 smart pairings (optional but good for testing integration)
mock_phase1_data = {
    'phase': 1,
    'smart_pairings': [
        {'resident_id': 'rec_resident_001', 'paired_blocks': 5},
        {'resident_id': 'rec_resident_002', 'paired_blocks': 4}
    ],
    'phase0_integration': {
        'verbatim_replacements': 3,
        'absence_aware_pairing': True
    }
}

# Assemble all input items (simulating n8n merge node output)
all_input_items = []

# Add master assignments
for assignment in mock_master_assignments:
    all_input_items.append({'json': assignment})

# Add faculty data
for faculty in mock_faculty_data:
    all_input_items.append({'json': faculty})

# Add clinic templates
for template in mock_clinic_templates:
    all_input_items.append({'json': template})

# Add Phase 0 data
all_input_items.append({'json': {
    'phase': 0,
    'absence_data': mock_phase0_absence_data
}})

# Add Phase 1 data
all_input_items.append({'json': mock_phase1_data})

# Set the mock input
mock_env.set_input_all(all_input_items)

print(f"✓ Created {len(mock_faculty_data)} faculty members")
print(f"✓ Created {len(mock_master_assignments)} master assignments")
print(f"✓ Created {len(mock_clinic_templates)} clinic templates")
print(f"✓ Created Phase 0 absence data with {len(mock_phase0_absence_data['facultyAbsences'])} faculty absences")
print(f"✓ Total input items: {len(all_input_items)}")

# =============================================================================
# RUN PHASE 3 PYTHON CODE
# =============================================================================

print("\n[2/5] Executing Phase 3 Enhanced Faculty Assignment Engine...")

# Import/execute the Phase 3 code
exec(open('/home/user/n8n-residency-scheduler-phases/phase3-enhanced-faculty-assignment-python.py').read())

# Capture the output (the Phase 3 script sets 'output' variable)
if 'output' in locals():
    test_output = output
    mock_env.set_output(test_output)
    print("✓ Phase 3 execution completed successfully")
else:
    raise RuntimeError("Phase 3 did not produce expected output")

# =============================================================================
# VALIDATE OUTPUTS
# =============================================================================

print("\n[3/5] Validating outputs...")

validation_results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def validate(condition, test_name, error_msg=""):
    """Helper to track validation results."""
    if condition:
        validation_results['passed'].append(test_name)
        print(f"  ✓ {test_name}")
        return True
    else:
        validation_results['failed'].append(f"{test_name}: {error_msg}")
        print(f"  ✗ {test_name}: {error_msg}")
        return False

# Extract results
result_data = test_output[0]['json']

# Validation 1: Basic structure
validate(
    'phase' in result_data and result_data['phase'] == 3,
    "Output contains correct phase number"
)

validate(
    result_data.get('success') == True,
    "Execution reported success"
)

validate(
    'enhanced_faculty_assignments' in result_data,
    "Output contains faculty assignments"
)

# Validation 2: Faculty assignments created
faculty_assignments = result_data.get('enhanced_faculty_assignments', [])
validate(
    len(faculty_assignments) > 0,
    f"Faculty assignments created ({len(faculty_assignments)} assignments)",
    f"Expected > 0, got {len(faculty_assignments)}"
)

validate(
    len(faculty_assignments) <= len(mock_master_assignments),
    "Faculty assignments not exceeding master assignments",
    f"Got {len(faculty_assignments)} faculty assignments for {len(mock_master_assignments)} master assignments"
)

# Validation 3: ACGME compliance
acgme_compliance = result_data.get('acgme_compliance', {})
validate(
    'complianceRate' in acgme_compliance,
    "ACGME compliance rate calculated"
)

# Parse compliance rate
compliance_rate_str = acgme_compliance.get('complianceRate', '0%')
try:
    compliance_rate = float(compliance_rate_str.replace('%', ''))
    validate(
        compliance_rate >= 50.0,
        f"ACGME compliance rate acceptable ({compliance_rate_str})",
        f"Compliance rate {compliance_rate}% is too low"
    )
except:
    validation_results['warnings'].append(f"Could not parse compliance rate: {compliance_rate_str}")

# Validation 4: Phase 0 integration
phase_integration = result_data.get('phase_integration', {})
validate(
    phase_integration.get('phase0AbsenceIntegration') is not None,
    "Phase 0 absence integration tracked"
)

validate(
    'absenceAwareAssignments' in phase_integration,
    "Absence-aware assignments counted"
)

# Validation 5: Absence substitutions
absence_substitutions = result_data.get('absence_substitutions', [])
print(f"  ℹ Info: {len(absence_substitutions)} absence substitutions applied")

# Validation 6: Coverage gaps
coverage_gaps = result_data.get('coverage_gaps', [])
if len(coverage_gaps) > len(mock_master_assignments) * 0.3:
    validation_results['warnings'].append(
        f"High coverage gap rate: {len(coverage_gaps)}/{len(mock_master_assignments)} ({len(coverage_gaps)/len(mock_master_assignments)*100:.1f}%)"
    )
else:
    print(f"  ✓ Coverage gaps acceptable ({len(coverage_gaps)} gaps)")

# Validation 7: Faculty utilization
faculty_utilization = result_data.get('faculty_utilization', [])
validate(
    len(faculty_utilization) > 0,
    f"Faculty utilization calculated ({len(faculty_utilization)} faculty)",
    f"Expected > 0, got {len(faculty_utilization)}"
)

# Validation 8: Check assignment structure
if faculty_assignments:
    sample_assignment = faculty_assignments[0]
    required_fields = [
        'assignmentId', 'halfDayId', 'facultyId', 'facultyName',
        'clinicTemplateId', 'supervisionType', 'pgyLevel'
    ]

    missing_fields = [field for field in required_fields if field not in sample_assignment]
    validate(
        len(missing_fields) == 0,
        "Assignment structure complete",
        f"Missing fields: {missing_fields}"
    )

    # Check for phase integration metadata
    validate(
        'phaseIntegration' in sample_assignment,
        "Phase integration metadata present"
    )

# Validation 9: Revolutionary improvements
revolutionary = result_data.get('revolutionary_improvements', {})
validate(
    'python_conversion' in revolutionary,
    "Python conversion acknowledged in output"
)

# =============================================================================
# DETAILED ANALYSIS
# =============================================================================

print("\n[4/5] Detailed analysis...")

# Analyze by supervision type
direct_supervision = [a for a in faculty_assignments if a.get('supervisionType') == 'direct']
indirect_supervision = [a for a in faculty_assignments if a.get('supervisionType') == 'indirect']

print(f"\n  Supervision Types:")
print(f"    - Direct supervision: {len(direct_supervision)}")
print(f"    - Indirect supervision: {len(indirect_supervision)}")

# Analyze by PGY level
pgy_distribution = {}
for assignment in faculty_assignments:
    pgy = assignment.get('pgyLevel', 'Unknown')
    pgy_distribution[pgy] = pgy_distribution.get(pgy, 0) + 1

print(f"\n  PGY Level Distribution:")
for pgy, count in sorted(pgy_distribution.items()):
    print(f"    - {pgy}: {count} assignments")

# Analyze faculty workload
print(f"\n  Faculty Utilization:")
for util in faculty_utilization[:5]:  # Top 5
    print(f"    - {util['facultyName']}: {util['totalAssignments']} assignments ({util['utilizationRate']})")

# Check absence substitutions in detail
if absence_substitutions:
    print(f"\n  Absence Substitutions ({len(absence_substitutions)}):")
    for sub in absence_substitutions[:3]:  # First 3
        print(f"    - {sub['date']}: {sub['originalActivity']} → {sub['replacementActivity']}")
        print(f"      Reason: {sub['absenceType']}")

# =============================================================================
# GENERATE TEST REPORT
# =============================================================================

print("\n[5/5] Generating test report...")

test_report = {
    'test_metadata': {
        'test_date': datetime.now().isoformat(),
        'phase_tested': 3,
        'phase_name': 'Enhanced Faculty Assignment (Python)',
        'test_type': 'Mock Data Validation'
    },
    'test_data_summary': {
        'faculty_count': len(mock_faculty_data),
        'master_assignments': len(mock_master_assignments),
        'clinic_templates': len(mock_clinic_templates),
        'faculty_with_absences': len(mock_phase0_absence_data['facultyAbsences']),
        'total_input_items': len(all_input_items)
    },
    'execution_results': {
        'success': result_data.get('success', False),
        'faculty_assignments_created': len(faculty_assignments),
        'absence_substitutions': len(absence_substitutions),
        'coverage_gaps': len(coverage_gaps),
        'acgme_compliance_rate': acgme_compliance.get('complianceRate', 'N/A'),
        'faculty_utilized': len(faculty_utilization)
    },
    'validation_summary': {
        'tests_passed': len(validation_results['passed']),
        'tests_failed': len(validation_results['failed']),
        'warnings': len(validation_results['warnings']),
        'total_tests': len(validation_results['passed']) + len(validation_results['failed'])
    },
    'detailed_validations': validation_results,
    'analysis': {
        'supervision_types': {
            'direct': len(direct_supervision),
            'indirect': len(indirect_supervision)
        },
        'pgy_distribution': pgy_distribution,
        'top_utilized_faculty': [
            {
                'name': u['facultyName'],
                'assignments': u['totalAssignments'],
                'utilization': u['utilizationRate']
            }
            for u in faculty_utilization[:3]
        ]
    }
}

# Calculate overall test result
tests_passed = len(validation_results['passed'])
tests_failed = len(validation_results['failed'])
total_tests = tests_passed + tests_failed
pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0

test_report['overall_result'] = {
    'status': 'PASS' if tests_failed == 0 else 'FAIL',
    'pass_rate': f"{pass_rate:.1f}%",
    'recommendation': 'Ready for deployment' if pass_rate >= 90 else 'Needs review'
}

# =============================================================================
# PRINT FINAL REPORT
# =============================================================================

print("\n" + "="*80)
print("TEST REPORT SUMMARY")
print("="*80)

print(f"\nTest Execution: {'✓ PASSED' if test_report['overall_result']['status'] == 'PASS' else '✗ FAILED'}")
print(f"Pass Rate: {test_report['overall_result']['pass_rate']}")
print(f"Recommendation: {test_report['overall_result']['recommendation']}")

print(f"\nValidation Results:")
print(f"  ✓ Passed: {tests_passed}/{total_tests}")
print(f"  ✗ Failed: {tests_failed}/{total_tests}")
print(f"  ⚠ Warnings: {len(validation_results['warnings'])}")

if validation_results['failed']:
    print(f"\nFailed Tests:")
    for failure in validation_results['failed']:
        print(f"  ✗ {failure}")

if validation_results['warnings']:
    print(f"\nWarnings:")
    for warning in validation_results['warnings']:
        print(f"  ⚠ {warning}")

print(f"\nKey Metrics:")
print(f"  - Faculty assignments created: {len(faculty_assignments)}")
print(f"  - ACGME compliance rate: {acgme_compliance.get('complianceRate', 'N/A')}")
print(f"  - Absence substitutions: {len(absence_substitutions)}")
print(f"  - Coverage gaps: {len(coverage_gaps)}")
print(f"  - Faculty utilized: {len(faculty_utilization)}/{len(mock_faculty_data)}")

print(f"\nPhase Integration:")
print(f"  - Phase 0 absence checking: {'✓' if phase_integration.get('phase0AbsenceIntegration') else '✗'}")
print(f"  - Phase 5 eliminated: {'✓' if phase_integration.get('phase5Eliminated') else '✗'}")
print(f"  - Smart pairing compatible: {'✓' if phase_integration.get('smartPairingCompatible') else '✗'}")

print("\n" + "="*80)

# Save test report to file
with open('/home/user/n8n-residency-scheduler-phases/phase3_test_report.json', 'w') as f:
    json.dump(test_report, f, indent=2)

print("\n✓ Test report saved to: phase3_test_report.json")

# Exit with appropriate code
exit(0 if tests_failed == 0 else 1)
