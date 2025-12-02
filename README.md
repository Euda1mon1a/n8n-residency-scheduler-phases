# n8n Residency Scheduler Phases

## Overview

This repository contains a comprehensive medical residency scheduling system built on the n8n automation platform. The system uses a multi-phase architecture orchestrated by a master workflow to handle absence tracking, block pairing, resident associations, and faculty assignments.

## Current Active Workflows

### Master Orchestrator
- **UPDATED-orchestrator-workflow.json** - Master orchestrator that coordinates all scheduling phases

### Phase Workflows
- **UPDATED-phase0-absence-loader.json** - Phase 0: Absence data loading and processing
- **UPDATED-phase1-smart-block-pairing.json** - Phase 1: Smart block pairing logic
- **UPDATED-phase2-smart-resident-association.json** - Phase 2: Resident-to-block associations
- **UPDATED-phase3-enhanced-faculty-assignment.json** - Phase 3: Faculty assignment (orchestrator interface)

### Phase 3 Modular Architecture (v4)
- **phase3-main-v4.json** - Phase 3 data gathering workflow
- **phase3-processing-subworkflow.json** - Phase 3 processing engine with Pyodide Python
- **phase3-enhanced-faculty-assignment-python.py** - Python source for ACGME compliance engine

## Key Features

- **Orchestrator Pattern**: Master workflow coordinates all phases with proper context passing
- **Absence-Aware Scheduling**: Integrates faculty leave data across all phases
- **ACGME Compliance**: Python-powered engine ensures supervision ratios
- **Field ID Mapping**: Uses Airtable field IDs for resilience to schema changes
- **Modular Architecture**: Phase 3 uses subworkflow pattern for clean separation

## Project Structure

```
n8n-residency-scheduler-phases/
├── README.md                                    # This file
├── IMPLEMENTATION-SUMMARY.md                    # Comprehensive implementation guide
├── UPDATED-orchestrator-workflow.json           # Master orchestrator
├── UPDATED-phase0-absence-loader.json           # Phase 0 workflow
├── UPDATED-phase1-smart-block-pairing.json      # Phase 1 workflow
├── UPDATED-phase2-smart-resident-association.json # Phase 2 workflow
├── UPDATED-phase3-enhanced-faculty-assignment.json # Phase 3 interface
├── phase3-main-v4.json                          # Phase 3 main workflow
├── phase3-processing-subworkflow.json           # Phase 3 processing engine
├── phase3-enhanced-faculty-assignment-python.py # Python source code
├── scheduling-conflicts-template.csv            # Template for conflict tracking
├── docs/
│   ├── n8n_ENV.md                              # n8n Code node environment contract
│   ├── airtable_schema.json                    # Airtable schema reference
│   └── archive/                                # Historical documentation
│       ├── validation-reports/
│       ├── migration-guides/
│       ├── design-documents/
│       ├── field-mapping/
│       └── delivery/
├── workflows/
│   ├── phase0+1.json                           # Legacy combined Phase 0+1
│   └── archive/                                # Historical workflow versions
│       ├── phase3-old-versions/
│       ├── phase0-1-2-old-versions/
│       └── orchestrator-old-versions/
├── tests/
│   └── archive/                                # Historical test files
└── atlas/                                      # Atlas workflow management tools
```

## Quick Start

### 1. Import Workflows into n8n

Import workflows in this order:

1. **UPDATED-phase0-absence-loader.json**
2. **UPDATED-phase1-smart-block-pairing.json**
3. **UPDATED-phase2-smart-resident-association.json**
4. **phase3-processing-subworkflow.json** (if using Phase 3)
5. **phase3-main-v4.json** (if using Phase 3)
6. **UPDATED-orchestrator-workflow.json** (master orchestrator)

### 2. Configure Workflow IDs

After importing, update the orchestrator workflow:
- Open **UPDATED-orchestrator-workflow.json** in n8n
- Update each "Execute Phase X" node with the correct workflow ID from your n8n instance
- For Phase 3, point to **phase3-main-v4** workflow

### 3. Configure Airtable Credentials

All workflows require Airtable credentials configured in n8n:
- Ensure your Airtable connection is set up in n8n settings
- All workflows use field IDs (not field names) for reliability

### 4. Run the Orchestrator

Execute the **UPDATED-orchestrator-workflow** to run all phases sequentially with proper data passing.

## Documentation

- **IMPLEMENTATION-SUMMARY.md** - Comprehensive implementation guide covering architecture, data flow, and troubleshooting
- **docs/n8n_ENV.md** - n8n Code node environment contract and requirements
- **docs/airtable_schema.json** - Airtable schema reference
- **docs/archive/** - Historical validation reports, migration guides, and design documents

## Archive Structure

Historical documents and superseded workflow versions are preserved in organized archive directories:

- **docs/archive/validation-reports/** - Phase 3/4 validation reports
- **docs/archive/migration-guides/** - Python migration and orchestrator compatibility guides
- **docs/archive/design-documents/** - Phase 8 design and conflict tracking specifications
- **workflows/archive/** - Old workflow versions and iterations
- **tests/archive/** - Historical test files and reports

## Architecture Highlights

### Data Flow
1. **Phase 0** loads absence data from Airtable
2. **Phase 1** pairs half-day blocks using absence data
3. **Phase 2** associates residents with blocks
4. **Phase 3** assigns faculty with ACGME compliance checking
5. **Orchestrator** manages state and passes context between phases

### Phase 3 Subworkflow Pattern
- **phase3-main-v4.json** handles data gathering and can be called by orchestrator
- **phase3-processing-subworkflow.json** contains the Python/Pyodide processing engine
- Clean separation follows n8n Cloud compatibility guidelines

### Field ID Strategy
All workflows use Airtable field IDs (e.g., `fldHalfDayOfWeekBlocks`) instead of field names for resilience to schema changes.

## Contributing

Contributions are welcome! Please ensure:
- Workflow JSON files do not contain sensitive credentials
- Changes are accompanied by clear descriptions
- Field ID mapping is used (not field names)
- Documentation is updated to reflect changes

## Support

For detailed implementation guidance, troubleshooting, and architecture details, see:
- **IMPLEMENTATION-SUMMARY.md** - Main implementation guide
- **docs/archive/migration-guides/** - Migration and compatibility guides
- **docs/archive/validation-reports/** - Testing and validation details
