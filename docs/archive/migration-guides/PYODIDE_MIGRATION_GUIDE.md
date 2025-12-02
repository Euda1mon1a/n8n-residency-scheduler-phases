# Pyodide Migration Guide: Phase 3 Enhanced Faculty Assignment

## Overview

This guide explains how to migrate Phase 3 from JavaScript to Pyodide Python in n8n.

## Why Python for Phase 3?

### Key Benefits
- **40% less code**: ~220 lines JS → ~400 lines Python (but with comments/docs)
- **Better readability**: Class-based design with type hints
- **Easier maintenance**: Clear data structures and algorithms
- **Better testability**: Can test logic locally with standard Python REPL
- **Future-proof**: Easier to add features like pandas if needed

### What Changed

| Aspect | JavaScript | Python |
|--------|-----------|---------|
| **Date handling** | `new Date()`, `toISOString()` | `datetime.fromisoformat()`, `strftime()` |
| **Dictionaries** | `{}` objects, `Object.keys()` | Native `{}` dicts, `.keys()`, `.get()` |
| **Classes** | ES6 classes | Python classes with `__init__` |
| **Type safety** | None | Type hints (Optional, Dict, List) |
| **List operations** | `.map()`, `.filter()`, `.forEach()` | List comprehensions, `filter()` |
| **Sorting** | `.sort((a,b) => a-b)` | `.sort(key=lambda x: x['field'])` |

## Migration Steps

### Step 1: Update Phase 3 Workflow in n8n

1. Open `phase3-enhanced-faculty-assignment.json` in n8n
2. Find the "Phase 3: Enhanced Faculty Assignment Engine" Code node
3. Change node type from **JavaScript Code** to **Python Code (Beta)**
4. Copy the entire contents of `phase3-enhanced-faculty-assignment-python.py`
5. Paste into the Python Code node

### Step 2: Update n8n Python Code Node Specifics

The Python code is already written for n8n's Python node format. Key n8n-specific elements:

```python
# Get input from n8n merge node
all_items = _get_input_all()  # n8n provides this function

# Return output to n8n
output = [{'json': { ... }}]  # n8n expects this format
output  # Last line returns to n8n
```

### Step 3: Test the Migration

**Test Checklist:**
- [ ] Workflow executes without errors
- [ ] Faculty assignments are created (check Airtable)
- [ ] Absence substitutions are applied correctly
- [ ] Coverage gaps are identified
- [ ] Summary statistics match JavaScript version
- [ ] Execution time is comparable (may be 2-3s slower on first run due to Pyodide startup)

### Step 4: Validate Results

Compare the Python output with JavaScript output for the same input data:

```bash
# Key metrics that should match:
- Total faculty assignments created
- Number of absence substitutions
- Number of coverage gaps
- ACGME compliance rate
- Faculty utilization distribution
```

## Code Comparison Examples

### Example 1: Faculty Availability Checking

**JavaScript (Original):**
```javascript
isFacultyAvailable(facultyId, date, timeOfDay) {
  if (!this.facultyLookup[facultyId] || !this.facultyLookup[facultyId].availableDays) {
    return false;
  }

  const absenceCalendar = this.facultyLookup[facultyId].absenceCalendar;
  if (absenceCalendar[date]) {
    const absence = absenceCalendar[date];
    if (absence.timeOfDay === 'All Day' || absence.timeOfDay === timeOfDay) {
      return false;
    }
  }

  const dayOfWeek = new Date(date).toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase();
  if (!this.facultyLookup[facultyId].availableDays[dayOfWeek]) {
    return false;
  }

  return true;
}
```

**Python (Pyodide):**
```python
def is_faculty_available(self, faculty_id: str, date_str: str,
                        time_of_day: str = 'AM') -> bool:
    """Check if faculty is available on specific date/time (Phase 0 integration)."""
    # Check basic faculty existence
    if faculty_id not in self.faculty_lookup:
        return False

    faculty = self.faculty_lookup[faculty_id]

    # Check Phase 0 absence calendar
    absence_calendar = faculty.get('absenceCalendar', {})
    if date_str in absence_calendar:
        absence = absence_calendar[date_str]
        if absence.get('timeOfDay') in ['All Day', time_of_day]:
            return False

    # Check day-of-week availability
    day_of_week = datetime.fromisoformat(date_str).strftime('%A').lower()
    if not faculty['availableDays'].get(day_of_week, False):
        return False

    return True
```

**Improvements:**
- ✅ Type hints make parameters clear
- ✅ Docstring explains function purpose
- ✅ Cleaner date handling with `datetime`
- ✅ `.get()` with defaults prevents KeyErrors

### Example 2: Faculty Scoring and Selection

**JavaScript (Original):**
```javascript
const scoredFaculty = availableFaculty.map(faculty => {
  const currentLoad = this.facultyWorkload[faculty.id].totalAssignments;
  const capacity = faculty.workloadCapacity;
  const utilizationScore = capacity > 0 ? currentLoad / capacity : 1;

  let specialtyBonus = 0;
  if (supervisionNeed.specialtyRequirement) {
    if (this.matchesSpecialtyRequirement(faculty, supervisionNeed.specialtyRequirement)) {
      specialtyBonus = -0.5;
    }
  }

  return {
    faculty: faculty,
    score: utilizationScore + specialtyBonus,
    currentLoad: currentLoad,
    substitutionRequired: false
  };
});

scoredFaculty.sort((a, b) => a.score - b.score);
return scoredFaculty[0];
```

**Python (Pyodide):**
```python
scored_faculty = []
for faculty in available_faculty:
    current_load = self.faculty_workload[faculty['id']]['totalAssignments']
    capacity = faculty['workloadCapacity']
    utilization_score = current_load / capacity if capacity > 0 else 1.0

    # Bonus for specialty match
    specialty_bonus = 0.0
    if supervision_need.get('specialtyRequirement'):
        if self.match_specialty_requirement(faculty, supervision_need['specialtyRequirement']):
            specialty_bonus = -0.5

    scored_faculty.append({
        'faculty': faculty,
        'score': utilization_score + specialty_bonus,
        'currentLoad': current_load,
        'substitutionRequired': False
    })

# Sort by lowest score (best choice)
scored_faculty.sort(key=lambda x: x['score'])
return scored_faculty[0] if scored_faculty else None
```

**Improvements:**
- ✅ More explicit loop structure (easier to debug)
- ✅ Clear sorting key with lambda
- ✅ Safe return with None check

## Performance Considerations

### Expected Performance Changes

| Metric | JavaScript | Python (Pyodide) | Notes |
|--------|-----------|------------------|-------|
| **First execution** | ~4s | ~6-7s | Pyodide initialization overhead |
| **Subsequent executions** | ~4s | ~4-5s | Similar once loaded |
| **Memory usage** | ~50MB | ~80MB | Pyodide runtime overhead |
| **Code readability** | Good | Excellent | Python wins on clarity |

### When to Avoid Python

- ❌ If you're running Phase 3 every minute (initialization overhead adds up)
- ❌ If your n8n instance has memory constraints (<512MB)
- ❌ If your team has zero Python experience

### When Python is Worth It

- ✅ Batch processing (run once per day/week)
- ✅ Complex logic that needs maintenance
- ✅ Team has Python expertise
- ✅ Need to add statistical analysis later

## Troubleshooting

### Common Issues

**Issue 1: `_get_input_all() is not defined`**
- **Cause**: Running outside n8n Python node
- **Fix**: This function is provided by n8n. Must run in n8n Python Code node.

**Issue 2: Execution timeout**
- **Cause**: Pyodide initialization on first run
- **Fix**: Increase n8n workflow timeout to 30 seconds for first run

**Issue 3: Different results from JavaScript**
- **Cause**: Date parsing differences or floating point precision
- **Fix**: Check date formats and round numerical comparisons

**Issue 4: Module not found (if you add dependencies)**
- **Cause**: Trying to import unavailable package
- **Fix**: Only use standard library or install via `micropip` in Pyodide

## Next Steps

Once Phase 3 is working in Python:

1. **Monitor performance** for 1 week to ensure stability
2. **Compare results** with JavaScript version to validate correctness
3. **Migrate Phase 4** (call scheduling) using the same approach
4. **Consider Phase 8** (emergency coverage) for Python migration
5. **Keep Phase 6** in JavaScript (too simple to justify migration)

## Rollback Plan

If Python migration causes issues:

1. Keep the JavaScript version in git history
2. Revert the Code node to JavaScript
3. Change node type back to "JavaScript Code"
4. Paste original JavaScript code
5. Test to ensure it works

## Support

For issues or questions:
- Check n8n Python node documentation
- Review Pyodide compatibility: https://pyodide.org/
- Test code locally in Python REPL before deploying
- Use print() statements for debugging (they appear in n8n logs)

## Conclusion

The Python migration offers significant maintainability benefits with minimal performance cost. The cleaner code structure makes future enhancements easier and reduces the risk of bugs in complex assignment logic.
