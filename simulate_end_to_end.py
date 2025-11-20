import json
from datetime import datetime, timedelta
import random
from phase3_faculty_assignment import run_phase3
from phase4_call_scheduling import run_phase4
from phase7_validation import run_phase7_validation

def create_mock_data():
    """Create comprehensive mock data for simulation"""
    print("Generating mock data...")
    
    # Faculty
    faculty_data = [
        {
            'id': f'fac_{i}',
            'Faculty': f'Faculty {i}',
            'Last Name': f'Faculty {i}',
            'Faculty Status': 'Active',
            'Primary Duty': 'Faculty' if i < 3 else 'Sports Medicine' if i == 3 else 'Leadership',
            'Performs Procedure': i % 2 == 0,
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
        }
        for i in range(5)
    ]
    
    # Residents
    residents = [
        {
            'id': f'res_{i}',
            'Resident': f'Resident {i}',
            'PGY Level': f'PGY-{1 + (i % 3)}'
        }
        for i in range(10)
    ]
    
    # Master Assignments (Phase 2 Output)
    master_assignments = []
    today = datetime.now()
    start_date = today - timedelta(days=today.weekday()) # Start of this week
    
    for i in range(20): # 20 assignments
        res = residents[i % len(residents)]
        day_offset = i % 5
        date_str = (start_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        
        master_assignments.append({
            'id': f'assign_{i}',
            'Resident (from Residency Block Schedule)': [res['id']],
            'PGY Link (from Residency Block Schedule)': [res['PGY Level']],
            'Half-Day of the Week of Blocks': [f'hd_{i}'],
            'Activity (from Rotation Templates)': ['General Clinic'],
            # Mocking date in ID or separate field for simulation
            'Date': date_str 
        })
        
    # Leave Data (Phase 0 Output)
    leave_records = [] # No leave for base case
    absence_data = {'facultyAbsences': {}, 'facultyReference': {}}
    
    # Primary Duties
    primary_duties = [
        {
            'Faculty': [f['id'] for f in faculty_data],
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
        'faculty_data': faculty_data,
        'residents': residents,
        'master_assignments': master_assignments,
        'leave_records': leave_records,
        'absence_data': absence_data,
        'primary_duties': primary_duties,
        'clinic_templates': [{'id': 'tmpl_1', 'Name': 'General Clinic', 'Activity Type': 'Clinic'}]
    }

def main():
    print("=== END-TO-END RESIDENCY SCHEDULER SIMULATION ===")
    
    # 1. Setup Data
    data = create_mock_data()
    
    # 2. Run Phase 3 (Faculty Assignment)
    print("\n--- Running Phase 3: Faculty Assignment ---")
    phase3_results = run_phase3(
        data['master_assignments'],
        data['faculty_data'],
        data['clinic_templates'],
        data['absence_data']
    )
    print(f"Generated {len(phase3_results['assignments'])} faculty assignments")
    
    # 3. Run Phase 4 (Call Scheduling)
    print("\n--- Running Phase 4: Call Scheduling ---")
    phase4_results = run_phase4(
        data['faculty_data'],
        data['leave_records']
    )
    print(f"Generated {len(phase4_results['assignments'])} call assignments")
    
    # 4. Run Phase 7 (Validation)
    print("\n--- Running Phase 7: Final Validation ---")
    
    # Prepare data context for validation
    validation_context = {
        'master_assignments': data['master_assignments'],
        'faculty_assignments': phase3_results['assignments'],
        'call_assignments': phase4_results['assignments'],
        'active_faculty': data['faculty_data'],
        'residents': data['residents'],
        'primary_duties': data['primary_duties']
    }
    
    validation_report = run_phase7_validation(validation_context)
    
    print("\n=== VALIDATION REPORT ===")
    print(json.dumps(validation_report, indent=2))
    
    if validation_report['readyForDeployment']:
        print("\n✅ SIMULATION SUCCESSFUL: System is ready for deployment")
    else:
        print("\n⚠️ SIMULATION COMPLETED WITH WARNINGS: Review validation report")

if __name__ == "__main__":
    main()
