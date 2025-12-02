# n8n Code Node Environment Contract

## Purpose

This document defines the environment contract for any code that will run inside n8n Code nodes in this project. All code contributions must adhere to these rules to ensure compatibility, reliability, and maintainability across the n8n residency scheduling system.

## General n8n Items Model

### Input Structure
- Input to a Code node is **`items`**, an array of objects
- Each object in the array has at least a **`json`** key containing the actual data
- Example input structure:
  ```javascript
  [
    { json: { id: 1, name: "John Doe", date: "2025-01-15" } },
    { json: { id: 2, name: "Jane Smith", date: "2025-01-16" } }
  ]
  ```

### Output Structure
- Output from a Code node must maintain the same shape as input
- Return an array of objects with **`json`** keys that n8n can route forward
- Example output structure:
  ```javascript
  [
    { json: { id: 1, name: "John Doe", processed: true } },
    { json: { id: 2, name: "Jane Smith", processed: true } }
  ]
  ```

### Shape Preservation
- **Do not silently change the overall shape of `items`** unless the node is explicitly intended to do so
- If you need to aggregate, filter, or transform the structure, ensure it's documented and intentional
- Always maintain the `json` key structure for compatibility with downstream nodes

## JavaScript Code Node Rules

### Environment
- Code runs in **n8n's JavaScript sandbox**, not a full Node.js environment
- No filesystem access, no network access (except through n8n nodes)
- Limited to JavaScript features available in the sandbox

### Input/Output Pattern
- **Always read from `items`** variable provided by n8n
- **Always return an array of items** at the end of your code
- Typical pattern:
  ```javascript
  // Read input
  const inputData = items[0].json;

  // Process data
  const result = processData(inputData);

  // Return in n8n format
  return items.map(item => ({
    json: {
      ...item.json,
      processed: true,
      result: result
    }
  }));
  ```

### Module Usage
- **Avoid `require()` and `import`** statements except for modules documented as built-in for n8n
- Common available modules may include basic utilities, but always verify in n8n documentation
- When in doubt, implement logic directly rather than importing external dependencies

### Code Style
- **Prefer small, pure functions** and data transformations
- **Avoid side effects** (external state changes, mutations)
- Keep code focused on transforming input data to output data
- Use descriptive variable names for clarity

### Example: Valid JavaScript Code Node

```javascript
// ✅ VALID: Processes items and returns transformed array
const processedItems = items.map(item => {
  const { date, facultyId, timeOfDay } = item.json;

  // Pure transformation logic
  const dayOfWeek = new Date(date).toLocaleDateString('en-US', { weekday: 'long' });
  const isWeekend = ['Saturday', 'Sunday'].includes(dayOfWeek);

  return {
    json: {
      ...item.json,
      dayOfWeek: dayOfWeek,
      isWeekend: isWeekend,
      shift: timeOfDay === 'AM' ? 'morning' : 'afternoon'
    }
  };
});

return processedItems;
```

### Example: Invalid JavaScript Code Node

```javascript
// ❌ INVALID: Uses require() for unavailable module
const axios = require('axios'); // Not available in n8n sandbox

// ❌ INVALID: Doesn't return items array
const result = items[0].json.value * 2;
return result; // Should return array of items with json keys

// ❌ INVALID: Attempts filesystem access
const fs = require('fs');
fs.writeFileSync('/tmp/data.json', JSON.stringify(items)); // Not allowed
```

## Python Code Node (Pyodide) Rules

### Environment
- Python Code nodes run in a **Pyodide** environment (Python compiled to WebAssembly)
- Browser-based Python runtime with significant limitations
- **No `pip install`** during execution
- **No arbitrary network I/O** or filesystem operations
- **No long-running blocking operations** (risk of timeout)

### Available Packages
- Use only the **Python standard library** (`datetime`, `json`, `re`, `math`, etc.)
- Use packages that **Pyodide provides out of the box** (e.g., `micropip` for limited package management)
- Check [Pyodide package list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) for available packages
- Common available packages: `numpy`, `pandas`, `scipy` (verify version compatibility)

### Input/Output Pattern
- Input is accessed via n8n-provided functions like **`_get_input_all()`**
- Treat the input as a Python representation of `items` (list of dictionaries)
- **Return a list of dictionaries** with `"json"` keys
- The last expression in the code is returned to n8n

### Typical Pattern

```python
# Get input from n8n
all_items = _get_input_all()

# Extract data from the first item (adjust as needed)
input_data = all_items[0]['json']

# Process data with pure Python logic
def process_faculty_assignment(data):
    from datetime import datetime

    date_obj = datetime.fromisoformat(data['date'])
    day_of_week = date_obj.strftime('%A').lower()

    return {
        'facultyId': data['facultyId'],
        'date': data['date'],
        'dayOfWeek': day_of_week,
        'isWeekend': day_of_week in ['saturday', 'sunday']
    }

# Process all items
processed_items = [
    {'json': process_faculty_assignment(item['json'])}
    for item in all_items
]

# Return output (last expression)
processed_items
```

### Code Style
- **Focus on pure data transformations**
- Use **type hints** for clarity (optional but recommended):
  ```python
  def is_faculty_available(faculty_id: str, date_str: str, time_of_day: str = 'AM') -> bool:
      # Implementation
      pass
  ```
- Use **docstrings** for complex functions
- Leverage Python's built-in data structures (`dict`, `list`, `set`)
- Use **list comprehensions** and **generator expressions** for concise transformations

### Example: Valid Python Code Node

```python
# ✅ VALID: Uses standard library and returns proper structure
from datetime import datetime
from typing import Dict, List, Optional

all_items = _get_input_all()

def calculate_workload_score(faculty: Dict) -> float:
    """Calculate workload utilization score for faculty member."""
    current_load = faculty.get('totalAssignments', 0)
    capacity = faculty.get('workloadCapacity', 1)
    return current_load / capacity if capacity > 0 else 1.0

# Process items
output = []
for item in all_items:
    faculty_data = item['json']
    score = calculate_workload_score(faculty_data)

    output.append({
        'json': {
            'facultyId': faculty_data['id'],
            'workloadScore': score,
            'isOverloaded': score > 0.8
        }
    })

# Return to n8n
output
```

### Example: Invalid Python Code Node

```python
# ❌ INVALID: Attempts pip install
import subprocess
subprocess.run(['pip', 'install', 'requests'])  # Not allowed in Pyodide

# ❌ INVALID: Attempts network access
import urllib.request
response = urllib.request.urlopen('https://api.example.com/data')  # Not allowed

# ❌ INVALID: Attempts filesystem I/O
with open('/tmp/data.json', 'w') as f:  # Not allowed in Pyodide
    f.write(json.dumps(data))

# ❌ INVALID: Long-running blocking operation
import time
time.sleep(300)  # Will timeout

# ❌ INVALID: Wrong return structure
result = all_items[0]['json']['value'] * 2
result  # Should return list of dicts with 'json' keys
```

## Validity Criteria for Contributions

All code contributions must pass the following validity checks:

### ❌ Invalid Code Patterns

1. **Uses `pip install` or attempts package installation**
   ```python
   # INVALID
   import micropip
   await micropip.install('some-package')
   ```

2. **Performs arbitrary file reads or writes**
   ```javascript
   // INVALID
   const fs = require('fs');
   fs.writeFileSync('/tmp/output.txt', data);
   ```

3. **Makes network calls not explicitly allowed by this project**
   ```python
   # INVALID (unless specifically approved for this project)
   import requests
   requests.get('https://external-api.com')
   ```

4. **Does not consume `items` as input**
   ```javascript
   // INVALID - hardcoded data instead of reading items
   const data = { id: 1, name: "John" };
   return [{ json: data }];
   ```

5. **Does not return array of items as output**
   ```javascript
   // INVALID - returns single object instead of array
   return { json: { result: "success" } };
   ```

6. **Returns data without proper `json` key structure**
   ```python
   # INVALID - missing 'json' wrapper
   output = [{'facultyId': 'f1', 'date': '2025-01-15'}]
   output
   ```

### ✅ Valid Code Patterns

1. **Reads from `items` input**
   ```javascript
   const inputData = items[0].json;
   ```

2. **Returns array of items with `json` keys**
   ```javascript
   return items.map(item => ({
     json: { ...item.json, processed: true }
   }));
   ```

3. **Uses only standard library or Pyodide-provided packages**
   ```python
   from datetime import datetime
   import json
   ```

4. **Performs pure data transformations**
   ```python
   result = [process(item['json']) for item in all_items]
   ```

5. **Includes all necessary helper functions in the code**
   ```javascript
   // Helper function defined in-place
   function calculateScore(data) {
     return data.value * 0.8 + data.bonus;
   }

   return items.map(item => ({
     json: {
       ...item.json,
       score: calculateScore(item.json)
     }
   }));
   ```

## "Ready to Drop" Requirement

All code examples and contributions must be **"ready to drop"** into an n8n Code node:

- ✅ **Self-contained**: No missing imports, helpers, or dependencies
- ✅ **No placeholders**: All functions and variables are defined
- ✅ **Correct input/output**: Uses `items` or `_get_input_all()` and returns proper structure
- ✅ **Tested**: Code has been validated in an actual n8n Code node
- ❌ **No pseudo-code**: Every line must be executable JavaScript or Python

### Example: Ready to Drop

```javascript
// ✅ This code can be copy-pasted directly into n8n JavaScript Code node
const now = new Date();
const currentHour = now.getHours();

const processedItems = items.map(item => {
  const shiftType = item.json.timeOfDay === 'AM'
    ? 'morning'
    : 'afternoon';

  const isCurrentShift = (
    (shiftType === 'morning' && currentHour >= 6 && currentHour < 14) ||
    (shiftType === 'afternoon' && currentHour >= 14 && currentHour < 22)
  );

  return {
    json: {
      ...item.json,
      shiftType: shiftType,
      isCurrentShift: isCurrentShift,
      processedAt: now.toISOString()
    }
  };
});

return processedItems;
```

### Example: Not Ready to Drop

```javascript
// ❌ This code is NOT ready to drop (missing helper, uses undefined variables)
const result = processData(items); // processData() is not defined
const config = getConfig(); // getConfig() is not defined

return result.map(item => ({
  json: { ...item, config: config }
}));
```

## Testing Code Locally

### JavaScript Code Nodes
- Test logic in a standard JavaScript environment (Node.js, browser console)
- Remove any Node.js-specific APIs before deploying to n8n
- Use `console.log()` for debugging (appears in n8n execution logs)

### Python Code Nodes
- Test in a local Python REPL or Jupyter notebook
- Mock the `_get_input_all()` function with sample data:
  ```python
  # Local testing mock
  def _get_input_all():
      return [
          {'json': {'id': 1, 'name': 'Test'}},
          {'json': {'id': 2, 'name': 'Test2'}}
      ]
  ```
- Ensure no external dependencies beyond standard library + Pyodide packages
- Use `print()` for debugging (appears in n8n execution logs)

## Error Handling

### JavaScript
```javascript
// Wrap risky operations in try-catch
return items.map(item => {
  try {
    const result = processData(item.json);
    return {
      json: {
        ...item.json,
        result: result,
        error: null
      }
    };
  } catch (error) {
    return {
      json: {
        ...item.json,
        result: null,
        error: error.message
      }
    };
  }
});
```

### Python
```python
# Handle errors gracefully
output = []
for item in all_items:
    try:
        result = process_data(item['json'])
        output.append({
            'json': {
                **item['json'],
                'result': result,
                'error': None
            }
        })
    except Exception as e:
        output.append({
            'json': {
                **item['json'],
                'result': None,
                'error': str(e)
            }
        })

output
```

## Performance Guidelines

1. **Avoid nested loops** when possible (use dictionaries for lookups)
2. **Minimize object copies** (use references when safe)
3. **Be mindful of large datasets** (n8n Code nodes have memory limits)
4. **Use early returns** to short-circuit unnecessary processing
5. **Keep Python code simple** (Pyodide startup has ~2-3s overhead on first run)

### Example: Efficient Lookup Pattern

```javascript
// ✅ Efficient O(n) lookup
const facultyById = {};
facultyItems.forEach(item => {
  facultyById[item.json.id] = item.json;
});

return assignmentItems.map(item => {
  const faculty = facultyById[item.json.facultyId]; // O(1) lookup
  return {
    json: {
      ...item.json,
      facultyName: faculty ? faculty.name : 'Unknown'
    }
  };
});

// ❌ Inefficient O(n²) nested loop
return assignmentItems.map(item => {
  const faculty = facultyItems.find(f =>
    f.json.id === item.json.facultyId  // O(n) for each item
  );
  return {
    json: {
      ...item.json,
      facultyName: faculty ? faculty.json.name : 'Unknown'
    }
  };
});
```

## Summary

This environment contract ensures that all n8n Code node implementations in this project are:

- **Compatible**: Work within n8n's sandbox limitations
- **Reliable**: Follow consistent input/output patterns
- **Maintainable**: Use clear, testable code patterns
- **Portable**: "Ready to drop" into any n8n Code node
- **Performant**: Avoid common performance pitfalls

All contributors must validate their code against these rules before submitting pull requests. Code that violates this contract must be rewritten to comply before it can be merged.

## Related Documentation

- For migrating existing JavaScript phases to Python, see: [PYODIDE_MIGRATION_GUIDE.md](../PYODIDE_MIGRATION_GUIDE.md)
- For n8n workflow structure, see: [README.md](../README.md)
