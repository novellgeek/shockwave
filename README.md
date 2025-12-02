# SHOCKWAVE PLANNER v1.0

Desktop Launch Operations Planning System for tracking launch activities.

## Overview

SHOCKWAVE PLANNER is a comprehensive desktop application for tracking and managing launch operations data, with a focus on Chinese space launch activities. It features:

- **Calendar View**: Visual monthly calendar showing launches
- **List View**: Searchable table of all launches
- **Statistics Dashboard**: Overview of launch statistics and trends
- **Database-backed**: SQLite database for reliable data storage
- **Launch Editor**: Easy-to-use interface for adding and editing launches

## Features

### Data Tracking
- Launch dates and times
- Launch sites and pads
- Rocket types and configurations
- Mission names and payloads
- Orbit types and parameters
- Launch status tracking
- Success/failure records
- Remarks and notes

### Pre-populated Data
- 15+ Chinese launch sites (Jiuquan, Taiyuan, Xichang, Wenchang)
- 25+ rocket types (Long March series, commercial launchers)
- 7 launch status types
- Sample launch data for November-December 2025

### User Interface
- **Calendar View**: Color-coded monthly calendar with launch details
- **List View**: Searchable and sortable launch list
- **Statistics**: Launch success rates, top rockets, site usage
- **Launch Editor**: Form-based entry/editing with validation

## Installation

### Requirements
- Python 3.9+
- PyQt6

### Setup
```bash
pip install PyQt6 --break-system-packages

# Clone or download the application
cd shockwave_planner

# Run the application
python3 main.py
```

## Usage

### Starting the Application
```bash
python3 /home/claude/shockwave_planner/main.py
```

### Adding a Launch
1. Click "➕ New Launch" button or press Ctrl+N
2. Fill in the launch details:
   - Date and time
   - Launch site and pad
   - Rocket type
   - Mission and payload names
   - Orbit type
   - Status
   - Optional remarks
3. Click "Save"

### Editing a Launch
1. Double-click a launch in List View, or
2. Click a day with launches in Calendar View
3. Modify the details
4. Click "Save"

### Searching Launches
- Use the search box in List View
- Search by mission name, payload, or rocket type
- Results update as you type

### Navigating the Calendar
- Use "◀ Previous" and "Next ▶" buttons to change months
- Click on any day to view/edit launches
- Color coding indicates launch status:
  - Yellow: Scheduled
  - Green: Go/Success
  - Orange: Scrubbed
  - Red: Failure
  - Gray: Unknown

## Database Schema

### Tables
- **launch_sites**: Launch facility locations and pads
- **rockets**: Rocket types and specifications
- **launch_vehicles**: Specific rocket configurations
- **launch_status**: Status types (Scheduled, Success, etc.)
- **launches**: Main launch records
- **launch_tles**: TLE data associated with launches
- **launch_predictions**: Predicted vs actual launch times

### Database Location
`shockwave_planner.db` in the application directory

## Integration with TAWHIRI

SHOCKWAVE PLANNER is designed to integrate with the TAWHIRI space domain awareness platform:

- Shared SQLite database format
- TLE tracking integration
- Compatible launch site nomenclature
- Space weather correlation (planned)

## Keyboard Shortcuts

- `Ctrl+N`: New Launch
- `Ctrl+Q`: Exit
- `F5`: Refresh all views

## Data Sources

Pre-populated data includes:
- Chinese launch sites from public sources
- Long March rocket family specifications
- Commercial launcher data (Galactic Energy, Landspace, i-Space, etc.)
- Historical launch records

## Future Enhancements

Planned features based on specification:
- Orbital element tracking
- Conjunction screening
- Launch window calculations
- Space weather integration
- Re-entry predictions
- TLE scraping and auto-update
- Export to Excel/PDF
- Launch manifest import
- Multi-country support

## Technical Details

### Architecture
```
shockwave_planner/
├── main.py                 # Application entry point
├── gui/
│   └── main_window.py     # Main window and UI components
├── data/
│   └── database.py        # Database layer
└── resources/             # Icons and assets (future)
```

### Technology Stack
- **GUI Framework**: PyQt6
- **Database**: SQLite3
- **Language**: Python 3.9+

## License

Proprietary - Remix Astronautics

## Author

Remix Astronautics
November 2025

## Support

For issues or questions, contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: November 29, 2025
