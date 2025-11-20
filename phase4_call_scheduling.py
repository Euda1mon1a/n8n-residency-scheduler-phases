import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import math

class CallSchedulingEngine:
    """Advanced call scheduling with equity management and absence awareness"""
    
    def __init__(self, faculty_list: List[Dict], leave_records: List[Dict],
                 config: Dict):
        self.faculty = {f['id']: self._enhance_faculty_profile(f) for f in faculty_list}
        self.absence_calendar = self._process_absences(leave_records)
        self.config = config
        self.assignments = []
        self.faculty_last_call = {}
        self.substitutions = []
        self.gaps = []
    
    def _enhance_faculty_profile(self, faculty: Dict) -> Dict:
        """Create enhanced faculty profile with call history"""
        return {
            'id': faculty['id'],
            'name': faculty.get('Faculty', faculty.get('Last Name', 'Unknown')),
            'call_counts': {
                'monday': faculty.get('Total Monday Call', 0),
                'tuesday': faculty.get('Total Tuesday Call', 0),
                'wednesday': faculty.get('Total Wednesday Call', 0),
                'thursday': faculty.get('Total Thursday Call', 0),
                'friday': faculty.get('Total Friday Call', 0),
                'saturday': faculty.get('Total Saturday Call', 0),
                'sunday': faculty.get('Total Sunday Call', 0)
            },
            'total_calls': sum([
                faculty.get('Total Monday Call', 0),
                faculty.get('Total Tuesday Call', 0),
                faculty.get('Total Wednesday Call', 0),
                faculty.get('Total Thursday Call', 0),
                faculty.get('Total Friday Call', 0),
                faculty.get('Total Saturday Call', 0),
                faculty.get('Total Sunday Call', 0)
            ]),
            'inpatient_weeks': faculty.get('Total Inpatient Weeks', 0),
            'is_active': faculty.get('Faculty Status', 'Active') != 'Inactive'
        }
    
    def _process_absences(self, leave_records: List[Dict]) -> Dict[str, Dict[str, Dict]]:
        """Process faculty leave into absence calendar"""
        calendar = {}
        
        for leave in leave_records:
            faculty_ids = leave.get('Faculty', [])
            # Handle potential string vs list for Faculty field
            if isinstance(faculty_ids, str):
                faculty_ids = [faculty_ids]
                
            start_str = leave.get('Leave Start')
            end_str = leave.get('Leave End')
            
            if not start_str or not end_str:
                continue
                
            start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            
            current = start
            while current <= end:
                date_str = current.strftime('%Y-%m-%d')
                
                for fac_id in faculty_ids:
                    if fac_id not in calendar:
                        calendar[fac_id] = {}
                    
                    calendar[fac_id][date_str] = {
                        'leave_type': leave.get('Leave Type', 'Leave'),
                        'comments': leave.get('Comments', ''),
                        'replacement': leave.get('Comments', '') or 'Leave'
                    }
                
                current += timedelta(days=1)
        
        return calendar
    
    def is_faculty_available(self, faculty_id: str, date: str) -> bool:
        """Check if faculty available for call on specific date"""
        if faculty_id not in self.faculty or not self.faculty[faculty_id]['is_active']:
            return False
        
        # Check absence calendar
        if faculty_id in self.absence_calendar:
            if date in self.absence_calendar[faculty_id]:
                return False
        
        return True
    
    def calculate_equity_score(self, faculty_id: str) -> float:
        """Calculate equity score (lower is more fair to assign)"""
        faculty = self.faculty[faculty_id]
        if not self.faculty:
            return 0.0
        avg_calls = sum(f['total_calls'] for f in self.faculty.values()) / len(self.faculty)
        
        equity_score = faculty['total_calls'] - avg_calls
        
        # Adjust for absences (faculty with more absences get lower scores)
        absence_count = len(self.absence_calendar.get(faculty_id, {}))
        equity_score -= (absence_count * 0.1)
        
        return equity_score
    
    def calculate_gap_penalty(self, faculty_id: str, date: str) -> float:
        """Calculate penalty for gap violations (min 3 days between calls)"""
        if faculty_id not in self.faculty_last_call:
            return 0.0
        
        last_call = datetime.fromisoformat(self.faculty_last_call[faculty_id])
        current_date = datetime.fromisoformat(date)
        
        days_between = (current_date - last_call).days
        
        if days_between < self.config['minimum_gap_days']:
            # Exponential penalty for gap violations
            return math.pow(self.config['minimum_gap_days'] - days_between + 1, 3)
        
        return 0.0
    
    def score_faculty_for_call(self, faculty_id: str, date: str, is_weekend: bool, 
                                is_holiday: bool) -> float:
        """Calculate total score for assigning faculty to call (lower is better)"""
        # Gap penalty (70% weight)
        gap_penalty = self.calculate_gap_penalty(faculty_id, date) * 0.7
        
        # Equity penalty (30% weight)
        equity_score = self.calculate_equity_score(faculty_id)
        call_weight = (self.config['holiday_weight'] if is_holiday 
                      else self.config['weekend_weight'] if is_weekend 
                      else 1.0)
        equity_penalty = (equity_score + call_weight) * 0.3
        
        return gap_penalty + equity_penalty
    
    def assign_call(self, date: str, day_of_week: str, is_weekend: bool, 
                   is_holiday: bool) -> Optional[Dict]:
        """Assign call for specific date"""
        call_weight = (self.config['holiday_weight'] if is_holiday 
                      else self.config['weekend_weight'] if is_weekend 
                      else 1.0)
        
        # Get available faculty
        available = [fid for fid in self.faculty.keys() 
                    if self.is_faculty_available(fid, date)]
        
        if not available:
            # Check for substitution opportunities
            absent_with_replacement = [
                fid for fid in self.faculty.keys()
                if fid in self.absence_calendar and date in self.absence_calendar[fid]
                and self.absence_calendar[fid][date]['replacement']
            ]
            
            if absent_with_replacement:
                faculty_id = absent_with_replacement[0]
                absence_info = self.absence_calendar[faculty_id][date]
                
                assignment = {
                    'date': date,
                    'day_of_week': day_of_week,
                    'faculty_id': faculty_id,
                    'faculty_name': self.faculty[faculty_id]['name'],
                    'call_type': absence_info['replacement'],
                    'original_call_type': 'Overnight Call',
                    'is_weekend': is_weekend,
                    'is_holiday': is_holiday,
                    'call_weight': call_weight,
                    'substitution_applied': True,
                    'absence_type': absence_info['leave_type'],
                    'python_powered': True
                }
                
                self.assignments.append(assignment)
                self.substitutions.append(assignment)
                return assignment
            
            # No faculty available - create gap
            self.gaps.append({
                'date': date,
                'day_of_week': day_of_week,
                'reason': 'All faculty absent',
                'is_weekend': is_weekend,
                'is_holiday': is_holiday
            })
            return None
        
        # Score all available faculty
        scored = [
            (fid, self.score_faculty_for_call(fid, date, is_weekend, is_holiday))
            for fid in available
        ]
        scored.sort(key=lambda x: x[1])
        
        # Assign to best scoring faculty
        faculty_id = scored[0][0]
        penalty_score = scored[0][1]
        
        gap_days = None
        if faculty_id in self.faculty_last_call:
            last_call = datetime.fromisoformat(self.faculty_last_call[faculty_id])
            current_date = datetime.fromisoformat(date)
            gap_days = (current_date - last_call).days
        
        assignment = {
            'date': date,
            'day_of_week': day_of_week,
            'faculty_id': faculty_id,
            'faculty_name': self.faculty[faculty_id]['name'],
            'call_type': 'Overnight Call',
            'is_weekend': is_weekend,
            'is_holiday': is_holiday,
            'call_weight': call_weight,
            'penalty_score': penalty_score,
            'gap_days': gap_days,
            'substitution_applied': False,
            'python_powered': True
        }
        
        # Update state
        self.faculty_last_call[faculty_id] = date
        self.faculty[faculty_id]['total_calls'] += call_weight
        
        self.assignments.append(assignment)
        return assignment
    
    def generate_call_schedule(self, start_date: str, weeks: int = 4) -> Dict:
        """Generate call schedule for specified period"""
        print(f"\\nGenerating {weeks}-week call schedule starting {start_date}")
        
        start = datetime.fromisoformat(start_date)
        
        for week in range(weeks):
            for day in range(7):
                current_date = start + timedelta(weeks=week, days=day)
                date_str = current_date.strftime('%Y-%m-%d')
                day_name = current_date.strftime('%A').lower()
                is_weekend = day_name in ['saturday', 'sunday']
                is_holiday = self._is_holiday(current_date)
                
                self.assign_call(date_str, day_name, is_weekend, is_holiday)
            
            print(f"  Week {week + 1} complete")
        
        # Calculate statistics
        stats = {
            'total_dates': weeks * 7,
            'successful_assignments': len([a for a in self.assignments if not a.get('substitution_applied')]),
            'substitutions': len(self.substitutions),
            'gaps': len(self.gaps),
            'coverage_rate': f"{(len(self.assignments) / (weeks * 7) * 100):.1f}%",
            'substitution_rate': f"{(len(self.substitutions) / max(len(self.assignments), 1) * 100):.1f}%",
            'gap_violations': sum(1 for a in self.assignments 
                                 if a.get('gap_days') and a['gap_days'] < self.config['minimum_gap_days'])
        }
        
        return {
            'assignments': self.assignments,
            'substitutions': self.substitutions,
            'gaps': self.gaps,
            'statistics': stats,
            'faculty_utilization': [
                {'faculty_id': fid, 'faculty_name': f['name'], 'total_calls': f['total_calls']}
                for fid, f in self.faculty.items()
            ]
        }
    
    def _is_holiday(self, date: datetime) -> bool:
        """Check if date is a major holiday"""
        return (
            (date.month == 12 and date.day == 25) or  # Christmas
            (date.month == 1 and date.day == 1) or     # New Year
            (date.month == 7 and date.day == 4) or     # July 4th
            (date.month == 11 and date.day == 11)      # Veterans Day
        )

def run_phase4(faculty_data: List[Dict], leave_records: List[Dict], config: Optional[Dict] = None) -> Dict:
    """Wrapper to run Phase 4 logic"""
    if config is None:
        config = {
            'minimum_gap_days': 3,
            'weekend_weight': 1.5,
            'holiday_weight': 2.0,
            'max_calls_per_month': 8
        }
        
    engine = CallSchedulingEngine(faculty_data, leave_records, config)
    
    # Determine start date (next Monday)
    today = datetime.now()
    days_ahead = 0 - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    start_date = (today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    
    return engine.generate_call_schedule(start_date, weeks=4)
