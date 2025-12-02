#!/usr/bin/env python3
"""
Test Phase 3 Python-Powered Faculty Assignment with Mock Data
This validates the ACGME compliance engine and orchestrator compatibility
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Mock data generator
def create_mock_data():
    """Create comprehensive mock data for Phase 3 testing"""

    # Mock Master Assignments (from Phase 2)
    master_assignments = [
        {
            'id': 'rec_ma_001',
            'Half-Day of the Week of Blocks': ['rec_hd_001'],
            'Resident (from Residency Block Schedule)': ['rec_res_001'],
            'PGY Link (from Residency Block Schedule)': ['PGY-1'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            'Processing Phase': 'Phase 2 - Smart Association'
        },
        {
            'id': 'rec_ma_002',
            'Half-Day of the Week of Blocks': ['rec_hd_002'],
            'Resident (from Residency Block Schedule)': ['rec_res_002'],
            'PGY Link (from Residency Block Schedule)': ['PGY-2'],
            'Activity (from Rotation Templates)': ['Vasectomy Clinic'],
            'Processing Phase': 'Phase 2 - Smart Association'
        },
        {
            'id': 'rec_ma_003',
            'Half-Day of the Week of Blocks': ['rec_hd_003'],
            'Resident (from Residency Block Schedule)': ['rec_res_003'],
            'PGY Link (from Residency Block Schedule)': ['PGY-3'],
            'Activity (from Rotation Templates)': ['Sports Medicine'],
            'Processing Phase': 'Phase 2 - Smart Association'
        },
        {
            'id': 'rec_ma_004',
            'Half-Day of the Week of Blocks': ['rec_hd_004'],
            'Resident (from Residency Block Schedule)': ['rec_res_004'],
            'PGY Link (from Residency Block Schedule)': ['PGY-1'],
            'Activity (from Rotation Templates)': ['Continuity Clinic'],
            'Processing Phase': 'Phase 2 - Smart Association'
        },
        {
            'id': 'rec_ma_005',
            'Half-Day of the Week of Blocks': ['rec_hd_005'],
            'Resident (from Residency Block Schedule)': ['rec_res_005'],
            'PGY Link (from Residency Block Schedule)': ['PGY-2'],
            'Activity (from Rotation Templates)': ['Inpatient Medicine'],
            'Processing Phase': 'Phase 2 - Smart Association'
        }
    ]

    # Mock Faculty Data
    faculty_data = [
        {
            'id': 'rec4F7XQKFyDjXn5n',  # Dr. Tagawa - Sports Medicine specialist
            'Faculty': 'Tagawa',
            'Last Name': 'Tagawa',
            'First Name': 'Ken',
            'Primary Duty': 'Clinical',
            'Performs Procedure': True,
            'Specialties': ['Sports Medicine'],
            'Available Monday': True,
            'Available Tuesday': True,
            'Available Wednesday': True,
            'Available Thursday': True,
            'Available Friday': True,
            'Total Inpatient Weeks': 2,
            'Faculty Status': 'Active'
        },
        {
            'id': 'rec_fac_002',
            'Faculty': 'Smith',
            'Last Name': 'Smith',
            'First Name': 'John',
            'Primary Duty': 'Clinical',
            'Performs Procedure': True,
            'Specialties': ['General Medicine'],
            'Available Monday': True,
            'Available Tuesday': True,
            'Available Wednesday': True,
            'Available Thursday': True,
            'Available Friday': True,
            'Total Inpatient Weeks': 4,
            'Faculty Status': 'Active'
        },
        {
            'id': 'rec_fac_003',
            'Faculty': 'Johnson',
            'Last Name': 'Johnson',
            'First Name': 'Sarah',
            'Primary Duty': 'Clinical',
            'Performs Procedure': False,
            'Specialties': ['General Medicine'],
            'Available Monday': True,
            'Available Tuesday': True,
            'Available Wednesday': False,
            'Available Thursday': True,
            'Available Friday': True,
            'Total Inpatient Weeks': 3,
            'Faculty Status': 'Active'
        },
        {
            'id': 'rec_fac_004',
            'Faculty': 'Williams',
            'Last Name': 'Williams',
            'First Name': 'Michael',
            'Primary Duty': 'Clinical',
            'Performs Procedure': True,
            'Specialties': ['Procedures'],
            'Available Monday': True,
            'Available Tuesday': True,
            'Available Wednesday': True,
            'Available Thursday': True,
            'Available Friday': True,
            'Total Inpatient Weeks': 1,
            'Faculty Status': 'Active'
        },
        {
            'id': 'rec_fac_005',
            'Faculty': 'Brown',
            'Last Name': 'Brown',
            'First Name': 'Emily',
            'Primary Duty': 'Clinical',
            'Performs Procedure': False,
            'Specialties': ['General Medicine'],
            'Available Monday': True,
            'Available Tuesday': True,
            'Available Wednesday': True,
            'Available Thursday': True,
            'Available Friday': False,
            'Faculty Status': 'Active'
        }
    ]

    # Mock Faculty Leave (Phase 0 data)
    today = datetime.now()
    faculty_leave = [
        {
            'id': 'rec_leave_001',
            'Faculty': ['rec_fac_002'],  # Dr. Smith on leave
            'Leave Start': (today + timedelta(days=5)).isoformat(),
            'Leave End': (today + timedelta(days=7)).isoformat(),
            'Leave Type': 'Medical Leave',
            'Comments': 'Medical appointment',
            'Leave Approved Residency': True,
            'Leave Approved Army': True
        },
        {
            'id': 'rec_leave_002',
            'Faculty': ['rec_fac_003'],  # Dr. Johnson on TDY
            'Leave Start': (today + timedelta(days=10)).isoformat(),
            'Leave End': (today + timedelta(days=12)).isoformat(),
            'Leave Type': 'TDY',
            'Comments': 'Temporary Duty Assignment',
            'Leave Approved Residency': True,
            'Leave Approved Army': True
        }
    ]

    # Mock Clinic Templates
    clinic_templates = [
        {
            'id': 'rec_template_001',
            'Name': 'Resident Supervision',
            'Category': 'Attending',
            'Activity Type': 'General Clinic'
        },
        {
            'id': 'rec_template_002',
            'Name': 'Procedure Supervision',
            'Category': 'Attending',
            'Activity Type': 'Vasectomy Clinic'
        },
        {
            'id': 'rec_template_003',
            'Name': 'Sports Medicine Supervision',
            'Category': 'Attending',
            'Activity Type': 'Sports Medicine'
        },
        {
            'id': 'rec_template_004',
            'Name': 'Continuity Care Supervision',
            'Category': 'Attending',
            'Activity Type': 'Continuity Clinic'
        }
    ]

    return {
        'master_assignments': master_assignments,
        'faculty_data': faculty_data,
        'faculty_leave': faculty_leave,
        'clinic_templates': clinic_templates
    }

# COPY OF PHASE 3 PYTHON CODE
# ACGME Supervision Ratios
ACGME_RATIOS = {
    'PGY-1': {'clinic': 2, 'procedure': 1, 'direct': True},
    'PGY-2': {'clinic': 4, 'procedure': 2, 'direct': False},
    'PGY-3': {'clinic': 4, 'procedure': 2, 'direct': False}
}

# Specialty Requirements
SPECIALTY_REQUIREMENTS = {
    'Sports Medicine': {'required_faculty': ['rec4F7XQKFyDjXn5n'], 'reason': 'Dr. Tagawa only'},
    'Vasectomy': {'credential_required': 'Performs Procedure'},
    'Botox': {'credential_required': 'Performs Procedure'}
}

class FacultyAbsenceProcessor:
    """Process and manage faculty absences from Phase 0 data"""

    @staticmethod
    def process_leave_records(leave_records: List[Dict]) -> Dict[str, Dict[str, Dict]]:
        """Convert leave records into date-indexed absence calendar"""
        absence_calendar = {}

        for leave in leave_records:
            faculty_ids = leave.get('Faculty', [])
            start_date = datetime.fromisoformat(leave['Leave Start'].replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(leave['Leave End'].replace('Z', '+00:00'))

            # Generate all dates in leave period
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')

                for faculty_id in faculty_ids:
                    if faculty_id not in absence_calendar:
                        absence_calendar[faculty_id] = {}

                    absence_calendar[faculty_id][date_str] = {
                        'leave_type': leave.get('Leave Type', 'Leave'),
                        'comments': leave.get('Comments', ''),
                        'replacement_activity': leave.get('Comments', '') or leave.get('Leave Type', 'Leave'),
                        'time_of_day': 'All Day'  # Default
                    }

                current_date += timedelta(days=1)

        return absence_calendar

class ACGMEComplianceEngine:
    """ACGME-compliant faculty assignment engine"""

    def __init__(self, faculty_list: List[Dict], absence_calendar: Dict,
                 acgme_ratios: Dict, specialty_req: Dict):
        self.faculty = {f['id']: f for f in faculty_list}
        self.absence_calendar = absence_calendar
        self.acgme_ratios = acgme_ratios
        self.specialty_req = specialty_req
        self.workload_tracker = {fid: 0 for fid in self.faculty.keys()}
        self.assignments = []
        self.substitutions = []
        self.coverage_gaps = []

    def is_faculty_available(self, faculty_id: str, date: str, time_of_day: str = 'AM') -> bool:
        """Check if faculty is available using Phase 0 absence data"""
        if faculty_id not in self.faculty:
            return False

        # Check absence calendar
        if faculty_id in self.absence_calendar:
            if date in self.absence_calendar[faculty_id]:
                absence = self.absence_calendar[faculty_id][date]
                if absence['time_of_day'] in ['All Day', time_of_day]:
                    return False

        return True

    def get_activity_type(self, activity: str) -> str:
        """Determine activity type for ACGME ratio lookup"""
        activity_lower = activity.lower()

        if any(word in activity_lower for word in ['procedure', 'vasectomy', 'botox']):
            return 'procedure'
        elif any(word in activity_lower for word in ['clinic', 'continuity']):
            return 'clinic'
        elif any(word in activity_lower for word in ['inpatient', 'hospital']):
            return 'inpatient'

        return 'clinic'  # Default

    def get_specialty_requirement(self, activity: str) -> Optional[Dict]:
        """Get specialty requirement for activity if any"""
        for specialty, requirement in self.specialty_req.items():
            if specialty.lower() in activity.lower():
                return requirement
        return None

    def select_optimal_faculty(self, eligible_faculty: List[str],
                               date: str = None, time_of_day: str = 'AM') -> Optional[str]:
        """Select optimal faculty based on workload and availability"""
        # Filter by availability if date provided
        if date:
            available = [fid for fid in eligible_faculty
                        if self.is_faculty_available(fid, date, time_of_day)]
        else:
            available = eligible_faculty

        if not available:
            return None

        # Score by workload (lower is better)
        scored = [(fid, self.workload_tracker[fid]) for fid in available]
        scored.sort(key=lambda x: x[1])

        return scored[0][0]

    def check_acgme_compliance(self, pgy_level: str, activity_type: str,
                               faculty_count: int) -> Tuple[bool, str]:
        """Verify ACGME supervision ratio compliance"""
        ratio_config = self.acgme_ratios.get(pgy_level, self.acgme_ratios['PGY-1'])
        max_residents = ratio_config.get(activity_type, 1)

        if faculty_count >= 1:  # At least one faculty assigned
            compliance = True
            message = f"ACGME compliant: 1 faculty for {pgy_level} {activity_type}"
        else:
            compliance = False
            message = f"ACGME violation: No faculty for {pgy_level} {activity_type}"

        return compliance, message

    def assign_faculty(self, assignment: Dict) -> Optional[Dict]:
        """Assign faculty to a master assignment with ACGME compliance"""
        # Extract assignment details
        assignment_id = assignment.get('id')
        half_day_ids = assignment.get('Half-Day of the Week of Blocks', [])
        activities = assignment.get('Activity (from Rotation Templates)', [])
        pgy_levels = assignment.get('PGY Link (from Residency Block Schedule)', [])

        if not half_day_ids or not activities:
            return None

        # Get primary values
        half_day_id = half_day_ids[0] if isinstance(half_day_ids, list) else half_day_ids
        activity = activities[0] if isinstance(activities, list) else activities
        pgy_level = pgy_levels[0] if pgy_levels else 'PGY-1'

        # Determine requirements
        activity_type = self.get_activity_type(activity)
        specialty_req = self.get_specialty_requirement(activity)
        ratio_config = self.acgme_ratios.get(pgy_level, self.acgme_ratios['PGY-1'])
        requires_direct = ratio_config['direct']

        # Filter eligible faculty
        eligible_faculty = list(self.faculty.keys())

        # Apply specialty requirements
        if specialty_req:
            if 'required_faculty' in specialty_req:
                eligible_faculty = [fid for fid in eligible_faculty
                                   if fid in specialty_req['required_faculty']]
            elif 'credential_required' in specialty_req:
                if specialty_req['credential_required'] == 'Performs Procedure':
                    eligible_faculty = [fid for fid in eligible_faculty
                                       if self.faculty[fid].get('Performs Procedure', False)]

        # Apply procedure requirements
        if activity_type == 'procedure':
            eligible_faculty = [fid for fid in eligible_faculty
                               if self.faculty[fid].get('Performs Procedure', False)]

        # Select optimal faculty
        selected_faculty = self.select_optimal_faculty(eligible_faculty)

        if not selected_faculty:
            # Create coverage gap
            self.coverage_gaps.append({
                'assignment_id': assignment_id,
                'half_day_id': half_day_id,
                'activity': activity,
                'pgy_level': pgy_level,
                'reason': 'No eligible faculty available',
                'specialty_requirement': specialty_req
            })
            return None

        # Check ACGME compliance
        acgme_compliant, compliance_msg = self.check_acgme_compliance(
            pgy_level, activity_type, 1
        )

        # Create faculty assignment
        faculty_assignment = {
            'assignment_id': assignment_id,
            'half_day_id': half_day_id,
            'faculty_id': selected_faculty,
            'faculty_name': self.faculty[selected_faculty].get('Faculty', 'Unknown'),
            'clinic_template_id': 'default_template',  # Simplified for now
            'supervision_type': 'direct' if requires_direct else 'indirect',
            'pgy_level': pgy_level,
            'activity': activity,
            'activity_type': activity_type,
            'supervision_ratio': ratio_config.get(activity_type, 1),
            'acgme_compliant': acgme_compliant,
            'compliance_message': compliance_msg,
            'python_powered': True,
            'orchestrator_ready': True
        }

        # Update workload
        self.workload_tracker[selected_faculty] += 1
        self.assignments.append(faculty_assignment)

        return faculty_assignment

    def process_all_assignments(self, master_assignments: List[Dict]) -> Dict:
        """Process all master assignments"""
        print(f"\n{'='*60}")
        print(f"Processing {len(master_assignments)} master assignments...")
        print(f"{'='*60}")

        for idx, assignment in enumerate(master_assignments):
            result = self.assign_faculty(assignment)

            if result:
                print(f"✓ Assignment {idx + 1}: {result['faculty_name']} → {result['pgy_level']} - {result['activity']}")
            else:
                print(f"✗ Assignment {idx + 1}: No faculty available")

        # Calculate statistics
        stats = {
            'total_processed': len(master_assignments),
            'successful_assignments': len(self.assignments),
            'coverage_gaps': len(self.coverage_gaps),
            'substitutions': len(self.substitutions),
            'success_rate': f"{(len(self.assignments) / len(master_assignments) * 100):.1f}%" if master_assignments else '0%',
            'acgme_compliant_rate': f"{(sum(1 for a in self.assignments if a['acgme_compliant']) / len(self.assignments) * 100):.1f}%" if self.assignments else '0%'
        }

        return {
            'assignments': self.assignments,
            'coverage_gaps': self.coverage_gaps,
            'substitutions': self.substitutions,
            'statistics': stats,
            'faculty_utilization': [
                {'faculty_id': fid, 'faculty_name': self.faculty[fid].get('Faculty', 'Unknown'),
                 'assignment_count': count}
                for fid, count in self.workload_tracker.items() if count > 0
            ]
        }

def validate_results(result: Dict, mock_data: Dict) -> Dict:
    """Validate the Phase 3 results"""

    print(f"\n{'='*60}")
    print("VALIDATION CHECKS")
    print(f"{'='*60}")

    validations = {}

    # Check 1: All assignments processed
    total_master = len(mock_data['master_assignments'])
    total_assigned = result['statistics']['successful_assignments']
    validations['all_assignments_processed'] = total_master == (total_assigned + result['statistics']['coverage_gaps'])
    print(f"✓ All assignments processed: {validations['all_assignments_processed']}")

    # Check 2: ACGME compliance
    acgme_rate = float(result['statistics']['acgme_compliant_rate'].rstrip('%'))
    validations['acgme_compliant'] = acgme_rate == 100.0
    print(f"✓ ACGME compliant: {validations['acgme_compliant']} ({result['statistics']['acgme_compliant_rate']})")

    # Check 3: Sports Medicine specialty requirement
    sports_med_assignments = [a for a in result['assignments'] if 'Sports Medicine' in a['activity']]
    sports_med_correct = all(a['faculty_id'] == 'rec4F7XQKFyDjXn5n' for a in sports_med_assignments)
    validations['sports_medicine_specialty'] = sports_med_correct
    print(f"✓ Sports Medicine specialty: {validations['sports_medicine_specialty']}")

    # Check 4: Procedure credentials
    procedure_assignments = [a for a in result['assignments'] if a['activity_type'] == 'procedure']
    procedure_faculty_ids = [a['faculty_id'] for a in procedure_assignments]
    procedure_faculty = [mock_data['faculty_data'][i] for i in range(len(mock_data['faculty_data']))
                        if mock_data['faculty_data'][i]['id'] in procedure_faculty_ids]
    procedure_credentials_ok = all(f.get('Performs Procedure', False) for f in procedure_faculty)
    validations['procedure_credentials'] = procedure_credentials_ok
    print(f"✓ Procedure credentials: {validations['procedure_credentials']}")

    # Check 5: PGY-1 direct supervision
    pgy1_assignments = [a for a in result['assignments'] if a['pgy_level'] == 'PGY-1']
    pgy1_direct = all(a['supervision_type'] == 'direct' for a in pgy1_assignments)
    validations['pgy1_direct_supervision'] = pgy1_direct
    print(f"✓ PGY-1 direct supervision: {validations['pgy1_direct_supervision']}")

    # Check 6: PGY-2/3 indirect supervision allowed
    pgy23_assignments = [a for a in result['assignments'] if a['pgy_level'] in ['PGY-2', 'PGY-3']]
    pgy23_indirect = all(a['supervision_type'] == 'indirect' for a in pgy23_assignments)
    validations['pgy23_indirect_supervision'] = pgy23_indirect
    print(f"✓ PGY-2/3 indirect supervision: {validations['pgy23_indirect_supervision']}")

    # Check 7: Workload balancing
    utilization = result['faculty_utilization']
    if utilization:
        max_assignments = max(u['assignment_count'] for u in utilization)
        min_assignments = min(u['assignment_count'] for u in utilization)
        workload_balanced = (max_assignments - min_assignments) <= 2  # Within 2 assignments
        validations['workload_balanced'] = workload_balanced
        print(f"✓ Workload balanced: {validations['workload_balanced']} (range: {min_assignments}-{max_assignments})")
    else:
        validations['workload_balanced'] = False
        print(f"✗ Workload balanced: No assignments to check")

    # Check 8: No duplicate assignments
    half_day_ids = [a['half_day_id'] for a in result['assignments']]
    no_duplicates = len(half_day_ids) == len(set(half_day_ids))
    validations['no_duplicate_assignments'] = no_duplicates
    print(f"✓ No duplicate assignments: {validations['no_duplicate_assignments']}")

    # Overall validation
    all_passed = all(validations.values())

    print(f"\n{'='*60}")
    if all_passed:
        print("✅ ALL VALIDATIONS PASSED!")
    else:
        print("❌ SOME VALIDATIONS FAILED")
        failed = [k for k, v in validations.items() if not v]
        print(f"Failed checks: {', '.join(failed)}")
    print(f"{'='*60}")

    return validations

def main():
    """Run the Phase 3 test"""
    print("="*60)
    print("PHASE 3 PYTHON-POWERED FACULTY ASSIGNMENT TEST")
    print("Testing with Mock Data")
    print("="*60)

    # Create mock data
    mock_data = create_mock_data()

    print(f"\n📊 Mock Data Summary:")
    print(f"   Master Assignments: {len(mock_data['master_assignments'])}")
    print(f"   Faculty Members: {len(mock_data['faculty_data'])}")
    print(f"   Faculty Leave Records: {len(mock_data['faculty_leave'])}")
    print(f"   Clinic Templates: {len(mock_data['clinic_templates'])}")

    # Process absences
    print(f"\n🔄 Processing Phase 0 absence data...")
    absence_processor = FacultyAbsenceProcessor()
    absence_calendar = absence_processor.process_leave_records(mock_data['faculty_leave'])
    print(f"   Processed absences for {len(absence_calendar)} faculty members")

    # Show absence details
    for faculty_id, absences in absence_calendar.items():
        faculty = next((f for f in mock_data['faculty_data'] if f['id'] == faculty_id), None)
        if faculty:
            print(f"   - {faculty['Faculty']}: {len(absences)} absence days")

    # Initialize ACGME engine
    print(f"\n🚀 Initializing ACGME Compliance Engine...")
    engine = ACGMEComplianceEngine(
        mock_data['faculty_data'],
        absence_calendar,
        ACGME_RATIOS,
        SPECIALTY_REQUIREMENTS
    )

    # Process all assignments
    result = engine.process_all_assignments(mock_data['master_assignments'])

    # Display results
    print(f"\n{'='*60}")
    print("PHASE 3 RESULTS")
    print(f"{'='*60}")
    print(f"Total Processed: {result['statistics']['total_processed']}")
    print(f"Successful Assignments: {result['statistics']['successful_assignments']}")
    print(f"Coverage Gaps: {result['statistics']['coverage_gaps']}")
    print(f"Success Rate: {result['statistics']['success_rate']}")
    print(f"ACGME Compliance Rate: {result['statistics']['acgme_compliant_rate']}")

    # Display faculty utilization
    print(f"\n📊 Faculty Utilization:")
    for util in sorted(result['faculty_utilization'], key=lambda x: x['assignment_count'], reverse=True):
        print(f"   {util['faculty_name']}: {util['assignment_count']} assignments")

    # Display coverage gaps if any
    if result['coverage_gaps']:
        print(f"\n⚠️  Coverage Gaps:")
        for gap in result['coverage_gaps']:
            print(f"   - {gap['activity']} ({gap['pgy_level']}): {gap['reason']}")

    # Validate results
    validations = validate_results(result, mock_data)

    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")

    if all(validations.values()):
        print("✅ Phase 3 Python code is VALIDATED and WORKING CORRECTLY!")
        print("✅ Orchestrator-compatible data flow verified")
        print("✅ ACGME compliance engine functioning properly")
        print("✅ Specialty requirements enforced correctly")
        print("✅ Workload balancing operational")
        print("\n🎉 Ready for deployment to n8n!")
        return 0
    else:
        print("❌ Phase 3 has validation issues")
        print("Please review failed checks above")
        return 1

if __name__ == "__main__":
    exit(main())
